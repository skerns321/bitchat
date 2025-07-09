# MCP Server Troubleshooting Guide

## Current Status
- ✅ MCP server code is working
- ✅ Configuration file is valid JSON
- ✅ Python environment is set up correctly
- ✅ Server can be imported and starts without errors
- ❓ Claude Desktop is not detecting the MCP server

## Common Issues and Solutions

### 1. Claude Desktop Version
**Check**: Ensure you're using Claude Desktop 0.11.6 or later (you have 0.11.6 ✅)
**Solution**: Update Claude Desktop if needed

### 2. Configuration File Location
**Check**: Config should be at `~/.config/claude-desktop/config.json`
**Current**: `/Users/stephen.kerns/.config/claude-desktop/config.json` ✅

### 3. MCP Server Not Appearing
**Possible causes**:
- Claude Desktop needs to be completely restarted (not just closed)
- MCP feature might need to be enabled in settings
- Server might be crashing on startup

**Solutions**:
1. **Force restart Claude Desktop**:
   - Quit Claude Desktop completely
   - Wait 5 seconds
   - Kill any remaining processes: `pkill -f "Claude"`
   - Restart Claude Desktop

2. **Check for MCP in Claude Desktop**:
   - Look for a MCP or "Model Context Protocol" section in settings
   - Look for connected servers in the interface

3. **Test with minimal server**:
   - I've added a minimal test server to your config
   - This should be easier to debug

### 4. Server Startup Issues
**Check**: Server might be failing to start
**Test**: Run the server manually to see if it starts

### 5. Permission Issues
**Check**: File permissions on config and server files
**Current**: All files have correct permissions ✅

### 6. Claude Desktop Feature Flag
**Issue**: MCP might be behind a feature flag
**Solution**: Check Claude Desktop settings for MCP/developer options

## Next Steps

1. **Restart Claude Desktop completely** (force quit and restart)
2. **Look for MCP indicators** in the Claude Desktop interface
3. **Test with the minimal server** first
4. **Check Console.app** for any error messages when Claude starts
5. **Try asking Claude directly**: "What MCP servers are available?"

## Testing Commands

Once MCP is working, try these:
- "List all available MCP tools"
- "Use the test_tool with message 'hello'"
- "Scan for Bluetooth devices using bitchat tools"
- "Show me the mesh network topology"

## Console.app Debugging

1. Open Console.app
2. Search for "Claude" or "MCP"
3. Look for error messages when starting Claude Desktop
4. Check for permission errors or path issues

## If Still Not Working

1. **Check Claude Desktop documentation** for MCP setup
2. **Verify MCP feature is enabled** in your version
3. **Try a different MCP server** (like the minimal test)
4. **Check online forums** for similar issues
5. **Contact Claude support** if needed

The setup looks technically correct, so the issue is likely either:
- Need to fully restart Claude Desktop
- MCP feature needs to be enabled
- Version compatibility issue