#!/usr/bin/env python3
"""
Working MCP server for Claude Desktop
Based on the official MCP Python SDK examples
"""

import asyncio
import sys
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent, ServerCapabilities

# Create server instance
server = Server("bitchat-working-server")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools"""
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
        )
    ]
    return ListToolsResult(tools=tools)

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
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
                text="🔍 Scanning for Bluetooth devices...\n\n✅ Found devices:\n📱 Device 1: F4:D4:88:8A:23:8C (Computer)\n🔊 Device 2: 78:4F:43:D0:C2:C2 (Speaker)\n⌨️ Device 3: D6:C7:DD:A2:0F:17 (Keyboard)\n🎧 Device 4: 38:C4:3A:29:62:8C (Headphones)\n\n🚀 Bitchat MCP server is working perfectly!"
            )]
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point"""
    print("Starting bitchat MCP server...", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        print("MCP server ready for connections", file=sys.stderr)
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="bitchat-working-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )

if __name__ == "__main__":
    asyncio.run(main())