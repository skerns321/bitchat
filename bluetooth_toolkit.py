#!/usr/bin/env python3
"""
Bluetooth Toolkit Launcher
Easy access to all Bluetooth tools for macOS
"""

import sys
import subprocess
import os
from datetime import datetime

class BluetoothToolkit:
    def __init__(self):
        self.tools = {
            '1': {
                'name': 'Basic Bluetooth Scanner',
                'file': 'bluetooth_scanner.py',
                'description': 'Scan for nearby Bluetooth devices',
                'commands': ['python3 bluetooth_scanner.py', 'python3 bluetooth_scanner.py --continuous']
            },
            '2': {
                'name': 'Bitchat Network Monitor',
                'file': 'bitchat_monitor.py',
                'description': 'Monitor mesh network activity',
                'commands': ['python3 bitchat_monitor.py', 'python3 bitchat_monitor.py --continuous', 'python3 bitchat_monitor.py --simulate']
            },
            '3': {
                'name': 'Real-time Activity Monitor',
                'file': 'bt_activity_monitor.py',
                'description': 'Live Bluetooth activity tracking',
                'commands': ['python3 bt_activity_monitor.py --live', 'python3 bt_activity_monitor.py --mesh']
            }
        }
    
    def display_banner(self):
        """Display toolkit banner"""
        print("\n" + "="*80)
        print("🔵 BLUETOOTH TOOLKIT FOR macOS")
        print("="*80)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🖥️  MacBook Bluetooth Development Tools")
        print("="*80)
    
    def display_menu(self):
        """Display main menu"""
        print("\n📋 Available Tools:")
        for key, tool in self.tools.items():
            print(f"   {key}. {tool['name']}")
            print(f"      {tool['description']}")
        print("   q. Quit")
        print("\n🔍 Quick Actions:")
        print("   s. System Bluetooth status")
        print("   h. Show hardware info")
        print("   c. Clear screen")
    
    def get_bluetooth_status(self):
        """Get quick Bluetooth status"""
        print("\n🔍 Checking Bluetooth status...")
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True)
            lines = result.stdout.split('\n')[:20]  # First 20 lines
            for line in lines:
                if 'State:' in line or 'Address:' in line or 'Chipset:' in line:
                    print(f"   {line.strip()}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def show_hardware_info(self):
        """Show Bluetooth hardware information"""
        print("\n🔧 Bluetooth Hardware Information:")
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['Chipset:', 'Firmware:', 'Vendor ID:', 'Product ID:']):
                    print(f"   {line.strip()}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def run_tool(self, tool_key):
        """Run a specific tool"""
        if tool_key not in self.tools:
            print("❌ Invalid tool selection")
            return
        
        tool = self.tools[tool_key]
        print(f"\n🚀 Starting {tool['name']}...")
        
        # Check if file exists
        if not os.path.exists(tool['file']):
            print(f"❌ Tool file {tool['file']} not found!")
            return
        
        # Show available commands
        print(f"\n📋 Available commands for {tool['name']}:")
        for i, cmd in enumerate(tool['commands'], 1):
            print(f"   {i}. {cmd}")
        
        # Get user choice
        try:
            choice = input(f"\nSelect command (1-{len(tool['commands'])}): ").strip()
            cmd_index = int(choice) - 1
            
            if 0 <= cmd_index < len(tool['commands']):
                command = tool['commands'][cmd_index]
                print(f"\n🔄 Running: {command}")
                subprocess.run(command.split())
            else:
                print("❌ Invalid command selection")
        except ValueError:
            print("❌ Invalid input")
        except KeyboardInterrupt:
            print("\n👋 Tool interrupted by user")
    
    def run_interactive(self):
        """Run interactive mode"""
        while True:
            self.display_banner()
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice: ").strip().lower()
                
                if choice == 'q':
                    print("👋 Goodbye!")
                    break
                elif choice == 's':
                    self.get_bluetooth_status()
                    input("\nPress Enter to continue...")
                elif choice == 'h':
                    self.show_hardware_info()
                    input("\nPress Enter to continue...")
                elif choice == 'c':
                    os.system('clear')
                elif choice in self.tools:
                    self.run_tool(choice)
                    input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid choice")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
    
    def run_direct(self, tool_name):
        """Run tool directly from command line"""
        for key, tool in self.tools.items():
            if tool_name.lower() in tool['name'].lower():
                self.run_tool(key)
                return
        print(f"❌ Tool '{tool_name}' not found")

def main():
    toolkit = BluetoothToolkit()
    
    if len(sys.argv) > 1:
        tool_name = ' '.join(sys.argv[1:])
        toolkit.run_direct(tool_name)
    else:
        toolkit.run_interactive()

if __name__ == "__main__":
    main() 