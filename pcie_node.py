import os
import subprocess
from typing import Dict, List, Optional


class PcieNode:
    def __init__(self, path: str) -> None:
        self.path: str = path  # E.g., "/sys/devices/pci0000:e0/0000:e0:05.1".

        self.device: Optional[str] = None
        self.vendor: Optional[str] = None
        self.lspci_vmm: Optional[Dict] = (
            None  # Output of `lspci -vvm -d <vendor>:<device>`.
        )
        self.class_: Optional[str] = None
        self.numa_node: Optional[str] = None
        self.max_link_speed: Optional[str] = None
        self.current_link_speed: Optional[str] = None
        self.max_link_width: Optional[str] = None
        self.current_link_width: Optional[str] = None
        self.children: List = []

        if os.path.exists(self.path):
            self.set_device()
            self.set_vendor()
            self.set_lspci_vmm()
            self.set_class()
            self.set_numa_node()
            self.set_current_link_speed()
            self.set_max_link_speed()
            self.set_current_link_width()
            self.set_max_link_width()

    @staticmethod
    def _read_file(file_path: str) -> Optional[str]:
        try:
            with open(file_path, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return None
        except Exception as _:
            return None

    @staticmethod
    def _parse_lspci_vmm_output(output: str) -> Dict:
        """
        Args:
            output: Output of `lspci -vvm -d <vendor>:<device>`.
        Return:
            Hashmap of tag-value pairs.
        """
        hashmap = {}
        for line in output.splitlines():
            if "\t" in line:
                # Tags and values are separated by a tab.
                tag, value = line.split("\t", maxsplit=1)
                tag = tag.rstrip(":").strip()
                value = value.strip()
                hashmap[tag] = value
        return hashmap

    def set_lspci_vmm(self):
        if not self.vendor and not self.device:
            self.lspci_vmm = None
            return

        local_query_cmd = f"lspci -vvm -d {self.vendor}:{self.device}"
        central_query_cmd = f"lspci -q -vvm -d {self.vendor}:{self.device}"

        try:
            local_query_stdout = subprocess.check_output(
                local_query_cmd, text=True, shell=True
            )
            if local_query_stdout:
                self.lspci_vmm = PcieNode._parse_lspci_vmm_output(local_query_stdout)
                return
        except Exception as _:
            # Local quary failed. Try central quary next.
            pass

        try:
            central_query_stdout = subprocess.check_output(
                central_query_cmd, text=True, shell=True
            )
            if central_query_stdout:
                self.lspci_vmm = PcieNode._parse_lspci_vmm_output(central_query_stdout)
                return
        except Exception as _:
            # Central quary failed.
            pass

        # Both local and central queries failed.
        self.lspci_vmm = None

    def set_vendor(self):
        file_path = os.path.join(self.path, "vendor")
        self.vendor = PcieNode._read_file(file_path)

    def set_device(self):
        file_path = os.path.join(self.path, "device")
        self.device = PcieNode._read_file(file_path)

    def set_numa_node(self):
        file_path = os.path.join(self.path, "numa_node")
        self.numa_node = PcieNode._read_file(file_path)

    def set_class(self):
        file_path = os.path.join(self.path, "class")
        self.class_ = PcieNode._read_file(file_path)

    def set_current_link_speed(self):
        file_path = os.path.join(self.path, "current_link_speed")
        self.current_link_speed = PcieNode._read_file(file_path)

    def set_current_link_width(self):
        file_path = os.path.join(self.path, "current_link_width")
        self.current_link_width = PcieNode._read_file(file_path)

    def set_max_link_speed(self):
        file_path = os.path.join(self.path, "current_link_speed")
        self.current_link_speed = PcieNode._read_file(file_path)

    def set_max_link_width(self):
        file_path = os.path.join(self.path, "current_max_width")
        self.current_max_width = PcieNode._read_file(file_path)

    def __str__(self) -> str:
        return (
            f"{self.lspci_vmm['Slot']}"
            if self.lspci_vmm is not None
            else "Unavailable. "
        )
