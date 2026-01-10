#!/bin/bash
# BlackRoad Pi Deployment Monitor
# Monitors deployment status and progress across all Pis

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Pi configuration
declare -A PI_IPS=(
    ["lucidia"]="192.168.4.38"
    ["aria"]="192.168.4.64"
    ["alice"]="192.168.4.49"
    ["octavia"]="192.168.4.74"
)

# Domain to Pi/Port mappings from pi-infrastructure.yaml
declare -A DOMAINS=(
    ["blackroad.io"]="lucidia:3000"
    ["carpool.blackroad.io"]="lucidia:3002"
    ["os.blackroad.io"]="lucidia:8081"
    ["app.blackroad.io"]="lucidia:3003"
    ["dashboard.blackroad.io"]="aria:3102"
    ["core.blackroad.systems"]="alice:3200"
)

# Check if a service is running
check_service() {
    local pi=$1
    local port=$2
    local ip=${PI_IPS[$pi]}

    if curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://$ip:$port" | grep -q "200\|404\|301\|302"; then
        echo "up"
    else
        echo "down"
    fi
}

# Check if a container is running
check_container() {
    local pi=$1
    local container=$2
    local ip=${PI_IPS[$pi]}

    if ssh -o ConnectTimeout=2 "$pi" "docker ps --format '{{.Names}}' | grep -q '^${container}$'" 2>/dev/null; then
        echo "running"
    else
        echo "stopped"
    fi
}

# Get container logs
get_logs() {
    local pi=$1
    local container=$2

    ssh "$pi" "docker logs --tail 20 $container 2>&1" 2>/dev/null || echo "Container not found"
}

# Main monitoring function
monitor_deployments() {
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}           🎯 BlackRoad Pi Deployment Status Monitor${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "$(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # Check each domain
    for domain in "${!DOMAINS[@]}"; do
        local target="${DOMAINS[$domain]}"
        local pi="${target%%:*}"
        local port="${target##*:}"
        local ip="${PI_IPS[$pi]}"

        # Check service status
        local status=$(check_service "$pi" "$port")

        # Determine container name from domain
        local container=$(echo "$domain" | sed 's/\.blackroad\.io$//' | sed 's/\.blackroad\.systems$//')

        # Check container status
        local container_status=$(check_container "$pi" "$container")

        # Display status
        echo -e "━━━ ${BLUE}$domain${NC} ━━━"
        echo -e "  Pi:         $pi ($ip:$port)"

        if [ "$status" == "up" ]; then
            echo -e "  HTTP:       ${GREEN}✓ ONLINE${NC}"
        else
            echo -e "  HTTP:       ${RED}✗ OFFLINE${NC}"
        fi

        if [ "$container_status" == "running" ]; then
            echo -e "  Container:  ${GREEN}✓ RUNNING${NC}"
        else
            echo -e "  Container:  ${YELLOW}⏸ STOPPED${NC}"
        fi

        echo ""
    done

    # Check deployment hub (octavia)
    echo -e "${BLUE}━━━ Deployment Hub (octavia) ━━━${NC}"
    if ssh -o ConnectTimeout=2 octavia "echo ok" > /dev/null 2>&1; then
        echo -e "  Status:     ${GREEN}✓ ONLINE${NC}"

        # Check disk usage
        local disk_usage=$(ssh octavia "df -h /media/pi/Extreme\ SSD | tail -1 | awk '{print \$5}'")
        echo -e "  Disk:       $disk_usage used"

        # Check active deployments
        local active=$(ssh octavia "ps aux | grep deploy-to-pi | grep -v grep | wc -l")
        if [ "$active" -gt 0 ]; then
            echo -e "  Deploying:  ${YELLOW}$active active deployment(s)${NC}"
        else
            echo -e "  Deploying:  ${GREEN}idle${NC}"
        fi
    else
        echo -e "  Status:     ${RED}✗ OFFLINE${NC}"
    fi

    echo ""
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
}

# Watch mode
if [ "$1" == "watch" ]; then
    while true; do
        clear
        monitor_deployments
        sleep 5
    done
elif [ "$1" == "logs" ]; then
    # Show logs for a specific domain
    domain="${2:-blackroad.io}"
    target="${DOMAINS[$domain]}"
    pi="${target%%:*}"
    container=$(echo "$domain" | sed 's/\.blackroad\.io$//' | sed 's/\.blackroad\.systems$//')

    echo "📋 Logs for $domain ($pi:$container)"
    echo "════════════════════════════════════════"
    get_logs "$pi" "$container"
elif [ "$1" == "json" ]; then
    # Output JSON for integration
    echo "{"
    echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"services\": ["

    first=true
    for domain in "${!DOMAINS[@]}"; do
        target="${DOMAINS[$domain]}"
        pi="${target%%:*}"
        port="${target##*:}"
        status=$(check_service "$pi" "$port")

        if [ "$first" = false ]; then
            echo ","
        fi
        first=false

        echo -n "    {\"domain\": \"$domain\", \"pi\": \"$pi\", \"port\": $port, \"status\": \"$status\"}"
    done

    echo ""
    echo "  ]"
    echo "}"
else
    # Single run
    monitor_deployments
fi
