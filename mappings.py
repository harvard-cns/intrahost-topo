from typing import List
from PcieNode import PcieNode


def get_device_class_label(node: PcieNode) -> str:
    if not node.class_:
        return ""
    
    class_mappings = {
        # Base Class 00h - Unclassified Device
        '0x000000': 'Unclassified device',
        '0x000080': 'Non-VGA unclassified device',
        '0x000100': 'VGA compatible unclassified device',
        
        # Base Class 01h - Mass Storage Controller
        '0x010000': 'SCSI bus controller',
        '0x010100': 'IDE interface',
        '0x010110': 'ATA controller (single DMA)',
        '0x010120': 'ATA controller (chained DMA)',
        '0x010180': 'ATA controller (other)',
        '0x010200': 'Floppy disk controller',
        '0x010300': 'IPI bus controller',
        '0x010400': 'RAID bus controller',
        '0x010500': 'ATA controller',
        '0x010600': 'Serial ATA controller',
        '0x010601': 'Serial ATA controller (AHCI 1.0)',
        '0x010602': 'Serial ATA controller (vendor specific)',
        '0x010700': 'Serial Attached SCSI controller',
        '0x010800': 'Non-Volatile memory controller',
        '0x010801': 'NVMHCI controller',
        '0x010802': 'NVM Express controller',
        '0x010900': 'Other mass storage controller',
        
        # Base Class 02h - Network Controller
        '0x020000': 'Ethernet controller',
        '0x020100': 'Token ring network controller',
        '0x020200': 'FDDI network controller',
        '0x020300': 'ATM network controller',
        '0x020400': 'ISDN controller',
        '0x020500': 'WorldFip controller',
        '0x020600': 'PICMG 2.14 Multi Computing',
        '0x020700': 'Infiniband controller',
        '0x020800': 'Fabric controller',
        '0x028000': 'Other network controller',
        
        # Base Class 03h - Display Controller
        '0x030000': 'VGA compatible controller',
        '0x030100': 'XGA controller',
        '0x030200': '3D controller',
        '0x038000': 'Other display controller',
        
        # Base Class 04h - Multimedia Device
        '0x040000': 'Multimedia video controller',
        '0x040100': 'Multimedia video controller (VGA)',
        '0x040300': 'Audio device',
        '0x040380': 'Audio device (HD Audio)',
        '0x048000': 'Other multimedia device',
        
        # Base Class 05h - Memory Controller
        '0x050000': 'RAM memory',
        '0x050100': 'FLASH memory',
        '0x058000': 'Other memory controller',
        
        # Base Class 06h - Bridge Device
        '0x060000': 'Host bridge',
        '0x060100': 'ISA bridge',
        '0x060200': 'EISA bridge',
        '0x060300': 'MCA bridge',
        '0x060400': 'PCI-to-PCI bridge',
        '0x060401': 'PCI-to-PCI bridge (subtractive decode)',
        '0x060500': 'PCMCIA bridge',
        '0x060600': 'NuBus bridge',
        '0x060700': 'CardBus bridge',
        '0x060800': 'RACEway bridge',
        '0x060900': 'PCI-to-PCI bridge (semi-transparent)',
        '0x060a00': 'InfiniBand-to-PCI host bridge',
        '0x068000': 'Other bridge device',
        
        # Base Class 07h - Simple Communication Controller
        '0x070000': 'Serial controller',
        '0x070100': 'Parallel controller',
        '0x070200': 'Multiport serial controller',
        '0x070300': 'Modem',
        '0x070400': 'IEEE 488.1/2 (GPIB) controller',
        '0x070500': 'Smart card',
        '0x070800': 'Other communication device',
        
        # Base Class 08h - Base System Peripheral
        '0x080000': 'PIC',
        '0x080100': 'DMA controller',
        '0x080200': 'Timer',
        '0x080300': 'RTC',
        '0x080400': 'PCI Hot-plug controller',
        '0x080500': 'SD Host controller',
        '0x080600': 'IOMMU',
        '0x080700': 'Root Complex Event Collector',
        '0x088000': 'Other base system peripheral',
        
        # Base Class 09h - Input Device
        '0x090000': 'Keyboard controller',
        '0x090100': 'Digitizer',
        '0x090200': 'Mouse controller',
        '0x090300': 'Scanner controller',
        '0x090400': 'Gameport controller',
        '0x098000': 'Other input device',
        
        # Base Class 0Ah - Docking Station
        '0x0a0000': 'Generic docking station',
        '0x0a8000': 'Other docking station',
        
        # Base Class 0Bh - Processor
        '0x0b0000': '386 processor',
        '0x0b0100': '486 processor',
        '0x0b0200': 'Pentium processor',
        '0x0b0300': 'Pentium Pro processor',
        '0x0b1000': 'Alpha processor',
        '0x0b2000': 'PowerPC processor',
        '0x0b3000': 'MIPS processor',
        '0x0b4000': 'Co-processor',
        '0x0b8000': 'Other processor',
        
        # Base Class 0Ch - Serial Bus Controller
        '0x0c0000': 'FireWire (IEEE 1394) controller',
        '0x0c0010': 'FireWire (IEEE 1394) controller (OHCI)',
        '0x0c0100': 'ACCESS.bus',
        '0x0c0200': 'SSA',
        '0x0c0300': 'USB UHCI controller',
        '0x0c0310': 'USB UHCI controller',
        '0x0c0320': 'USB OHCI controller',
        '0x0c0330': 'USB EHCI controller',
        '0x0c0340': 'USB XHCI controller',
        '0x0c0350': 'USB device controller',
        '0x0c0380': 'USB controller (unified)',
        '0x0c0400': 'Fibre Channel',
        '0x0c0500': 'SMBus',
        '0x0c0600': 'InfiniBand',
        '0x0c0700': 'IPMI SMIC interface',
        '0x0c0701': 'IPMI Keyboard Controller Style interface',
        '0x0c0702': 'IPMI Block Transfer interface',
        '0x0c0800': 'SERCOS interface (IEC 61491)',
        '0x0c0900': 'CANbus',
        '0x0c0a00': 'I3C controller',
        '0x0c8000': 'Other serial bus controller',
        
        # Base Class 0Dh - Wireless Controller
        '0x0d0000': 'iRDA compatible controller',
        '0x0d0100': 'Consumer IR controller',
        '0x0d0200': 'RF controller',
        '0x0d0300': 'Bluetooth controller',
        '0x0d0400': 'Broadband controller',
        '0x0d0500': 'Ethernet controller (802.11a)',
        '0x0d0600': 'Ethernet controller (802.11b)',
        '0x0d0700': 'Cellular controller',
        '0x0d0800': 'Ethernet controller (802.11abg)',
        '0x0d0900': 'Ethernet controller (802.11n)',
        '0x0d0a00': 'Other wireless controller',
        '0x0d4000': 'Multi-function wireless controller',
        '0x0d4100': 'Multi-function wireless controller',
        '0x0d8000': 'Other wireless controller',
        
        # Base Class 0Eh - Intelligent I/O Controller
        '0x0e0000': 'I2O controller',
        '0x0e8000': 'Other intelligent I/O controller',
        
        # Base Class 0Fh - Satellite Communication Controller
        '0x0f0000': 'Satellite TV controller',
        '0x0f0100': 'Satellite audio controller',
        '0x0f0300': 'Satellite voice controller',
        '0x0f0400': 'Satellite data controller',
        '0x0f8000': 'Other satellite communication controller',
        
        # Base Class 10h - Encryption Controller
        '0x100000': 'Network and computing encryption device',
        '0x100100': 'Entertainment encryption device',
        '0x108000': 'Other encryption controller',
        
        # Base Class 11h - Signal Processing Controller
        '0x110000': 'DPIO modules',
        '0x110100': 'Performance counters',
        '0x111000': 'Communication synchronizer',
        '0x112000': 'Signal processing management',
        '0x118000': 'Other signal processing controller',
        
        # Base Class 12h - Processing Accelerator
        '0x120000': 'Processing accelerator',
        '0x128000': 'Other processing accelerator',
        
        # Base Class 13h - Non-Essential Instrumentation Function
        '0x130000': 'Non-Essential Instrumentation Function',
    }
    
    if node.class_ in class_mappings:
        return class_mappings[node.class_]
    
    for class_code, label in class_mappings.items():
        if node.class_.startswith(class_code):
            return label
    return f"Unknown class ({node.class_})"


def tree_contains_class(root: PcieNode, target_classes: List[str]) -> bool:
    target_set = {cls.lower().strip() for cls in target_classes}
    
    def check_node(node: PcieNode) -> bool:
        class_label = get_device_class_label(node)
        if class_label.lower() in target_set:
            return True

        for child in node.children:
            if check_node(child):
                return True
        
        return False
    
    return check_node(root)


def filter_trees_by_classes(roots: List[PcieNode], target_classes: List[str]) -> List[PcieNode]:
    if not target_classes:
        return roots
    
    filtered_roots = []
    for root in roots:
        if tree_contains_class(root, target_classes):
            filtered_roots.append(root)
    
    return filtered_roots


def parse_filter_classes(filter_string: str) -> List[str]:

    if not filter_string:
        return []
    classes = [cls.strip() for cls in filter_string.split(',')]
    return [cls for cls in classes if cls]
