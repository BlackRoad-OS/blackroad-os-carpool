#!/bin/bash
# Quick test script to check if sites are live

echo "Testing BlackRoad Pi deployments..."
echo ""

echo "🌐 os.blackroad.io (192.168.4.38:8081)"
curl -I -s http://192.168.4.38:8081 | head -1
echo ""

echo "🚗 carpool.blackroad.io (192.168.4.38:3002)"
curl -I -s http://192.168.4.38:3002 | head -1
echo ""

echo "✅ If you see 'HTTP/1.1 200 OK' or '404' they're running!"
echo "❌ If you see nothing or connection errors, still building..."
