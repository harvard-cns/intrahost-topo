#PCIe Topology Visualizer - Tree-level Filtering Commands

Tree-level filtering: If a tree contains at least one node belonging to the specified classes, include the entire tree.

##Filter by Device Classes

```bash
#GPUs
python3 CLI.py --filter-classes="3D controller"

#NICs
python3 CLI.py --filter-classes="Ethernet controller"

python3 CLI.py --filter-classes="3D controller,Ethernet controller"

python3 CLI.py --filter-classes="Storage controller"

python3 CLI.py --filter-classes="Bridge"

python3 CLI.py --filter-classes="Audio device"

python3 CLI.py --filter-classes="USB controller"

python3 CLI.py --filter-classes="Encryption controller"

python3 CLI.py --filter-classes="Wireless controller"
```

## Class Combinations

```bash
#GPUs OR NICs
python3 CLI.py --filter-classes="3D controller,Ethernet controller"

#GPUs OR storage devices
python3 CLI.py --filter-classes="3D controller,Storage controller"

#any networking devices
python3 CLI.py --filter-classes="Ethernet controller,Wireless controller"

#high-performance devices
python3 CLI.py --filter-classes="3D controller,Storage controller,Encryption controller"
```

## No Filters (Show All Trees)

```bash
python3 CLI.py
```



### Unclassified Devices
- `Unclassified device` - Unclassified devices
- `Non-VGA unclassified device` - Non-VGA unclassified devices
- `VGA compatible unclassified device` - VGA compatible unclassified devices

### Mass Storage Controllers
- `SCSI bus controller` - SCSI bus controllers
- `IDE interface` - IDE interfaces
- `ATA controller (single DMA)` - ATA controllers with single DMA
- `ATA controller (chained DMA)` - ATA controllers with chained DMA
- `ATA controller (other)` - Other ATA controllers
- `Floppy disk controller` - Floppy disk controllers
- `IPI bus controller` - IPI bus controllers
- `RAID bus controller` - RAID bus controllers
- `Serial ATA controller` - Serial ATA controllers
- `Serial ATA controller (AHCI 1.0)` - Serial ATA controllers with AHCI 1.0
- `Serial ATA controller (vendor specific)` - Vendor specific Serial ATA controllers
- `Serial Attached SCSI controller` - Serial Attached SCSI controllers
- `Non-Volatile memory controller` - Non-Volatile memory controllers
- `NVMHCI controller` - NVMHCI controllers
- `NVM Express controller` - NVM Express controllers
- `Other mass storage controller` - Other mass storage controllers

### Network Controllers
- `Ethernet controller` - Ethernet controllers
- `Token ring network controller` - Token ring network controllers
- `FDDI network controller` - FDDI network controllers
- `ATM network controller` - ATM network controllers
- `ISDN controller` - ISDN controllers
- `WorldFip controller` - WorldFip controllers
- `PICMG 2.14 Multi Computing` - PICMG 2.14 Multi Computing controllers
- `Infiniband controller` - Infiniband controllers
- `Fabric controller` - Fabric controllers
- `Other network controller` - Other network controllers

### Display Controllers
- `VGA compatible controller` - VGA compatible controllers
- `XGA controller` - XGA controllers
- `3D controller` - 3D controllers (GPUs)
- `Other display controller` - Other display controllers

### Multimedia Devices
- `Multimedia video controller` - Multimedia video controllers
- `Multimedia video controller (VGA)` - Multimedia video controllers with VGA
- `Audio device` - Audio devices
- `Audio device (HD Audio)` - HD Audio devices
- `Other multimedia device` - Other multimedia devices

### Memory Controllers
- `RAM memory` - RAM memory controllers
- `FLASH memory` - FLASH memory controllers
- `Other memory controller` - Other memory controllers

### Bridge Devices
- `Host bridge` - Host bridges
- `ISA bridge` - ISA bridges
- `EISA bridge` - EISA bridges
- `MCA bridge` - MCA bridges
- `PCI-to-PCI bridge` - PCI-to-PCI bridges
- `PCI-to-PCI bridge (subtractive decode)` - PCI-to-PCI bridges with subtractive decode
- `PCMCIA bridge` - PCMCIA bridges
- `NuBus bridge` - NuBus bridges
- `CardBus bridge` - CardBus bridges
- `RACEway bridge` - RACEway bridges
- `PCI-to-PCI bridge (semi-transparent)` - Semi-transparent PCI-to-PCI bridges
- `InfiniBand-to-PCI host bridge` - InfiniBand-to-PCI host bridges
- `Other bridge device` - Other bridge devices

### Communication Controllers
- `Serial controller` - Serial controllers
- `Parallel controller` - Parallel controllers
- `Multiport serial controller` - Multiport serial controllers
- `Modem` - Modems
- `IEEE 488.1/2 (GPIB) controller` - IEEE 488.1/2 (GPIB) controllers
- `Smart card` - Smart card controllers
- `Other communication device` - Other communication devices

### Base System Peripherals
- `PIC` - Programmable Interrupt Controllers
- `DMA controller` - DMA controllers
- `Timer` - Timer controllers
- `RTC` - Real Time Clock controllers
- `PCI Hot-plug controller` - PCI Hot-plug controllers
- `SD Host controller` - SD Host controllers
- `IOMMU` - IOMMU controllers
- `Root Complex Event Collector` - Root Complex Event Collectors
- `Other base system peripheral` - Other base system peripherals

### Input Devices
- `Keyboard controller` - Keyboard controllers
- `Digitizer` - Digitizers
- `Mouse controller` - Mouse controllers
- `Scanner controller` - Scanner controllers
- `Gameport controller` - Gameport controllers
- `Other input device` - Other input devices

### Docking Stations
- `Generic docking station` - Generic docking stations
- `Other docking station` - Other docking stations

### Processors
- `386 processor` - 386 processors
- `486 processor` - 486 processors
- `Pentium processor` - Pentium processors
- `Pentium Pro processor` - Pentium Pro processors
- `Alpha processor` - Alpha processors
- `PowerPC processor` - PowerPC processors
- `MIPS processor` - MIPS processors
- `Co-processor` - Co-processors
- `Other processor` - Other processors

### Serial Bus Controllers
- `FireWire (IEEE 1394) controller` - FireWire (IEEE 1394) controllers
- `FireWire (IEEE 1394) controller (OHCI)` - FireWire (IEEE 1394) OHCI controllers
- `ACCESS.bus` - ACCESS.bus controllers
- `SSA` - SSA controllers
- `USB UHCI controller` - USB UHCI controllers
- `USB OHCI controller` - USB OHCI controllers
- `USB EHCI controller` - USB EHCI controllers
- `USB XHCI controller` - USB XHCI controllers
- `USB device controller` - USB device controllers
- `USB controller (unified)` - Unified USB controllers
- `Fibre Channel` - Fibre Channel controllers
- `SMBus` - SMBus controllers
- `InfiniBand` - InfiniBand controllers
- `IPMI SMIC interface` - IPMI SMIC interfaces
- `IPMI Keyboard Controller Style interface` - IPMI Keyboard Controller Style interfaces
- `IPMI Block Transfer interface` - IPMI Block Transfer interfaces
- `SERCOS interface (IEC 61491)` - SERCOS interfaces
- `CANbus` - CANbus controllers
- `I3C controller` - I3C controllers
- `Other serial bus controller` - Other serial bus controllers

### Wireless Controllers
- `iRDA compatible controller` - iRDA compatible controllers
- `Consumer IR controller` - Consumer IR controllers
- `RF controller` - RF controllers
- `Bluetooth controller` - Bluetooth controllers
- `Broadband controller` - Broadband controllers
- `Ethernet controller (802.11a)` - 802.11a Ethernet controllers
- `Ethernet controller (802.11b)` - 802.11b Ethernet controllers
- `Cellular controller` - Cellular controllers
- `Ethernet controller (802.11abg)` - 802.11abg Ethernet controllers
- `Ethernet controller (802.11n)` - 802.11n Ethernet controllers
- `Other wireless controller` - Other wireless controllers
- `Multi-function wireless controller` - Multi-function wireless controllers

### Intelligent I/O Controllers
- `I2O controller` - I2O controllers
- `Other intelligent I/O controller` - Other intelligent I/O controllers

### Satellite Communication Controllers
- `Satellite TV controller` - Satellite TV controllers
- `Satellite audio controller` - Satellite audio controllers
- `Satellite voice controller` - Satellite voice controllers
- `Satellite data controller` - Satellite data controllers
- `Other satellite communication controller` - Other satellite communication controllers

### Encryption Controllers
- `Network and computing encryption device` - Network and computing encryption devices
- `Entertainment encryption device` - Entertainment encryption devices
- `Other encryption controller` - Other encryption controllers

### Signal Processing Controllers
- `DPIO modules` - DPIO modules
- `Performance counters` - Performance counters
- `Communication synchronizer` - Communication synchronizers
- `Signal processing management` - Signal processing management controllers
- `Other signal processing controller` - Other signal processing controllers

### Processing Accelerators
- `Processing accelerator` - Processing accelerators
- `Other processing accelerator` - Other processing accelerators

### Non-Essential Instrumentation Functions
- `Non-Essential Instrumentation Function` - Non-Essential Instrumentation Functions