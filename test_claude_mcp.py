#!/usr/bin/env python3
"""
Test script to verify Claude Desktop can communicate with our MCP server
"""

import json
import subprocess
import sys
import os

def test_mcp_server_directly():
    """Test MCP server by sending it a direct stdin message"""
    print("🔍 Testing MCP server with direct communication...")
    
    # Create a simple initialize message that Claude Desktop would send
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": False},
                "sampling": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # Write the message to a temp file
    with open("/tmp/mcp_test_input.json", "w") as f:
        json.dump(initialize_request, f)
    
    try:
        # Run our MCP server with the test input
        result = subprocess.run([
            "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat/mcp_env/bin/python",
            "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat/bitchat_mcp_server.py"
        ], 
        input=json.dumps(initialize_request) + "\n",
        text=True,
        capture_output=True,
        timeout=5,
        cwd="/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat"
        )
        
        print(f"✅ MCP server responded")
        print(f"📤 Return code: {result.returncode}")
        print(f"📥 Stdout: {result.stdout[:500]}")
        if result.stderr:
            print(f"⚠️ Stderr: {result.stderr[:500]}")
            
    except subprocess.TimeoutExpired:
        print("⏰ MCP server is running (timeout reached - this is expected)")
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")

def check_claude_desktop_settings():
    """Check if Claude Desktop has MCP settings visible"""
    print("🔍 Checking Claude Desktop configuration...")
    
    # Check if config file exists and is readable
    config_path = "/Users/stephen.kerns/Library/Application Support/Claude/claude_desktop_config.json"
    if os.path.exists(config_path):
        print(f"✅ Config file exists: {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"📋 Config contents:")
            print(json.dumps(config, indent=2))
        except Exception as e:
            print(f"❌ Error reading config: {e}")
    else:
        print(f"❌ Config file not found: {config_path}")

def look_for_mcp_indicators():
    """Look for MCP indicators in Claude Desktop process"""
    print("🔍 Looking for MCP indicators in Claude Desktop processes...")
    
    try:
        # Look for MCP-related process arguments
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        claude_processes = [line for line in result.stdout.split('\n') if 'claude' in line.lower()]
        
        mcp_indicators = []
        for proc in claude_processes:
            if 'mcp' in proc.lower() or 'bitchat' in proc.lower():
                mcp_indicators.append(proc)
        
        if mcp_indicators:
            print("✅ Found MCP-related processes:")
            for indicator in mcp_indicators:
                print(f"   {indicator}")
        else:
            print("❌ No MCP indicators found in processes")
            
    except Exception as e:
        print(f"❌ Error checking processes: {e}")

def check_mcp_server_status():
    """Check if our MCP server process is running"""
    print("🔍 Checking if MCP server is running...")
    
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        bitchat_processes = [line for line in result.stdout.split('\n') if 'bitchat_mcp_server' in line]
        
        if bitchat_processes:
            print("✅ MCP server is running:")
            for proc in bitchat_processes:
                print(f"   {proc}")
        else:
            print("❌ MCP server is not running")
            
    except Exception as e:
        print(f"❌ Error checking MCP server: {e}")

def main():
    print("🔍 Claude Desktop MCP Integration Test")
    print("=" * 50)
    
    check_claude_desktop_settings()
    print()
    
    check_mcp_server_status()
    print()
    
    test_mcp_server_directly()
    print()
    
    look_for_mcp_indicators()
    print()
    
    print("💡 Next steps:")
    print("1. In Claude Desktop, look for a hammer/tools icon in the bottom right")
    print("2. Try asking: 'What MCP servers are available?'")
    print("3. Try asking: 'What tools can I use?'")
    print("4. Check Claude Desktop settings for MCP or Developer options")

if __name__ == "__main__":
    main()