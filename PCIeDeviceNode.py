import os
import subprocess

class PCIeDeviceNode:
    def __init__(self, path: str):
        # E.g., `/sys/devices/pci0000:e0/0000:e0:05.1`
        self.path = path
        
        self.id = None
        self.info = {}  
        
        self.max_link_speed = None
        self.current_link_speed = None
        self.max_link_width = None
        self.current_link_width = None
        
        self.numa_node = None
        
        self.children = []

        # Initialize fields. 
        self.set_id()
        self.set_info()
        self.set_numa_node()
        self.set_current_link_speed()
        self.set_max_link_speed()
        self.set_current_link_width()
        self.set_max_link_width()

    def add_child(self, child_node):
        self.children.append(child_node)
    
    def __read_file(self, filename: str):
        """
        Helper to read a file within self.path. 
        Returns the stripped contents or None if not found.
        """
        file_path = os.path.join(self.path, filename)
        try:
            with open(file_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def set_id(self):
        """
        Set `self.id` to "<vendor>:<device>" based on 
        the contents of self.path/vendor and self.path/device.
        """
        vendor = self.__read_file("vendor")
        device = self.__read_file("device")
        if vendor and device:
            self.id = f"{vendor}:{device}"
        else:
            self.id = None

    @staticmethod
    def __parse_info(stdout: str) -> dict:
        """
        Given stdout from a command like `lspci -vvm -d <id>`,
        return a dictionary with tag-value pairs.
        """
        info = {}
        for line in stdout.splitlines():
            if "\t" in line:
                # Tags and values are separated by a tab.
                tag, value = line.split("\t", 1)
                tag = tag.rstrip(":").strip()
                value = value.strip()
                info[tag] = value
        return info

    def set_info(self):
        """
        Query the PCI database locally first and, if necessary,
        remotely using lspci, to set self.info.
        """
        if not self.id:
            self.info = None
            return
        
        local_query_cmd = f"lspci -vvm -d {self.id}"
        central_query_cmd = f"lspci -q -vvm -d {self.id}"

        try:
            local_query_stdout = subprocess.check_output(local_query_cmd, text=True, shell=True)
            if local_query_stdout:
                self.info = PCIeDeviceNode.__parse_info(local_query_stdout)
                return  # Found local info; no need to query remotely.
        except subprocess.CalledProcessError:
            # Local query failed; proceed to query central database.
            pass

        try:
            central_query_stdout = subprocess.check_output(central_query_cmd, text=True, shell=True)
            if central_query_stdout:
                self.info = PCIeDeviceNode.__parse_info(central_query_stdout)
                return
        except subprocess.CalledProcessError:
            # Central query failed.
            pass

        # If no info was found either locally or centrally, leave info as None.
        self.info = None

    def set_numa_node(self):
        """
        Reads the NUMA node from self.path/numa_node 
        and sets self.numa_node.
        """
        numa_str = self.__read_file("numa_node")
        if numa_str is not None:
            try:
                self.numa_node = int(numa_str)
            except ValueError:
                self.numa_node = None
        else:
            self.numa_node = None

    def set_current_link_speed(self):
        """Reads current link speed from self.path/current_link_speed."""
        self.current_link_speed = self.__read_file("current_link_speed")

    def set_max_link_speed(self):
        """Reads maximum link speed from self.path/max_link_speed."""
        self.max_link_speed = self.__read_file("max_link_speed")

    def set_current_link_width(self):
        """Reads current link width from self.path/current_link_width."""
        self.current_link_width = self.__read_file("current_link_width")

    def set_max_link_width(self):
        """Reads maximum link width from self.path/max_link_width."""
        self.max_link_width = self.__read_file("max_link_width")

    def __str__(self) -> str:
        # For the sake of testing and simplicity, just return `self.path`. 
        return self.path[-12:]
