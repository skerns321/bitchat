#!/usr/bin/env python3
"""
Minimal MCP server test to verify it's working
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

server = Server("minimal-test")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    return ListToolsResult(
        tools=[
            Tool(
                name="test_tool",
                description="A simple test tool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    }
                }
            )
        ]
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "test_tool":
        message = arguments.get("message", "Hello from MCP!")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Test tool received: {message}"
            )]
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="minimal-test",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())