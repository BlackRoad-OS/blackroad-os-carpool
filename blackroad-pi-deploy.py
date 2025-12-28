#!/usr/bin/env python3
"""
BlackRoad Pi Deployment Automation
Deploys all repositories to Raspberry Pis with automatic:
- Docker containerization
- Caddy configuration
- DNS management
- GitHub Actions setup
"""

import yaml
import subprocess
import os
from pathlib import Path

class BlackRoadPiDeployer:
    def __init__(self, config_file='pi-infrastructure.yaml'):
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
        self.public_ip = self.config['global']['public_ip']

    def generate_caddyfile(self):
        """Generate master Caddyfile for all domains across all Pis"""
        caddy_config = []

        for pi_name, pi_config in self.config['pis'].items():
            pi_ip = pi_config['ip']
            for domain_config in pi_config['domains']:
                domain = domain_config['domain']
                port = domain_config['port']

                caddy_config.append(f"""
{domain} {{
    reverse_proxy {pi_ip}:{port}
    encode gzip
    header {{
        X-Powered-By "BlackRoad OS"
        X-Pi "{pi_name}"
    }}
}}
""")

        return '\n'.join(caddy_config)

    def generate_github_action(self, repo_name):
        """Generate GitHub Action for auto-deploy to Pi"""
        # Find which Pi this repo deploys to
        target_pi = None
        target_port = None

        for pi_name, pi_config in self.config['pis'].items():
            for domain_config in pi_config['domains']:
                if domain_config['repo'] == repo_name:
                    target_pi = pi_name
                    target_port = domain_config['port']
                    break
            if target_pi:
                break

        if not target_pi:
            return None

        return f"""name: Deploy to {target_pi} Pi

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js (if needed)
        if: hashFiles('package.json') != ''
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Build Application
        run: |
          if [ -f "package.json" ]; then
            npm install --legacy-peer-deps
            npm run build
          fi

      - name: Deploy to {target_pi}
        env:
          PI_HOST: ${{{{ secrets.{target_pi.upper()}_HOST }}}}
          PI_USER: ${{{{ secrets.PI_USER }}}}
          PI_SSH_KEY: ${{{{ secrets.PI_SSH_KEY }}}}
        run: |
          # Setup SSH
          mkdir -p ~/.ssh
          echo "$PI_SSH_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H $PI_HOST >> ~/.ssh/known_hosts

          # Create deployment package
          tar -czf deploy.tar.gz .

          # Upload to Pi
          scp deploy.tar.gz $PI_USER@$PI_HOST:~/deploys/{repo_name}.tar.gz

          # Deploy on Pi
          ssh $PI_USER@$PI_HOST << 'ENDSSH'
            cd ~/deploys
            mkdir -p {repo_name}
            tar -xzf {repo_name}.tar.gz -C {repo_name}
            cd {repo_name}

            # Create/update Docker container
            docker build -t {repo_name}:latest .
            docker stop {repo_name} || true
            docker rm {repo_name} || true
            docker run -d --name {repo_name} \\
              -p {target_port}:3000 \\
              --restart unless-stopped \\
              {repo_name}:latest

            echo "Deployed {repo_name} to port {target_port}"
ENDSSH

          echo "✅ Deployment complete to {target_pi}:{target_port}"
"""

    def deploy_all(self):
        """Deploy all repositories to their designated Pis"""
        print("═══════════════════════════════════════════════════════════")
        print("  BlackRoad Pi Mass Deployment")
        print("═══════════════════════════════════════════════════════════\n")

        # Generate master Caddyfile
        caddyfile = self.generate_caddyfile()
        with open('/tmp/Caddyfile.all', 'w') as f:
            f.write(caddyfile)
        print(f"✅ Generated Caddyfile for {self.count_domains()} domains")

        # Deploy Caddyfile to primary Pi (lucidia)
        subprocess.run([
            'scp', '/tmp/Caddyfile.all',
            'lucidia:~/blackroad-console/Caddyfile'
        ])
        subprocess.run(['ssh', 'lucidia', 'docker restart blackroad-caddy'])
        print("✅ Deployed Caddyfile to lucidia\n")

        # Show deployment summary
        self.show_summary()

    def count_domains(self):
        total = 0
        for pi_config in self.config['pis'].values():
            total += len(pi_config['domains'])
        return total

    def show_summary(self):
        print("\n📊 Deployment Summary:\n")
        for pi_name, pi_config in self.config['pis'].items():
            print(f"  {pi_name} ({pi_config['ip']}):")
            for domain_config in pi_config['domains']:
                domain = domain_config['domain']
                port = domain_config['port']
                repo = domain_config['repo']
                print(f"    • {domain:40} → :{port} ({repo})")
            print()

    def create_dns_records(self):
        """Generate Cloudflare DNS records for all domains"""
        print("\n📋 DNS Records to Create:\n")

        domains_by_zone = {}
        for pi_config in self.config['pis'].values():
            for domain_config in pi_config['domains']:
                domain = domain_config['domain']
                # Extract zone (e.g., blackroad.io from app.blackroad.io)
                parts = domain.split('.')
                zone = '.'.join(parts[-2:])

                if zone not in domains_by_zone:
                    domains_by_zone[zone] = []
                domains_by_zone[zone].append(domain)

        for zone, domains in domains_by_zone.items():
            print(f"\n  Zone: {zone}")
            for domain in domains:
                subdomain = domain.replace(f'.{zone}', '') if domain != zone else '@'
                print(f"""    {{
      "type": "A",
      "name": "{subdomain}",
      "content": "{self.public_ip}",
      "proxied": false,
      "ttl": 1
    }},""")

if __name__ == '__main__':
    import sys

    deployer = BlackRoadPiDeployer()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'caddyfile':
            print(deployer.generate_caddyfile())
        elif command == 'dns':
            deployer.create_dns_records()
        elif command == 'summary':
            deployer.show_summary()
        elif command == 'github-action':
            if len(sys.argv) > 2:
                action = deployer.generate_github_action(sys.argv[2])
                if action:
                    print(action)
                else:
                    print(f"Repo {sys.argv[2]} not found in configuration")
        else:
            deployer.deploy_all()
    else:
        deployer.deploy_all()
