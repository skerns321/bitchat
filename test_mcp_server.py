#!/usr/bin/env python3
"""
Test script for Bitchat MCP Server
"""

import asyncio
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
try:
    from bitchat_mcp_server import BitchatMCPServer
    print("✅ Successfully imported BitchatMCPServer")
except ImportError as e:
    print(f"❌ Failed to import BitchatMCPServer: {e}")
    sys.exit(1)

async def test_server_initialization():
    """Test server initialization"""
    print("\n🔧 Testing server initialization...")
    
    try:
        server = BitchatMCPServer()
        print("✅ Server initialized successfully")
        return server
    except Exception as e:
        print(f"❌ Server initialization failed: {e}")
        return None

async def test_tools(server):
    """Test MCP tools"""
    print("\n🔧 Testing MCP tools...")
    
    # Test bluetooth_scan
    try:
        result = await server.handle_bluetooth_scan({"continuous": False})
        print("✅ bluetooth_scan tool works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ bluetooth_scan tool failed: {e}")
    
    # Test mesh_monitor
    try:
        result = await server.handle_mesh_monitor({"mode": "simulate"})
        print("✅ mesh_monitor tool works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ mesh_monitor tool failed: {e}")
    
    # Test analyze_packet
    try:
        import base64
        test_data = base64.b64encode(b"Hello World").decode()
        result = await server.handle_analyze_packet({"packet_data": test_data})
        print("✅ analyze_packet tool works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ analyze_packet tool failed: {e}")
    
    # Test simulate_mesh_network
    try:
        result = await server.handle_simulate_mesh_network({"nodes": 3})
        print("✅ simulate_mesh_network tool works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ simulate_mesh_network tool failed: {e}")

async def test_resources(server):
    """Test MCP resources"""
    print("\n🔧 Testing MCP resources...")
    
    # Test network topology
    try:
        result = await server.get_network_topology()
        print("✅ network topology resource works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ network topology resource failed: {e}")
    
    # Test network peers
    try:
        result = await server.get_network_peers()
        print("✅ network peers resource works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ network peers resource failed: {e}")
    
    # Test protocol spec
    try:
        result = await server.get_protocol_spec()
        print("✅ protocol spec resource works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ protocol spec resource failed: {e}")

async def test_prompts(server):
    """Test MCP prompts"""
    print("\n🔧 Testing MCP prompts...")
    
    # Test network health prompt
    try:
        result = await server.get_network_health_prompt({"focus_area": "connectivity"})
        print("✅ network health prompt works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ network health prompt failed: {e}")
    
    # Test debug protocol prompt
    try:
        result = await server.get_debug_protocol_prompt({
            "issue_description": "Test issue",
            "error_logs": "Test logs"
        })
        print("✅ debug protocol prompt works")
        print(f"   Result type: {type(result)}")
    except Exception as e:
        print(f"❌ debug protocol prompt failed: {e}")

async def test_integration():
    """Test integration with existing tools"""
    print("\n🔧 Testing integration with existing tools...")
    
    try:
        from bluetooth_scanner import BluetoothScanner
        scanner = BluetoothScanner()
        print("✅ BluetoothScanner integration works")
    except Exception as e:
        print(f"❌ BluetoothScanner integration failed: {e}")
    
    try:
        from bitchat_monitor import BitchatMonitor
        monitor = BitchatMonitor()
        print("✅ BitchatMonitor integration works")
    except Exception as e:
        print(f"❌ BitchatMonitor integration failed: {e}")
    
    try:
        from bt_activity_monitor import BluetoothActivityMonitor
        activity_monitor = BluetoothActivityMonitor()
        print("✅ BluetoothActivityMonitor integration works")
    except Exception as e:
        print(f"❌ BluetoothActivityMonitor integration failed: {e}")

async def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 Starting Bitchat MCP Server Test Suite")
    print("=" * 50)
    
    # Test server initialization
    server = await test_server_initialization()
    if not server:
        print("❌ Cannot continue tests without server")
        return
    
    # Test tools
    await test_tools(server)
    
    # Test resources
    await test_resources(server)
    
    # Test prompts
    await test_prompts(server)
    
    # Test integration
    await test_integration()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("\nNext steps:")
    print("1. Add the MCP server to your Claude Desktop config")
    print("2. Restart Claude Desktop")
    print("3. Test with actual AI interactions")
    print("\nConfig location: ~/.config/claude-desktop/config.json")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())