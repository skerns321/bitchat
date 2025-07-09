#!/usr/bin/env python3
"""
Basic MCP server using direct method implementation instead of decorators
"""

import asyncio
import sys
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, ListToolsResult, CallToolResult, TextContent, 
    ServerCapabilities, Resource, ListResourcesResult, 
    ReadResourceResult, TextResourceContents
)

class BasicMCPServer:
    def __init__(self):
        self.server = Server("bitchat-basic-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all MCP handlers"""
        
        # Tools
        self.server.list_tools()(self.handle_list_tools)
        self.server.call_tool()(self.handle_call_tool)
        
        # Resources
        self.server.list_resources()(self.handle_list_resources)
        self.server.read_resource()(self.handle_read_resource)
    
    async def handle_list_tools(self) -> ListToolsResult:
        """Handle list_tools request"""
        print("handle_list_tools called", file=sys.stderr)
        
        try:
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
                    name="mesh_monitor",
                    description="Monitor mesh network",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mode": {
                                "type": "string",
                                "enum": ["scan", "simulate"],
                                "default": "scan"
                            }
                        }
                    }
                )
            ]
            
            result = ListToolsResult(tools=tools)
            print(f"Returning tools result: {result}", file=sys.stderr)
            return result
            
        except Exception as e:
            print(f"Error in handle_list_tools: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    
    async def handle_call_tool(self, name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle call_tool request"""
        print(f"handle_call_tool called: {name} with {arguments}", file=sys.stderr)
        
        try:
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
            
            elif name == "mesh_monitor":
                mode = arguments.get("mode", "scan")
                result = {
                    "mode": mode,
                    "nodes_found": 3,
                    "status": "active",
                    "timestamp": datetime.now().isoformat()
                }
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"📡 Mesh network monitoring: {json.dumps(result, indent=2)}"
                    )]
                )
            
            else:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
                )
                
        except Exception as e:
            print(f"Error in handle_call_tool: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
            )
    
    async def handle_list_resources(self) -> ListResourcesResult:
        """Handle list_resources request"""
        print("handle_list_resources called", file=sys.stderr)
        
        try:
            resources = [
                Resource(
                    uri="mesh://network/status",
                    name="Network Status",
                    description="Current mesh network status",
                    mimeType="application/json"
                ),
                Resource(
                    uri="protocol://spec",
                    name="Protocol Specification",
                    description="Bitchat protocol specification",
                    mimeType="text/markdown"
                )
            ]
            
            result = ListResourcesResult(resources=resources)
            print(f"Returning resources result: {result}", file=sys.stderr)
            return result
            
        except Exception as e:
            print(f"Error in handle_list_resources: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    
    async def handle_read_resource(self, uri: str) -> ReadResourceResult:
        """Handle read_resource request"""
        print(f"handle_read_resource called with uri: {uri}", file=sys.stderr)
        
        try:
            if uri == "mesh://network/status":
                status = {
                    "nodes": 3,
                    "connections": 2,
                    "status": "active",
                    "timestamp": datetime.now().isoformat()
                }
                
                return ReadResourceResult(
                    contents=[TextResourceContents(
                        type="text",
                        text=json.dumps(status, indent=2),
                        uri=uri
                    )]
                )
            
            elif uri == "protocol://spec":
                spec = """
# Bitchat Protocol Specification

## Overview
Bitchat uses a binary protocol for mesh networking communication.

## Message Types
- ANNOUNCE: Node announcement
- MESSAGE: User message
- KEY_EXCHANGE: Cryptographic key exchange
"""
                
                return ReadResourceResult(
                    contents=[TextResourceContents(
                        type="text",
                        text=spec,
                        uri=uri
                    )]
                )
            
            else:
                return ReadResourceResult(
                    contents=[TextResourceContents(
                        type="text",
                        text=f"Unknown resource: {uri}",
                        uri=uri
                    )]
                )
                
        except Exception as e:
            print(f"Error in handle_read_resource: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise

async def main():
    """Main entry point"""
    print("Starting basic MCP server...", file=sys.stderr)
    
    try:
        mcp_server = BasicMCPServer()
        
        async with stdio_server() as (read_stream, write_stream):
            print("Basic MCP server ready for connections", file=sys.stderr)
            await mcp_server.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="bitchat-basic-server",
                    server_version="1.0.0",
                    capabilities=ServerCapabilities()
                )
            )
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())