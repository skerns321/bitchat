#!/usr/bin/env python3
"""
Simple MCP server for testing with Claude Desktop
"""

import asyncio
import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("simple-bitchat-server")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools"""
    return ListToolsResult(
        tools=[
            Tool(
                name="hello",
                description="Say hello",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name to greet"
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
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    logger.info(f"Tool called: {name} with args: {arguments}")
    
    if name == "hello":
        name_arg = arguments.get("name", "World")
        return CallToolResult(
            content=[TextContent(
                type="text", 
                text=f"Hello, {name_arg}! This is the bitchat MCP server."
            )]
        )
    elif name == "bluetooth_scan":
        return CallToolResult(
            content=[TextContent(
                type="text",
                text="Scanning for Bluetooth devices...\n✅ Found 4 devices:\n- Device 1: F4:D4:88:8A:23:8C (Computer)\n- Device 2: 78:4F:43:D0:C2:C2 (Speaker)\n- Device 3: D6:C7:DD:A2:0F:17 (Keyboard)\n- Device 4: 38:C4:3A:29:62:8C (Headphones)"
            )]
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point"""
    logger.info("Starting simple MCP server...")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("MCP server started, waiting for connections...")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="simple-bitchat-server",
                    server_version="1.0.0"
                )
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())