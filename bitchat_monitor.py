#!/usr/bin/env python3
"""
Bitchat Network Monitor
Monitors network activity and Bluetooth connections for bitchat debugging
"""

import subprocess
import json
import time
import sys
import socket
import threading
from datetime import datetime
from collections import defaultdict

class BitchatMonitor:
    def __init__(self):
        self.bluetooth_devices = {}
        self.network_stats = defaultdict(int)
        self.running = False
        
    def get_bluetooth_connections(self):
        """Get active Bluetooth connections"""
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Error getting Bluetooth connections: {e}")
            return None
    
    def get_network_activity(self):
        """Monitor network activity"""
        try:
            result = subprocess.run(['netstat', '-i'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Error getting network activity: {e}")
            return None
    
    def parse_bluetooth_status(self, bt_info):
        """Parse Bluetooth connection status"""
        devices = []
        if not bt_info:
            return devices
            
        lines = bt_info.split('\n')
        current_device = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.endswith(':') and not line.startswith('Bluetooth'):
                device_name = line[:-1].strip()
                if device_name and device_name not in ['Not Connected', 'Connected']:
                    if current_device:
                        devices.append(current_device)
                    current_device = {'name': device_name, 'timestamp': datetime.now()}
            elif ':' in line and current_device:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key == 'Address':
                    current_device['address'] = value
                elif key == 'State':
                    current_device['state'] = value
                    
        if current_device:
            devices.append(current_device)
            
        return devices
    
    def monitor_mesh_activity(self):
        """Monitor for potential mesh network activity"""
        print("🕸️  Monitoring mesh network activity...")
        
        # Check for processes that might be bitchat related
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = result.stdout
            
            bitchat_processes = [line for line in processes.split('\n') 
                               if 'bitchat' in line.lower() or 'bluetooth' in line.lower()]
            
            if bitchat_processes:
                print("🔍 Found relevant processes:")
                for proc in bitchat_processes:
                    print(f"   {proc}")
            
        except Exception as e:
            print(f"Error monitoring processes: {e}")
    
    def display_status(self):
        """Display current monitoring status"""
        print("\n" + "="*80)
        print(f"🔗 BITCHAT NETWORK MONITOR - {datetime.now().strftime('%H:%M:%S')}")
        print("="*80)
        
        # Bluetooth status
        bt_info = self.get_bluetooth_connections()
        devices = self.parse_bluetooth_status(bt_info)
        
        print(f"\n📡 Bluetooth Status:")
        if devices:
            for device in devices:
                status = device.get('state', 'Unknown')
                print(f"   🔵 {device['name']} ({device.get('address', 'No address')}): {status}")
        else:
            print("   No Bluetooth devices found")
        
        # Network activity
        net_info = self.get_network_activity()
        if net_info:
            print(f"\n🌐 Network Interfaces:")
            lines = net_info.split('\n')[1:6]  # First few lines
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        
        # Mesh activity
        self.monitor_mesh_activity()
        
        print(f"\n📊 Monitoring Stats:")
        print(f"   Scans completed: {self.network_stats['scans']}")
        print(f"   Devices tracked: {len(self.bluetooth_devices)}")
        
        self.network_stats['scans'] += 1
    
    def simulate_mesh_node(self):
        """Simulate a mesh node for testing"""
        print("\n🤖 Simulating mesh node behavior...")
        
        # Create a simple UDP socket to demonstrate mesh-like behavior
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('localhost', 0))  # Bind to any available port
            port = sock.getsockname()[1]
            print(f"   📡 Mesh node listening on port {port}")
            
            # Send a test beacon
            beacon_msg = f"bitchat-beacon-{datetime.now().strftime('%H%M%S')}"
            sock.sendto(beacon_msg.encode(), ('localhost', port))
            print(f"   📤 Sent beacon: {beacon_msg}")
            
            sock.close()
            print("   ✅ Mesh simulation complete")
            
        except Exception as e:
            print(f"   ❌ Error simulating mesh node: {e}")
    
    def run_continuous_monitoring(self, interval=10):
        """Run continuous monitoring"""
        print("🚀 Starting bitchat network monitoring...")
        print("Press Ctrl+C to stop")
        
        self.running = True
        try:
            while self.running:
                self.display_status()
                
                # Occasionally simulate mesh activity
                if self.network_stats['scans'] % 3 == 0:
                    self.simulate_mesh_node()
                
                print(f"\n⏰ Next scan in {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped by user")
            self.running = False
    
    def run_single_scan(self):
        """Run a single monitoring scan"""
        print("🔍 Running single network scan...")
        self.display_status()
        self.simulate_mesh_node()

def main():
    monitor = BitchatMonitor()
    
    print("🔗 Bitchat Network Monitor")
    print("=" * 30)
    print("1. Single scan")
    print("2. Continuous monitoring")
    print("3. Simulate mesh activity")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--continuous':
            monitor.run_continuous_monitoring()
        elif sys.argv[1] == '--simulate':
            monitor.simulate_mesh_node()
        else:
            monitor.run_single_scan()
    else:
        choice = input("\nEnter choice (1-3): ")
        if choice == '1':
            monitor.run_single_scan()
        elif choice == '2':
            monitor.run_continuous_monitoring()
        elif choice == '3':
            monitor.simulate_mesh_node()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main() 