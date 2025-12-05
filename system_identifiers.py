"""
System identifier resolver for PCIe devices.
Maps PCIe bus addresses to system identifiers like network interfaces, RDMA devices, and GPU indices.
"""

import os
import subprocess
import re
from typing import Dict, List, Optional, Tuple
from os.path import basename


class SystemIdentifierResolver:
    def __init__(self):
        self.pci_to_netdev: Dict[str, str] = {}  # PCIe address -> network interface (e.g., "enp63s0f0np0")
        self.pci_to_rdma: Dict[str, str] = {}  # PCIe address -> RDMA device (e.g., "mlx5_1")
        self.pci_to_gpu: Dict[str, int] = {}  # PCIe address -> GPU index
        self.pci_to_nvme: Dict[str, str] = {}  # PCIe address -> NVMe device (e.g., "nvme0")
        
        # NVLink topology data
        self.gpu_to_pci: Dict[int, str] = {}  # GPU index -> PCIe address
        self.nvlink_connections: Dict[int, Dict[int, str]] = {}  # gpu_idx -> {other_gpu_idx: link_type}
        
        self._load_network_interfaces()
        self._load_rdma_devices()
        self._load_gpu_indices()
        self._load_nvme_devices()
        self._load_nvlink_topology()
    
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
        pci_devices_dir = "/sys/bus/pci/devices"
        
        if not os.path.exists(pci_devices_dir):
            return
        
        try:
            for pci_addr in os.listdir(pci_devices_dir):
                normalized_addr = pci_addr.lower()
                rdma_dir = os.path.join(pci_devices_dir, pci_addr, "infiniband")
                if os.path.exists(rdma_dir):
                    try:
                        rdma_devices = os.listdir(rdma_dir)
                        if rdma_devices:
                            # Typically only 1 infiniband device per controller
                            self.pci_to_rdma[normalized_addr] = rdma_devices[0]
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
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
        """Get RDMA device name for a PCIe node, or None if not found."""
        pci_addr = self._extract_pci_address(node_path)
        if not pci_addr:
            return None
        
        normalized = self._normalize_pci_address(pci_addr)
        return self.pci_to_rdma.get(normalized)
    
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
    
    def _load_nvlink_topology(self):
        try:
            for pci_addr, gpu_idx in self.pci_to_gpu.items():
                self.gpu_to_pci[gpu_idx] = pci_addr
            
            if not self.gpu_to_pci:
                return
            
            result = subprocess.run(
                ["nvidia-smi", "topo", "-m"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return
            
            #nvidia-smi topo -m outputs a matrix where:
            lines = [line for line in result.stdout.splitlines() if line.strip()]
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            clean_lines = [ansi_escape.sub('', line) for line in lines]
            
            header_line_idx = None
            gpu_indices = []
            gpu_column_indices = []
            
            for i, line in enumerate(clean_lines):
                #line with GPU headers (e.g., "        GPU0    GPU1    GPU2")
                parts = line.split('\t') if '\t' in line else line.split()
                if len(parts) > 1:
                    for col_idx, part in enumerate(parts):
                        part_clean = part.strip()
                        if part_clean.startswith('GPU'):
                            try:
                                idx = int(re.search(r'\d+', part_clean).group())
                                gpu_indices.append(idx)
                                gpu_column_indices.append(col_idx)
                            except (ValueError, AttributeError):
                                pass
                    if gpu_indices:
                        header_line_idx = i
                        break
            
            if not gpu_indices:
                return
            
            for i, line in enumerate(clean_lines[header_line_idx + 1:], start=0):
                parts = line.split('\t') if '\t' in line else line.split()
                if len(parts) < 2:
                    continue
                source_label = parts[0].strip()
                source_match = re.search(r'GPU(\d+)', source_label)
                if not source_match:
                    continue
                
                try:
                    source_gpu_idx = int(source_match.group(1))
                except (ValueError, AttributeError):
                    continue
                
                #parse connections
                # - Header column 1 (GPU0) -> Data column 1
                # - Header column 2 (GPU1) -> Data column 2
                for header_col_idx, target_gpu_idx in zip(gpu_column_indices, gpu_indices):
                    data_col_idx = header_col_idx
                    if data_col_idx >= len(parts):
                        break
                    
                    if target_gpu_idx == source_gpu_idx:
                        continue
                    
                    conn = parts[data_col_idx].strip()
                    if conn == 'X' or not conn:
                        continue
                    
                    if conn.startswith('NV'):
                        if source_gpu_idx not in self.nvlink_connections:
                            self.nvlink_connections[source_gpu_idx] = {}
                        self.nvlink_connections[source_gpu_idx][target_gpu_idx] = conn
                        
                        if target_gpu_idx not in self.nvlink_connections:
                            self.nvlink_connections[target_gpu_idx] = {}
                        self.nvlink_connections[target_gpu_idx][source_gpu_idx] = conn
                        
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
    
    def get_nvlink_connections(self, gpu_idx: int) -> Dict[int, str]:
        """Get all NVLink connections for a GPU index."""
        return self.nvlink_connections.get(gpu_idx, {})
    
    def get_gpu_pci_address(self, gpu_idx: int) -> Optional[str]:
        """Get PCIe address for a GPU index."""
        return self.gpu_to_pci.get(gpu_idx)
    
    def has_nvlink_topology(self) -> bool:
        """Check if there are any NVLink connections."""
        return any(self.nvlink_connections.values())
    
    def get_all_gpu_indices(self) -> List[int]:
        """Get list of all GPU indices."""
        return sorted(self.gpu_to_pci.keys())


# Global instance
_system_resolver = None

def get_system_resolver() -> SystemIdentifierResolver:
    global _system_resolver
    if _system_resolver is None:
        _system_resolver = SystemIdentifierResolver()
    return _system_resolver

