#!/bin/bash

echo "🔧 Setting up Bitchat MCP Server..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make the MCP server executable
chmod +x bitchat_mcp_server.py

# Test the server
echo "🧪 Testing MCP server..."
python3 -c "
import asyncio
import sys
sys.path.append('.')
from bitchat_mcp_server import BitchatMCPServer

async def test():
    server = BitchatMCPServer()
    print('✅ MCP server initialized successfully')
    print(f'📊 Tools available: {len(server.server._tools) if hasattr(server.server, \"_tools\") else \"Unknown\"}')
    print(f'📚 Resources available: {len(server.server._resources) if hasattr(server.server, \"_resources\") else \"Unknown\"}')
    print(f'💬 Prompts available: {len(server.server._prompts) if hasattr(server.server, \"_prompts\") else \"Unknown\"}')

asyncio.run(test())
"

echo ""
echo "🚀 Setup complete!"
echo ""
echo "To use the MCP server:"
echo "1. Add the following to your Claude Desktop config:"
echo "   ~/.config/claude-desktop/config.json"
echo ""
echo "2. Copy the contents of mcp_server_config.json to your config"
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "4. The server will provide these capabilities:"
echo "   📡 bluetooth_scan - Scan for Bluetooth devices"
echo "   🕸️  mesh_monitor - Monitor mesh network activity"
echo "   📊 analyze_packet - Analyze protocol packets"
echo "   🎯 simulate_mesh_network - Simulate mesh behavior"
echo "   🔍 validate_protocol - Validate protocol implementations"
echo "   🔒 analyze_crypto - Analyze cryptographic code"
echo ""
echo "5. Plus resources for network topology, peers, and activity"
echo "6. Plus prompts for network health analysis and debugging"