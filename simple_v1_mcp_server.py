#!/usr/bin/env python3
"""
Simple MCP server for MCP SDK v1.0.0
"""

import asyncio
import sys
import json
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

# Create server instance
server = Server("bitchat-simple-v1")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools"""
    print("list_tools called", file=sys.stderr)
    
    tools = [
        Tool(
            name="hello",
            description="Say hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet",
                        "default": "World"
                    }
                }
            }
        ),
        Tool(
            name="bluetooth_scan",
            description="Scan for Bluetooth devices",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="mesh_status",
            description="Get mesh network status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]
    
    print(f"Returning {len(tools)} tools", file=sys.stderr)
    return ListToolsResult(tools=tools)

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    print(f"call_tool called with name={name}, arguments={arguments}", file=sys.stderr)
    
    if name == "hello":
        name_arg = arguments.get("name", "World")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Hello, {name_arg}! 🎉 The bitchat MCP server is working!"
            )]
        )
    
    elif name == "bluetooth_scan":
        return CallToolResult(
            content=[TextContent(
                type="text",
                text="🔍 Scanning for Bluetooth devices...\n\n✅ Found devices:\n📱 Device 1: F4:D4:88:8A:23:8C (Computer)\n🔊 Device 2: 78:4F:43:D0:C2:C2 (Speaker)\n⌨️ Device 3: D6:C7:DD:A2:0F:17 (Keyboard)\n🎧 Device 4: 38:C4:3A:29:62:8C (Headphones)\n\n🚀 Bitchat MCP server is working!"
            )]
        )
    
    elif name == "mesh_status":
        status = {
            "nodes": 3,
            "connections": 2,
            "health": "good",
            "last_updated": datetime.now().isoformat()
        }
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"📡 Mesh network status:\n\n{json.dumps(status, indent=2)}"
            )]
        )
    
    else:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
        )

async def main():
    """Main entry point"""
    print("Starting simple v1 MCP server...", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        print("MCP server ready for connections", file=sys.stderr)
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())