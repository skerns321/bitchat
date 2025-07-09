#!/usr/bin/env python3
"""
Real-time Bluetooth Activity Monitor
Tracks Bluetooth connections, disconnections, and activity in real-time
"""

import subprocess
import time
import sys
import json
import threading
from datetime import datetime
from collections import defaultdict, deque

class BluetoothActivityMonitor:
    def __init__(self):
        self.device_history = defaultdict(deque)
        self.connection_events = deque(maxlen=100)
        self.activity_stats = defaultdict(int)
        self.running = False
        self.last_scan_devices = set()
        
    def get_bluetooth_info(self):
        """Get detailed Bluetooth information"""
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType', '-json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return None
        except Exception as e:
            print(f"Error getting Bluetooth info: {e}")
            return None
    
    def parse_devices(self, bt_data):
        """Parse device information from Bluetooth data"""
        devices = []
        try:
            if bt_data and 'SPBluetoothDataType' in bt_data:
                for item in bt_data['SPBluetoothDataType']:
                    if 'device_title' in item:
                        for device_name, device_info in item.items():
                            if isinstance(device_info, dict) and 'device_address' in device_info:
                                devices.append({
                                    'name': device_name,
                                    'address': device_info.get('device_address', 'Unknown'),
                                    'connected': device_info.get('device_isConnected', 'No') == 'Yes',
                                    'type': device_info.get('device_minorType', 'Unknown'),
                                    'rssi': device_info.get('device_rssi', 'N/A'),
                                    'timestamp': datetime.now()
                                })
        except Exception as e:
            print(f"Error parsing devices: {e}")
        
        return devices
    
    def detect_activity(self, current_devices):
        """Detect connection/disconnection events"""
        current_addresses = {d['address'] for d in current_devices}
        
        # Check for new connections
        new_connections = current_addresses - self.last_scan_devices
        for address in new_connections:
            device = next((d for d in current_devices if d['address'] == address), None)
            if device:
                event = {
                    'type': 'connection',
                    'device': device,
                    'timestamp': datetime.now()
                }
                self.connection_events.append(event)
                self.activity_stats['connections'] += 1
                print(f"🔗 NEW CONNECTION: {device['name']} ({address})")
        
        # Check for disconnections
        disconnections = self.last_scan_devices - current_addresses
        for address in disconnections:
            event = {
                'type': 'disconnection',
                'address': address,
                'timestamp': datetime.now()
            }
            self.connection_events.append(event)
            self.activity_stats['disconnections'] += 1
            print(f"🔌 DISCONNECTION: {address}")
        
        self.last_scan_devices = current_addresses
    
    def monitor_signal_strength(self, devices):
        """Monitor signal strength changes"""
        for device in devices:
            if device['rssi'] != 'N/A':
                address = device['address']
                rssi = device['rssi']
                
                # Store RSSI history
                self.device_history[address].append({
                    'rssi': rssi,
                    'timestamp': datetime.now()
                })
                
                # Keep only last 10 readings
                if len(self.device_history[address]) > 10:
                    self.device_history[address].popleft()
    
    def display_live_status(self, devices):
        """Display live status with colors and activity"""
        print("\n" + "="*90)
        print(f"📡 LIVE BLUETOOTH ACTIVITY MONITOR - {datetime.now().strftime('%H:%M:%S')}")
        print("="*90)
        
        # Current devices
        print(f"\n🔵 Active Devices ({len(devices)}):")
        for i, device in enumerate(devices, 1):
            status = "🟢 Connected" if device['connected'] else "🔴 Disconnected"
            rssi_info = f"RSSI: {device['rssi']}" if device['rssi'] != 'N/A' else ""
            print(f"   {i}. {device['name']}")
            print(f"      📍 {device['address']} | {device['type']} | {status} | {rssi_info}")
        
        # Recent activity
        print(f"\n⚡ Recent Activity:")
        recent_events = list(self.connection_events)[-5:]  # Last 5 events
        if recent_events:
            for event in recent_events:
                timestamp = event['timestamp'].strftime('%H:%M:%S')
                if event['type'] == 'connection':
                    print(f"   🔗 {timestamp} - Connected: {event['device']['name']}")
                else:
                    print(f"   🔌 {timestamp} - Disconnected: {event['address']}")
        else:
            print("   No recent activity")
        
        # Activity statistics
        print(f"\n📊 Session Statistics:")
        print(f"   Total scans: {self.activity_stats['scans']}")
        print(f"   Connections detected: {self.activity_stats['connections']}")
        print(f"   Disconnections detected: {self.activity_stats['disconnections']}")
        print(f"   Devices tracked: {len(self.device_history)}")
        
        # Signal strength trends
        print(f"\n📶 Signal Strength Trends:")
        for address, history in list(self.device_history.items())[-3:]:  # Last 3 devices
            if history:
                recent_rssi = [h['rssi'] for h in history if isinstance(h['rssi'], (int, float))]
                if recent_rssi:
                    avg_rssi = sum(recent_rssi) / len(recent_rssi)
                    trend = "📈" if len(recent_rssi) > 1 and recent_rssi[-1] > recent_rssi[0] else "📉"
                    device_name = next((d['name'] for d in devices if d['address'] == address), address)
                    print(f"   {trend} {device_name}: Avg RSSI {avg_rssi:.1f} dBm")
        
        self.activity_stats['scans'] += 1
    
    def simulate_mesh_discovery(self):
        """Simulate discovering mesh network peers"""
        print(f"\n🕸️  Simulating mesh peer discovery...")
        
        # Create fake mesh peers
        mesh_peers = [
            {'id': 'peer-001', 'hops': 1, 'signal': -45},
            {'id': 'peer-002', 'hops': 2, 'signal': -67},
            {'id': 'peer-003', 'hops': 1, 'signal': -52}
        ]
        
        for peer in mesh_peers:
            print(f"   📡 Discovered: {peer['id']} (Hops: {peer['hops']}, Signal: {peer['signal']} dBm)")
        
        print(f"   ✅ Mesh simulation complete - {len(mesh_peers)} peers discovered")
    
    def run_live_monitoring(self, interval=3):
        """Run live monitoring with real-time updates"""
        print("🚀 Starting live Bluetooth activity monitoring...")
        print("Press Ctrl+C to stop")
        
        self.running = True
        try:
            while self.running:
                # Get current Bluetooth data
                bt_data = self.get_bluetooth_info()
                devices = self.parse_devices(bt_data) if bt_data else []
                
                # Detect activity
                self.detect_activity(devices)
                
                # Monitor signal strength
                self.monitor_signal_strength(devices)
                
                # Display status
                self.display_live_status(devices)
                
                # Occasionally simulate mesh activity
                if self.activity_stats['scans'] % 10 == 0:
                    self.simulate_mesh_discovery()
                
                print(f"\n⏰ Next scan in {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Live monitoring stopped by user")
            self.running = False
    
    def export_activity_log(self):
        """Export activity log to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"bluetooth_activity_{timestamp}.json"
        
        log_data = {
            'scan_time': datetime.now().isoformat(),
            'statistics': dict(self.activity_stats),
            'recent_events': [
                {
                    'type': event['type'],
                    'timestamp': event['timestamp'].isoformat(),
                    'device': event.get('device', {'address': event.get('address', 'Unknown')})
                } for event in list(self.connection_events)
            ],
            'device_history': {
                address: [
                    {
                        'rssi': entry['rssi'],
                        'timestamp': entry['timestamp'].isoformat()
                    } for entry in list(history)
                ] for address, history in self.device_history.items()
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f"📝 Activity log exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting log: {e}")

def main():
    monitor = BluetoothActivityMonitor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--live':
            monitor.run_live_monitoring()
        elif sys.argv[1] == '--export':
            monitor.export_activity_log()
        elif sys.argv[1] == '--mesh':
            monitor.simulate_mesh_discovery()
        else:
            print("Usage: python3 bt_activity_monitor.py [--live|--export|--mesh]")
    else:
        print("🔗 Bluetooth Activity Monitor")
        print("=" * 40)
        print("1. --live     : Live monitoring")
        print("2. --export   : Export activity log")
        print("3. --mesh     : Simulate mesh discovery")
        monitor.run_live_monitoring()

if __name__ == "__main__":
    main() 