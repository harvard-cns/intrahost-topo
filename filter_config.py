"""
Filter Configuration File

This file contains boolean filters for different device classes.
Set any filter to True to include trees containing that device class.
Set to False to exclude trees containing that device class.

Tree-level filtering: If a tree contains at least one node belonging to 
the specified classes (where filter=True), include the entire tree.
"""

# =============================================================================
# QUICK FILTERS
# =============================================================================
from pickle import FALSE


show_all = True
show_any_gpu = True
show_any_ethernet = False
show_any_storage = False 

# =============================================================================
# UNCLASSIFIED DEVICES (Base Class 00h)
# =============================================================================
show_unclassified_device = False
show_non_vga_unclassified_device = False
show_vga_compatible_unclassified_device = False

# =============================================================================
# MASS STORAGE CONTROLLERS (Base Class 01h)
# =============================================================================
show_scsi_bus_controller = False
show_ide_interface = False
show_ata_controller_single_dma = False
show_ata_controller_chained_dma = False
show_ata_controller_other = False
show_floppy_disk_controller = False
show_ipi_bus_controller = False
show_raid_bus_controller = False
show_ata_controller = False
show_serial_ata_controller = False
show_serial_ata_controller_ahci_1_0 = False
show_serial_ata_controller_vendor_specific = False
show_serial_attached_scsi_controller = False
show_non_volatile_memory_controller = False
show_nvmhci_controller = False
show_nvm_express_controller = False
show_other_mass_storage_controller = False

# =============================================================================
# NETWORK CONTROLLERS (Base Class 02h)
# =============================================================================
show_ethernet_controller = False
show_token_ring_network_controller = False
show_fddi_network_controller = False
show_atm_network_controller = False
show_isdn_controller = False
show_worldfip_controller = False
show_picmg_2_14_multi_computing = False
show_infiniband_controller = False
show_fabric_controller = False
show_other_network_controller = False

# =============================================================================
# DISPLAY CONTROLLERS (Base Class 03h)
# =============================================================================
show_vga_compatible_controller = False
show_xga_controller = False
show_3d_controller = False
show_other_display_controller = False

# =============================================================================
# MULTIMEDIA DEVICES (Base Class 04h)
# =============================================================================
show_multimedia_video_controller = False
show_multimedia_video_controller_vga = False
show_audio_device = False
show_audio_device_hd_audio = False
show_other_multimedia_device = False

# =============================================================================
# MEMORY CONTROLLERS (Base Class 05h)
# =============================================================================
show_ram_memory = False
show_flash_memory = False
show_other_memory_controller = False

# =============================================================================
# BRIDGE DEVICES (Base Class 06h)
# =============================================================================
show_host_bridge = False
show_isa_bridge = False
show_eisa_bridge = False
show_mca_bridge = False
show_pci_to_pci_bridge = False
show_pci_to_pci_bridge_subtractive_decode = False
show_pcmcia_bridge = False
show_nubus_bridge = False
show_cardbus_bridge = False
show_raceway_bridge = False
show_pci_to_pci_bridge_semi_transparent = False
show_infiniband_to_pci_host_bridge = False
show_other_bridge_device = False

# =============================================================================
# SIMPLE COMMUNICATION CONTROLLERS (Base Class 07h)
# =============================================================================
show_serial_controller = False
show_parallel_controller = False
show_multiport_serial_controller = False
show_modem = False
show_ieee_488_1_2_gpib_controller = False
show_smart_card = False
show_other_communication_device = False

# =============================================================================
# BASE SYSTEM PERIPHERALS (Base Class 08h)
# =============================================================================
show_pic = False
show_dma_controller = False
show_timer = False
show_rtc = False
show_pci_hot_plug_controller = False
show_sd_host_controller = False
show_iommu = False
show_root_complex_event_collector = False
show_other_base_system_peripheral = False

# =============================================================================
# INPUT DEVICES (Base Class 09h)
# =============================================================================
show_keyboard_controller = False
show_digitizer = False
show_mouse_controller = False
show_scanner_controller = False
show_gameport_controller = False
show_other_input_device = False

# =============================================================================
# DOCKING STATIONS (Base Class 0Ah)
# =============================================================================
show_generic_docking_station = False
show_other_docking_station = False

# =============================================================================
# PROCESSORS (Base Class 0Bh)
# =============================================================================
show_386_processor = False
show_486_processor = False
show_pentium_processor = False
show_pentium_pro_processor = False
show_alpha_processor = False
show_powerpc_processor = False
show_mips_processor = False
show_co_processor = False
show_other_processor = False

# =============================================================================
# SERIAL BUS CONTROLLERS (Base Class 0Ch)
# =============================================================================
show_firewire_ieee_1394_controller = False
show_firewire_ieee_1394_controller_ohci = False
show_access_bus = False
show_ssa = False
show_usb_uhci_controller = False
show_usb_ohci_controller = False
show_usb_ehci_controller = False
show_usb_xhci_controller = False
show_usb_device_controller = False
show_usb_controller_unified = False
show_fibre_channel = False
show_smbus = False
show_infiniband = False
show_ipmi_smic_interface = False
show_ipmi_keyboard_controller_style_interface = False
show_ipmi_block_transfer_interface = False
show_sercos_interface_iec_61491 = False
show_canbus = False
show_i3c_controller = False
show_other_serial_bus_controller = False

# =============================================================================
# WIRELESS CONTROLLERS (Base Class 0Dh)
# =============================================================================
show_irda_compatible_controller = False
show_consumer_ir_controller = False
show_rf_controller = False
show_bluetooth_controller = False
show_broadband_controller = False
show_ethernet_controller_802_11a = False
show_ethernet_controller_802_11b = False
show_cellular_controller = False
show_ethernet_controller_802_11abg = False
show_ethernet_controller_802_11n = False
show_other_wireless_controller = False
show_multi_function_wireless_controller = False

# =============================================================================
# INTELLIGENT I/O CONTROLLERS (Base Class 0Eh)
# =============================================================================
show_i2o_controller = False
show_other_intelligent_i_o_controller = False

# =============================================================================
# SATELLITE COMMUNICATION CONTROLLERS (Base Class 0Fh)
# =============================================================================
show_satellite_tv_controller = False
show_satellite_audio_controller = False
show_satellite_voice_controller = False
show_satellite_data_controller = False
show_other_satellite_communication_controller = False

# =============================================================================
# ENCRYPTION CONTROLLERS (Base Class 10h)
# =============================================================================
show_network_and_computing_encryption_device = False
show_entertainment_encryption_device = False
show_other_encryption_controller = False

# =============================================================================
# SIGNAL PROCESSING CONTROLLERS (Base Class 11h)
# =============================================================================
show_dpio_modules = False
show_performance_counters = False
show_communication_synchronizer = False
show_signal_processing_management = False
show_other_signal_processing_controller = False

# =============================================================================
# PROCESSING ACCELERATORS (Base Class 12h)
# =============================================================================
show_processing_accelerator = False
show_other_processing_accelerator = False

# =============================================================================
# NON-ESSENTIAL INSTRUMENTATION FUNCTIONS (Base Class 13h)
# =============================================================================
show_non_essential_instrumentation_function = False


def get_active_filters():
    from mappings import get_device_class_label
    from PcieNode import PcieNode
    
    current_module = globals()
    active_filters = []
    
    if current_module.get('show_all', False):
        return []
    
    if current_module.get('show_any_gpu', False):
        gpu_classes = [
            'VGA compatible controller',
            'XGA controller', 
            '3D controller',
            'Other display controller'
        ]
        active_filters.extend(gpu_classes)
    
    if current_module.get('show_any_ethernet', False):
        ethernet_classes = [
            'Ethernet controller',
            'Token ring network controller',
            'FDDI network controller',
            'ATM network controller',
            'ISDN controller',
            'WorldFip controller',
            'PICMG 2.14 Multi Computing',
            'Infiniband controller',
            'Fabric controller',
            'Other network controller'
        ]
        active_filters.extend(ethernet_classes)
    
    if current_module.get('show_any_storage', False):
        storage_classes = [
            'SCSI bus controller',
            'IDE interface',
            'ATA controller (single DMA)',
            'ATA controller (chained DMA)',
            'ATA controller (other)',
            'Floppy disk controller',
            'IPI bus controller',
            'RAID bus controller',
            'ATA controller',
            'Serial ATA controller',
            'Serial ATA controller (AHCI 1.0)',
            'Serial ATA controller (vendor specific)',
            'Serial Attached SCSI controller',
            'Non-Volatile memory controller',
            'NVMHCI controller',
            'NVM Express controller',
            'Other mass storage controller'
        ]
        active_filters.extend(storage_classes)
    
    # Handle individual detailed filters
    filter_mappings = {
        'show_unclassified_device': 'Unclassified device',
        'show_non_vga_unclassified_device': 'Non-VGA unclassified device',
        'show_vga_compatible_unclassified_device': 'VGA compatible unclassified device',
        
        'show_scsi_bus_controller': 'SCSI bus controller',
        'show_ide_interface': 'IDE interface',
        'show_ata_controller_single_dma': 'ATA controller (single DMA)',
        'show_ata_controller_chained_dma': 'ATA controller (chained DMA)',
        'show_ata_controller_other': 'ATA controller (other)',
        'show_floppy_disk_controller': 'Floppy disk controller',
        'show_ipi_bus_controller': 'IPI bus controller',
        'show_raid_bus_controller': 'RAID bus controller',
        'show_ata_controller': 'ATA controller',
        'show_serial_ata_controller': 'Serial ATA controller',
        'show_serial_ata_controller_ahci_1_0': 'Serial ATA controller (AHCI 1.0)',
        'show_serial_ata_controller_vendor_specific': 'Serial ATA controller (vendor specific)',
        'show_serial_attached_scsi_controller': 'Serial Attached SCSI controller',
        'show_non_volatile_memory_controller': 'Non-Volatile memory controller',
        'show_nvmhci_controller': 'NVMHCI controller',
        'show_nvm_express_controller': 'NVM Express controller',
        'show_other_mass_storage_controller': 'Other mass storage controller',
        
        'show_ethernet_controller': 'Ethernet controller',
        'show_token_ring_network_controller': 'Token ring network controller',
        'show_fddi_network_controller': 'FDDI network controller',
        'show_atm_network_controller': 'ATM network controller',
        'show_isdn_controller': 'ISDN controller',
        'show_worldfip_controller': 'WorldFip controller',
        'show_picmg_2_14_multi_computing': 'PICMG 2.14 Multi Computing',
        'show_infiniband_controller': 'Infiniband controller',
        'show_fabric_controller': 'Fabric controller',
        'show_other_network_controller': 'Other network controller',
        
        'show_vga_compatible_controller': 'VGA compatible controller',
        'show_xga_controller': 'XGA controller',
        'show_3d_controller': '3D controller',
        'show_other_display_controller': 'Other display controller',
        
        'show_multimedia_video_controller': 'Multimedia video controller',
        'show_multimedia_video_controller_vga': 'Multimedia video controller (VGA)',
        'show_audio_device': 'Audio device',
        'show_audio_device_hd_audio': 'Audio device (HD Audio)',
        'show_other_multimedia_device': 'Other multimedia device',
        
        'show_ram_memory': 'RAM memory',
        'show_flash_memory': 'FLASH memory',
        'show_other_memory_controller': 'Other memory controller',
        
        'show_host_bridge': 'Host bridge',
        'show_isa_bridge': 'ISA bridge',
        'show_eisa_bridge': 'EISA bridge',
        'show_mca_bridge': 'MCA bridge',
        'show_pci_to_pci_bridge': 'PCI-to-PCI bridge',
        'show_pci_to_pci_bridge_subtractive_decode': 'PCI-to-PCI bridge (subtractive decode)',
        'show_pcmcia_bridge': 'PCMCIA bridge',
        'show_nubus_bridge': 'NuBus bridge',
        'show_cardbus_bridge': 'CardBus bridge',
        'show_raceway_bridge': 'RACEway bridge',
        'show_pci_to_pci_bridge_semi_transparent': 'PCI-to-PCI bridge (semi-transparent)',
        'show_infiniband_to_pci_host_bridge': 'InfiniBand-to-PCI host bridge',
        'show_other_bridge_device': 'Other bridge device',
        
        'show_serial_controller': 'Serial controller',
        'show_parallel_controller': 'Parallel controller',
        'show_multiport_serial_controller': 'Multiport serial controller',
        'show_modem': 'Modem',
        'show_ieee_488_1_2_gpib_controller': 'IEEE 488.1/2 (GPIB) controller',
        'show_smart_card': 'Smart card',
        'show_other_communication_device': 'Other communication device',
        
        'show_pic': 'PIC',
        'show_dma_controller': 'DMA controller',
        'show_timer': 'Timer',
        'show_rtc': 'RTC',
        'show_pci_hot_plug_controller': 'PCI Hot-plug controller',
        'show_sd_host_controller': 'SD Host controller',
        'show_iommu': 'IOMMU',
        'show_root_complex_event_collector': 'Root Complex Event Collector',
        'show_other_base_system_peripheral': 'Other base system peripheral',
        
        'show_keyboard_controller': 'Keyboard controller',
        'show_digitizer': 'Digitizer',
        'show_mouse_controller': 'Mouse controller',
        'show_scanner_controller': 'Scanner controller',
        'show_gameport_controller': 'Gameport controller',
        'show_other_input_device': 'Other input device',
        
        'show_generic_docking_station': 'Generic docking station',
        'show_other_docking_station': 'Other docking station',
        
        'show_386_processor': '386 processor',
        'show_486_processor': '486 processor',
        'show_pentium_processor': 'Pentium processor',
        'show_pentium_pro_processor': 'Pentium Pro processor',
        'show_alpha_processor': 'Alpha processor',
        'show_powerpc_processor': 'PowerPC processor',
        'show_mips_processor': 'MIPS processor',
        'show_co_processor': 'Co-processor',
        'show_other_processor': 'Other processor',
        
        'show_firewire_ieee_1394_controller': 'FireWire (IEEE 1394) controller',
        'show_firewire_ieee_1394_controller_ohci': 'FireWire (IEEE 1394) controller (OHCI)',
        'show_access_bus': 'ACCESS.bus',
        'show_ssa': 'SSA',
        'show_usb_uhci_controller': 'USB UHCI controller',
        'show_usb_ohci_controller': 'USB OHCI controller',
        'show_usb_ehci_controller': 'USB EHCI controller',
        'show_usb_xhci_controller': 'USB XHCI controller',
        'show_usb_device_controller': 'USB device controller',
        'show_usb_controller_unified': 'USB controller (unified)',
        'show_fibre_channel': 'Fibre Channel',
        'show_smbus': 'SMBus',
        'show_infiniband': 'InfiniBand',
        'show_ipmi_smic_interface': 'IPMI SMIC interface',
        'show_ipmi_keyboard_controller_style_interface': 'IPMI Keyboard Controller Style interface',
        'show_ipmi_block_transfer_interface': 'IPMI Block Transfer interface',
        'show_sercos_interface_iec_61491': 'SERCOS interface (IEC 61491)',
        'show_canbus': 'CANbus',
        'show_i3c_controller': 'I3C controller',
        'show_other_serial_bus_controller': 'Other serial bus controller',
        
        'show_irda_compatible_controller': 'iRDA compatible controller',
        'show_consumer_ir_controller': 'Consumer IR controller',
        'show_rf_controller': 'RF controller',
        'show_bluetooth_controller': 'Bluetooth controller',
        'show_broadband_controller': 'Broadband controller',
        'show_ethernet_controller_802_11a': 'Ethernet controller (802.11a)',
        'show_ethernet_controller_802_11b': 'Ethernet controller (802.11b)',
        'show_cellular_controller': 'Cellular controller',
        'show_ethernet_controller_802_11abg': 'Ethernet controller (802.11abg)',
        'show_ethernet_controller_802_11n': 'Ethernet controller (802.11n)',
        'show_other_wireless_controller': 'Other wireless controller',
        'show_multi_function_wireless_controller': 'Multi-function wireless controller',
        
        'show_i2o_controller': 'I2O controller',
        'show_other_intelligent_i_o_controller': 'Other intelligent I/O controller',
        
        'show_satellite_tv_controller': 'Satellite TV controller',
        'show_satellite_audio_controller': 'Satellite audio controller',
        'show_satellite_voice_controller': 'Satellite voice controller',
        'show_satellite_data_controller': 'Satellite data controller',
        'show_other_satellite_communication_controller': 'Other satellite communication controller',
        
        'show_network_and_computing_encryption_device': 'Network and computing encryption device',
        'show_entertainment_encryption_device': 'Entertainment encryption device',
        'show_other_encryption_controller': 'Other encryption controller',
        
        'show_dpio_modules': 'DPIO modules',
        'show_performance_counters': 'Performance counters',
        'show_communication_synchronizer': 'Communication synchronizer',
        'show_signal_processing_management': 'Signal processing management',
        'show_other_signal_processing_controller': 'Other signal processing controller',
        
        'show_processing_accelerator': 'Processing accelerator',
        'show_other_processing_accelerator': 'Other processing accelerator',
        
        'show_non_essential_instrumentation_function': 'Non-Essential Instrumentation Function',
    }
    
    for filter_var, class_label in filter_mappings.items():
        if filter_var in current_module and current_module[filter_var]:
            active_filters.append(class_label)
    
    return active_filters
