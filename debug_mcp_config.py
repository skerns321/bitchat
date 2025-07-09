#!/usr/bin/env python3
"""
Debug MCP configuration issues
"""

import json
import os
import subprocess
import sys

def check_config_file():
    """Check if config file exists and is valid"""
    config_path = "/Users/stephen.kerns/.config/claude-desktop/config.json"
    print(f"🔍 Checking config file: {config_path}")
    
    if not os.path.exists(config_path):
        print("❌ Config file does not exist")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✅ Config file is valid JSON")
        print(f"📋 Config contents:")
        print(json.dumps(config, indent=2))
        return True
    except Exception as e:
        print(f"❌ Config file is invalid: {e}")
        return False

def check_python_path():
    """Check if Python path is correct"""
    python_path = "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat/mcp_env/bin/python"
    print(f"🔍 Checking Python path: {python_path}")
    
    if not os.path.exists(python_path):
        print("❌ Python path does not exist")
        return False
    
    try:
        result = subprocess.run([python_path, "--version"], capture_output=True, text=True)
        print(f"✅ Python version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python path error: {e}")
        return False

def check_mcp_server():
    """Check if MCP server can be imported"""
    server_path = "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat/bitchat_mcp_server.py"
    print(f"🔍 Checking MCP server: {server_path}")
    
    if not os.path.exists(server_path):
        print("❌ MCP server file does not exist")
        return False
    
    try:
        python_path = "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat/mcp_env/bin/python"
        result = subprocess.run([
            python_path, 
            "-c", 
            "import sys; sys.path.insert(0, '/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat'); import bitchat_mcp_server; print('✅ MCP server imports successfully')"
        ], capture_output=True, text=True, cwd="/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat")
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(f"❌ MCP server import failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ MCP server check error: {e}")
        return False

def check_claude_desktop_logs():
    """Check for Claude Desktop logs"""
    print("🔍 Checking for Claude Desktop logs...")
    
    # Common log locations
    log_paths = [
        "/Users/stephen.kerns/Library/Logs/Claude/",
        "/Users/stephen.kerns/Library/Application Support/Claude/",
        "/Users/stephen.kerns/Library/Logs/",
    ]
    
    for path in log_paths:
        if os.path.exists(path):
            print(f"📁 Found log directory: {path}")
            try:
                files = os.listdir(path)
                for file in files:
                    if 'claude' in file.lower() or 'mcp' in file.lower():
                        print(f"📄 Log file: {os.path.join(path, file)}")
            except Exception as e:
                print(f"❌ Error reading log directory: {e}")
    
    print("💡 To check Claude Desktop logs, look in Console.app for 'Claude' messages")

def create_simple_config():
    """Create a simpler config for testing"""
    print("🔧 Creating simplified config...")
    
    simple_config = {
        "mcpServers": {
            "bitchat": {
                "command": "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat/mcp_env/bin/python",
                "args": ["bitchat_mcp_server.py"],
                "cwd": "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat"
            }
        }
    }
    
    config_path = "/Users/stephen.kerns/.config/claude-desktop/config.json"
    try:
        with open(config_path, 'w') as f:
            json.dump(simple_config, f, indent=2)
        print("✅ Created simplified config")
        print(json.dumps(simple_config, indent=2))
    except Exception as e:
        print(f"❌ Error creating config: {e}")

def main():
    print("🔍 MCP Configuration Debugging")
    print("=" * 40)
    
    check_config_file()
    print()
    check_python_path()
    print()
    check_mcp_server()
    print()
    check_claude_desktop_logs()
    print()
    create_simple_config()
    print()
    
    print("🔄 Next steps:")
    print("1. Restart Claude Desktop completely")
    print("2. Check Console.app for Claude Desktop error messages")
    print("3. Try using the MCP server with a simple command")
    print("4. If it still doesn't work, check Claude Desktop settings for MCP")

if __name__ == "__main__":
    main()