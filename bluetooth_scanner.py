#!/usr/bin/env python3
"""
Bluetooth Scanner for macOS
Scans for nearby Bluetooth devices and displays them in a formatted way
"""

import subprocess
import json
import time
import sys
from datetime import datetime

class BluetoothScanner:
    def __init__(self):
        self.discovered_devices = {}
        
    def get_bluetooth_status(self):
        """Get current Bluetooth status"""
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Error getting Bluetooth status: {e}")
            return None
    
    def parse_bluetooth_info(self, info_text):
        """Parse Bluetooth information from system_profiler output"""
        devices = []
        current_device = {}
        
        lines = info_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if ':' in line and not line.startswith('Bluetooth'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if key == 'Address':
                    if current_device:
                        devices.append(current_device)
                    current_device = {'address': value}
                elif key in ['State', 'Firmware Version', 'Product ID', 'Vendor ID', 'Minor Type']:
                    current_device[key.lower().replace(' ', '_')] = value
            elif line.endswith(':') and not line.startswith('Bluetooth'):
                # This is likely a device name
                device_name = line[:-1].strip()
                if device_name and device_name not in ['Not Connected', 'Connected']:
                    current_device['name'] = device_name
        
        if current_device:
            devices.append(current_device)
            
        return devices
    
    def display_devices(self, devices):
        """Display discovered devices in a nice format"""
        print("\n" + "="*60)
        print(f"📱 BLUETOOTH SCAN RESULTS - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        if not devices:
            print("No devices found")
            return
            
        for i, device in enumerate(devices, 1):
            print(f"\n🔵 Device {i}:")
            print(f"   Name: {device.get('name', 'Unknown')}")
            print(f"   Address: {device.get('address', 'Unknown')}")
            if 'state' in device:
                print(f"   State: {device['state']}")
            if 'minor_type' in device:
                print(f"   Type: {device['minor_type']}")
            if 'firmware_version' in device:
                print(f"   Firmware: {device['firmware_version']}")
    
    def scan_continuously(self, interval=5):
        """Continuously scan for devices"""
        print("🔍 Starting continuous Bluetooth scan...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                info = self.get_bluetooth_status()
                if info:
                    devices = self.parse_bluetooth_info(info)
                    self.display_devices(devices)
                else:
                    print("❌ Failed to get Bluetooth info")
                
                print(f"\n⏰ Waiting {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Scan stopped by user")
    
    def scan_once(self):
        """Single scan for devices"""
        print("🔍 Scanning for Bluetooth devices...")
        info = self.get_bluetooth_status()
        if info:
            devices = self.parse_bluetooth_info(info)
            self.display_devices(devices)
        else:
            print("❌ Failed to get Bluetooth info")

def main():
    scanner = BluetoothScanner()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        scanner.scan_continuously()
    else:
        scanner.scan_once()

if __name__ == "__main__":
    main() 