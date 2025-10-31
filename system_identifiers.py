"""
System identifier resolver for PCIe devices.
Maps PCIe bus addresses to system identifiers like network interfaces, RDMA devices, and GPU indices.
"""

import os
import subprocess
import re
from typing import Dict, Optional, Tuple
from os.path import basename


class SystemIdentifierResolver:
    def __init__(self):
        self.pci_to_netdev: Dict[str, str] = {}  # PCIe address -> network interface (e.g., "enp63s0f0np0")
        self.netdev_to_rdma: Dict[str, str] = {}  # network interface -> RDMA device (e.g., "mlx5_1")
        self.pci_to_gpu: Dict[str, int] = {}  # PCIe address -> GPU index
        self.pci_to_nvme: Dict[str, str] = {}  # PCIe address -> NVMe device (e.g., "nvme0")
        
        self._load_network_interfaces()
        self._load_rdma_devices()
        self._load_gpu_indices()
        self._load_nvme_devices()
    
    def _extract_pci_address(self, path: str) -> Optional[str]:
        matches = re.findall(r'([0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7])', path)
        if matches:
            return matches[-1]
        return None
    
    def _normalize_pci_address(self, address: str) -> str:
        if not address.startswith('0000:') and not address.startswith('0000'):
            return f"0000:{address.lower()}"
        return address.lower()
    
    def _load_network_interfaces(self):
        pci_devices_dir = "/sys/bus/pci/devices"
        
        if not os.path.exists(pci_devices_dir):
            return
        
        try:
            for pci_addr in os.listdir(pci_devices_dir):
                normalized_addr = pci_addr.lower()
                net_dir = os.path.join(pci_devices_dir, pci_addr, "net")
                if os.path.exists(net_dir):
                    try:
                        net_interfaces = os.listdir(net_dir)
                        if net_interfaces:
                            self.pci_to_netdev[normalized_addr] = net_interfaces[0]
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
    
    def _load_rdma_devices(self):
        try:
            result = subprocess.run(
                ["ibdev2netdev"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    match = re.match(r'(\S+)\s+port\s+\d+\s+==>\s+(\S+)', line)
                    if match:
                        rdma_dev = match.group(1) 
                        netdev = match.group(2)
                        self.netdev_to_rdma[netdev] = rdma_dev
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
    
    def _load_gpu_indices(self):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=index,pci.bus_id", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    parts = line.split(',')
                    if len(parts) >= 2:
                        gpu_index = parts[0].strip()
                        pci_bus_id = parts[1].strip()
                        pci_bus_id = pci_bus_id.replace('00000000:', '0000:')
                        pci_bus_id = pci_bus_id.lower()
                        normalized = self._normalize_pci_address(pci_bus_id)
                        
                        try:
                            self.pci_to_gpu[normalized] = int(gpu_index)
                        except ValueError:
                            continue
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
    
    def _load_nvme_devices(self):
        pci_devices_dir = "/sys/bus/pci/devices"
        
        if not os.path.exists(pci_devices_dir):
            return
        
        try:
            for pci_addr in os.listdir(pci_devices_dir):
                normalized_addr = pci_addr.lower()
                nvme_dir = os.path.join(pci_devices_dir, pci_addr, "nvme")
                if os.path.exists(nvme_dir):
                    try:
                        nvme_devices = os.listdir(nvme_dir)
                        if nvme_devices:
                            # Typically one NVMe device per controller
                            self.pci_to_nvme[normalized_addr] = nvme_devices[0]
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
    
    def get_network_interface(self, node_path: str) -> Optional[str]:
        pci_addr = self._extract_pci_address(node_path)
        if not pci_addr:
            return None
        
        normalized = self._normalize_pci_address(pci_addr)
        return self.pci_to_netdev.get(normalized)
    
    def get_rdma_device(self, node_path: str) -> Optional[str]:
        netdev = self.get_network_interface(node_path)
        if not netdev:
            return None
        
        return self.netdev_to_rdma.get(netdev)
    
    def get_gpu_index(self, node_path: str) -> Optional[int]:
        pci_addr = self._extract_pci_address(node_path)
        if not pci_addr:
            return None
        
        normalized = self._normalize_pci_address(pci_addr)
        
        gpu_idx = self.pci_to_gpu.get(normalized)
        if gpu_idx is not None:
            return gpu_idx
        if '.' in normalized:
            base_addr = normalized.rsplit('.', 1)[0] + '.0'
            return self.pci_to_gpu.get(base_addr)
        
        return None
    
    def get_nvme_device(self, node_path: str) -> Optional[str]:
        """Get NVMe device name for a PCIe node, or None if not found."""
        pci_addr = self._extract_pci_address(node_path)
        if not pci_addr:
            return None
        
        normalized = self._normalize_pci_address(pci_addr)
        return self.pci_to_nvme.get(normalized)
    
    def get_all_identifiers(self, node_path: str) -> Tuple[Optional[str], Optional[str], Optional[int], Optional[str]]:
        """
        Get all system identifiers for a PCIe node.
        Returns: (network_interface, rdma_device, gpu_index, nvme_device)
        """
        netdev = self.get_network_interface(node_path)
        rdma = self.get_rdma_device(node_path)
        gpu_idx = self.get_gpu_index(node_path)
        nvme = self.get_nvme_device(node_path)
        
        return (netdev, rdma, gpu_idx, nvme)


# Global instance
_system_resolver = None

def get_system_resolver() -> SystemIdentifierResolver:
    global _system_resolver
    if _system_resolver is None:
        _system_resolver = SystemIdentifierResolver()
    return _system_resolver

