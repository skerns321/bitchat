# Bitchat MCP Server Examples

This document shows how to use the Bitchat MCP server with AI assistants.

## Setup

1. Run the setup script:
```bash
./setup_mcp.sh
```

2. Add the MCP server to your Claude Desktop config (`~/.config/claude-desktop/config.json`):
```json
{
  "mcpServers": {
    "bitchat": {
      "command": "python3",
      "args": ["bitchat_mcp_server.py"],
      "cwd": "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat",
      "env": {
        "PYTHONPATH": "/Users/stephen.kerns/Desktop/NAMTAB -TOOLS/bitchat"
      }
    }
  }
}
```

3. Restart Claude Desktop

## Available Tools

### 1. Bluetooth Scanning
```
Tool: bluetooth_scan
Description: Scan for nearby Bluetooth devices
Parameters:
  - continuous: boolean (default: false)
```

**Example usage:**
- "Scan for nearby Bluetooth devices"
- "Start continuous Bluetooth scanning"

### 2. Mesh Network Monitoring
```
Tool: mesh_monitor
Description: Monitor bitchat mesh network activity
Parameters:
  - mode: "scan" | "simulate" | "continuous" (default: "scan")
  - duration: integer (default: 60)
```

**Example usage:**
- "Monitor the mesh network activity"
- "Simulate mesh network behavior"
- "Start continuous mesh monitoring for 120 seconds"

### 3. Packet Analysis
```
Tool: analyze_packet
Description: Analyze bitchat protocol packet
Parameters:
  - packet_data: string (base64 encoded)
  - packet_type: "binary" | "json" | "hex" (default: "binary")
```

**Example usage:**
- "Analyze this packet data: SGVsbG8gV29ybGQ="
- "Help me understand the structure of this binary packet"

### 4. Mesh Network Simulation
```
Tool: simulate_mesh_network
Description: Simulate mesh network behavior
Parameters:
  - nodes: integer (default: 5)
  - topology: "random" | "grid" | "ring" | "star" (default: "random")
  - message_count: integer (default: 100)
```

**Example usage:**
- "Simulate a mesh network with 10 nodes"
- "Test message routing in a star topology"
- "Run performance simulation with 1000 messages"

### 5. Protocol Validation
```
Tool: validate_protocol
Description: Validate bitchat protocol implementation
Parameters:
  - code_path: string (required)
  - protocol_version: string (default: "1.0")
```

**Example usage:**
- "Validate the protocol implementation in BitchatProtocol.swift"
- "Check if this code follows the bitchat protocol specification"

### 6. Cryptographic Analysis
```
Tool: analyze_crypto
Description: Analyze cryptographic implementation
Parameters:
  - crypto_code: string (required)
  - analysis_type: "key_exchange" | "encryption" | "signature" | "all" (default: "all")
```

**Example usage:**
- "Analyze the security of this encryption code"
- "Review the key exchange implementation"

## Available Resources

### 1. Network Topology
```
Resource: mesh://network/topology
Description: Current mesh network topology and connections
```

### 2. Network Peers
```
Resource: mesh://network/peers
Description: List of discovered mesh network peers
```

### 3. Network Activity
```
Resource: mesh://network/activity
Description: Real-time network activity log
```

### 4. Protocol Specification
```
Resource: protocol://binary/spec
Description: Bitchat binary protocol specification
```

### 5. Encryption Details
```
Resource: protocol://encryption/details
Description: Cryptographic implementation details
```

### 6. Discovered Devices
```
Resource: bluetooth://devices/discovered
Description: Recently discovered Bluetooth devices
```

## Available Prompts

### 1. Network Health Analysis
```
Prompt: analyze_network_health
Parameters:
  - focus_area: string (optional)
```

**Example usage:**
- "Analyze the current mesh network health"
- "Focus on connection stability in the network analysis"

### 2. Protocol Debugging
```
Prompt: debug_protocol_issue
Parameters:
  - issue_description: string (required)
  - error_logs: string (optional)
```

**Example usage:**
- "Help me debug a message routing issue"
- "I'm having trouble with key exchange - can you help?"

### 3. Security Audit
```
Prompt: security_audit
Parameters:
  - component: string (optional)
```

**Example usage:**
- "Perform a security audit of the encryption system"
- "Review the overall security of the protocol"

### 4. Performance Optimization
```
Prompt: optimize_performance
Parameters:
  - performance_data: string (optional)
```

**Example usage:**
- "Suggest performance improvements for the mesh network"
- "How can I optimize message throughput?"

## Usage Examples

### Basic Network Analysis
```
User: "What devices are nearby and how healthy is the mesh network?"

AI will:
1. Use bluetooth_scan to find nearby devices
2. Use mesh_monitor to check network activity
3. Access mesh://network/topology for current topology
4. Provide comprehensive network health analysis
```

### Protocol Debugging
```
User: "I'm having trouble with message delivery in my mesh network"

AI will:
1. Use mesh_monitor to analyze current network state
2. Access mesh://network/activity for recent activity
3. Use analyze_packet if packet data is provided
4. Suggest debugging steps and solutions
```

### Security Review
```
User: "Can you review the security of my encryption implementation?"

AI will:
1. Use analyze_crypto to analyze the code
2. Access protocol://encryption/details for specifications
3. Check for common vulnerabilities
4. Provide security recommendations
```

### Performance Testing
```
User: "Test the performance of a 20-node mesh network"

AI will:
1. Use simulate_mesh_network with 20 nodes
2. Analyze delivery rates and hop counts
3. Suggest optimizations
4. Provide performance report
```

## Advanced Use Cases

### 1. Continuous Monitoring
Set up continuous monitoring of mesh network health:
```
"Start continuous mesh monitoring and alert me to any issues"
```

### 2. Protocol Compliance Testing
Validate that code follows the bitchat protocol:
```
"Validate that all my Swift files follow the bitchat protocol specification"
```

### 3. Security Hardening
Comprehensive security analysis:
```
"Perform a complete security audit of the bitchat implementation"
```

### 4. Performance Optimization
Identify and fix performance bottlenecks:
```
"Analyze current network performance and suggest specific optimizations"
```

## Tips for Best Results

1. **Be specific**: Provide details about what you want to analyze or debug
2. **Use prompts**: The specialized prompts provide better context for complex analysis
3. **Combine tools**: Use multiple tools together for comprehensive analysis
4. **Provide context**: Include error messages, code snippets, or performance data
5. **Follow up**: Ask follow-up questions to drill down into specific issues

## Troubleshooting

If the MCP server isn't working:

1. Check that Python dependencies are installed:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Verify the server can start:
   ```bash
   python3 bitchat_mcp_server.py
   ```

3. Check Claude Desktop logs for errors

4. Ensure the config path is correct in your Claude Desktop config

5. Try restarting Claude Desktop after config changes