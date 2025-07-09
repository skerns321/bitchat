#!/usr/bin/env python3
"""
Test MCP server connection and functionality
"""

import asyncio
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bitchat_mcp_server import BitchatMCPServer

async def test_mcp_connection():
    """Test MCP server as if Claude Desktop is connecting"""
    print("🔗 Testing MCP server connection...")
    
    try:
        # Initialize server
        server = BitchatMCPServer()
        print("✅ Server initialized")
        
        # Test tool listing
        tools_result = await server.server.list_tools()
        print(f"✅ Tools listed: {len(tools_result.tools)} tools available")
        for tool in tools_result.tools:
            print(f"   📧 {tool.name}: {tool.description}")
        
        # Test resource listing
        resources_result = await server.server.list_resources()
        print(f"✅ Resources listed: {len(resources_result.resources)} resources available")
        for resource in resources_result.resources:
            print(f"   📚 {resource.name}: {resource.description}")
        
        # Test prompt listing
        prompts_result = await server.server.list_prompts()
        print(f"✅ Prompts listed: {len(prompts_result.prompts)} prompts available")
        for prompt in prompts_result.prompts:
            print(f"   💬 {prompt.name}: {prompt.description}")
        
        # Test a simple tool call
        print("\n🧪 Testing tool call...")
        result = await server.server.call_tool("bluetooth_scan", {"continuous": False})
        print("✅ Tool call successful")
        print(f"   Result has {len(result.content)} content items")
        
        # Test a resource read
        print("\n🧪 Testing resource read...")
        result = await server.server.read_resource("mesh://network/topology")
        print("✅ Resource read successful")
        print(f"   Resource has {len(result.contents)} content items")
        
        print("\n🎉 All MCP server tests passed!")
        print("The server is ready for Claude Desktop connection.")
        
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())