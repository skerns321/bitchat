#!/usr/bin/env python3
"""
Minimal MCP server to test the issue
"""

import asyncio
import sys
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent, ServerCapabilities

# Create server instance
server = Server("minimal-test-server")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools"""
    print("list_tools called", file=sys.stderr)
    tool = Tool(
        name="test",
        description="Test tool",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
    result = ListToolsResult(tools=[tool])
    print(f"Returning: {result}", file=sys.stderr)
    return result

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    print(f"call_tool called with name={name}, arguments={arguments}", file=sys.stderr)
    return CallToolResult(
        content=[TextContent(type="text", text=f"Test tool {name} called")]
    )

async def main():
    """Main entry point"""
    print("Starting minimal test server...", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        print("Server ready for connections", file=sys.stderr)
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="minimal-test-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )

if __name__ == "__main__":
    asyncio.run(main())