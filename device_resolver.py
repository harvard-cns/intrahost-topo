"""
Device name resolver for PCI vendor/device IDs.
"""

import json
import os
import subprocess
from typing import Optional, Dict


class DeviceResolver:
    def __init__(self, known_devices_path: str = "Known_devices.json", known_vendors_path: str = "Known_vendors.json"):
        self.device_cache: Dict[str, str] = {}
        self.vendor_cache: Dict[str, str] = {}
        self.class_cache: Dict[str, str] = {}
        self.known_devices = self._load_known_devices(known_devices_path)
        self.known_vendors = self._load_known_vendors(known_vendors_path)
    
    def _load_known_devices(self, path: str) -> Dict:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}
    
    def _load_known_vendors(self, path: str) -> Dict:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}
    
    def _query_lspci(self, vendor_id: str, device_id: str) -> Optional[tuple]:
        """Query lspci for vendor and device names, return (vendor, device) or None."""
        try:
            cmd = f"lspci -vvm -d {vendor_id}:{device_id}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                vendor_name = None
                device_name = None
                for line in result.stdout.splitlines():
                    stripped = line.strip()
                    if stripped.startswith('Vendor:'):
                        vendor_name = stripped.split(':', 1)[1].strip()
                    elif stripped.startswith('Device:'):
                        device_name = stripped.split(':', 1)[1].strip()
                if vendor_name and device_name:
                    return (vendor_name, device_name)
        except:
            pass
        return None
    
    def _query_lspci_class(self, vendor_id: str, device_id: str) -> Optional[str]:
        """Query lspci for class name, return class name or None."""
        try:
            cmd = f"lspci -vvm -d {vendor_id}:{device_id}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.splitlines():
                    stripped = line.strip()
                    if stripped.startswith('Class:'):
                        class_name = stripped.split(':', 1)[1].strip()
                        return class_name
        except:
            pass
        return None
    
    
    def get_vendor_name(self, vendor_id: str) -> str:
        """Get human-readable vendor name."""
        if not vendor_id:
            return "Unknown Vendor"
        
        vendor_id = vendor_id.replace('0x', '') if vendor_id.startswith('0x') else vendor_id
        
        if vendor_id in self.vendor_cache:
            return self.vendor_cache[vendor_id]
        
        if vendor_id in self.known_vendors:
            vendor_name = self.known_vendors[vendor_id]
            self.vendor_cache[vendor_id] = vendor_name
            return vendor_name
        
        # Try lspci
        lspci_result = self._query_lspci(vendor_id, "*")
        if lspci_result:
            vendor_name, _ = lspci_result
            self.vendor_cache[vendor_id] = vendor_name
            return vendor_name
        
        self.vendor_cache[vendor_id] = vendor_id
        return vendor_id
    
    def get_device_name(self, vendor_id: str, device_id: str) -> str:
        """Get human-readable device name."""
        if not device_id:
            return "Unknown Device"
        
        vendor_id = vendor_id.replace('0x', '') if vendor_id.startswith('0x') else vendor_id
        device_id = device_id.replace('0x', '') if device_id.startswith('0x') else device_id
        
        device_key = f"{vendor_id}:{device_id}"
        
        if device_key in self.device_cache:
            return self.device_cache[device_key]
        
        if vendor_id in self.known_devices:
            vendor_devices = self.known_devices[vendor_id]
            if device_id in vendor_devices:
                device_name = vendor_devices[device_id]
                self.device_cache[device_key] = device_name
                return device_name
        
        #Try lspci
        lspci_result = self._query_lspci(vendor_id, device_id)
        if lspci_result:
            _, device_name = lspci_result
            self.device_cache[device_key] = device_name
            return device_name
        
        self.device_cache[device_key] = device_id
        return device_id
    
    def get_class_name(self, vendor_id: str, device_id: str, class_code: Optional[str] = None) -> Optional[str]:
        """Get human-readable class name from lspci."""
        if not vendor_id or not device_id:
            return None
        
        # Check cache first if class_code is provided
        if class_code and class_code in self.class_cache:
            return self.class_cache[class_code]
        
        vendor_id = vendor_id.replace('0x', '') if vendor_id.startswith('0x') else vendor_id
        device_id = device_id.replace('0x', '') if device_id.startswith('0x') else device_id
        
        class_name = self._query_lspci_class(vendor_id, device_id)
        
        # Cache the result if we have a class_code
        if class_name and class_code:
            self.class_cache[class_code] = class_name
        
        return class_name


# Global instance
_device_resolver = None

def get_device_resolver() -> DeviceResolver:
    global _device_resolver
    if _device_resolver is None:
        _device_resolver = DeviceResolver()
    return _device_resolver

def get_vendor_name(vendor_id: str) -> str:
    return get_device_resolver().get_vendor_name(vendor_id)

def get_device_name(vendor_id: str, device_id: str) -> str:
    return get_device_resolver().get_device_name(vendor_id, device_id)

def get_class_name(vendor_id: str, device_id: str, class_code: Optional[str] = None) -> Optional[str]:
    return get_device_resolver().get_class_name(vendor_id, device_id, class_code)