# External Interfaces

Documentation for the AERIS-10N external interfaces.

---

## 📊 Interface Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTERFACES                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ 10G ETH    │  │  USB 3.0   │  │   GPIO     │                │
│  │ (PRIMARY)  │  │  (BACKUP)  │  │   (SMA)    │                │
│  │ XAUI SFP+  │  │   FT601    │  │  PPS/Trig  │                │
│  └────────────┘  └────────────┘  └────────────┘                │
│                                                                   │
│  ┌────────────┐  ┌────────────┐                                 │
│  │  Ext Ref   │  │   JTAG     │                                 │
│  │  10 MHz    │  │  Debug     │                                 │
│  │   (SMA)    │  │ (Connector)│                                 │
│  └────────────┘  └────────────┘                                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔗 10 Gigabit Ethernet (PRIMARY)

### Specifications

| Parameter | Value |
|-----------|-------|
| **Interface** | XAUI SFP+ |
| **Speed** | 10 Gbps |
| **Protocol** | UDP streaming |
| **Core** | alexforencich verilog-ethernet |
| **FPGA** | Xilinx Artix-7 XC7A50T |

### Pinout (SFP+ Connector)

| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | VeeT | Transmitter Ground |
| 2 | TX Fault | Transmitter Fault |
| 3 | TX Disable | Transmitter Disable |
| 4 | SDA | 2-Wire Serial Interface Data |
| 5 | SCL | 2-Wire Serial Interface Clock |
| 6 | MOD_ABS | Module Absent |
| 7 | RS | Receiver Inverse Serial Data |
| 8 | RD- | Receiver Inverse Data |
| 9 | RD+ | Receiver Non-Inverse Data |
| 10 | VeeR | Receiver Ground |
| 11 | VeeR | Receiver Ground |
| 12 | TD+ | Transmitter Non-Inverse Data |
| 13 | TD- | Transmitter Inverse Data |
| 14 | VeeT | Transmitter Ground |
| 15 | VeeT | Transmitter Ground |
| 16 | VeeR | Receiver Ground |
| 17 | TD Fault | Transmitter Fault |
| 18 | TD Disable | Transmitter Disable |
| 19 | SDA | 2-Wire Serial Interface Data |
| 20 | SCL | 2-Wire Serial Interface Clock |

### Data Format

```
UDP Packet Structure:
┌────────────────────────────────────────┐
│ Ethernet Header (14 bytes)             │
├────────────────────────────────────────┤
│ IP Header (20 bytes)                   │
├────────────────────────────────────────┤
│ UDP Header (8 bytes)                   │
├────────────────────────────────────────┤
│ Payload (ADC samples, metadata)        │
├────────────────────────────────────────┤
│ CRC (4 bytes)                          │
└────────────────────────────────────────┘
```

---

## 🔗 USB 3.0 (BACKUP)

### Specifications

| Parameter | Value |
|-----------|-------|
| **Interface** | USB 3.0 Type-B |
| **Chip** | FTDI FT601Q |
| **Speed** | 3.2 Gbps (USB 3.0) |
| **Mode** | Bulk transfer |
| **Use case** | Local debug, close range |

### Pinout (USB 3.0 Type-B)

| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | VBUS | +5V Power |
| 2 | D- | USB 2.0 Differential - |
| 3 | D+ | USB 2.0 Differential + |
| 4 | GND | Ground |
| 5 | StdA_SSRX- | USB 3.0 RX - |
| 6 | StdA_SSRX+ | USB 3.0 RX + |
| 7 | StdA_SSTX- | USB 3.0 TX - |
| 8 | StdA_SSTX+ | USB 3.0 TX + |
| 9 | GND | Ground |

---

## 🔗 GPIO (SMA Connectors)

### Specifications

| Parameter | Value |
|-----------|-------|
| **Connector** | SMA |
| **Voltage** | 3.3V LVCMOS |
| **Current** | 8 mA (sink/source) |
| **FPGA** | Dedicated GPIO pins |

### Signals

| Signal | Direction | Description |
|--------|-----------|-------------|
| **PPS** | Input | Pulse Per Second (timing sync) |
| **Trigger** | Input | External trigger input |
| **Sync** | Output | System synchronization output |

---

## 🔗 External Reference Input

### Specifications

| Parameter | Value |
|-----------|-------|
| **Connector** | SMA |
| **Frequency** | 10 MHz |
| **Level** | 0 to +10 dBm |
| **Impedance** | 50 Ω |
| **Destination** | AD9523 (clock synthesizer) |

### Use Cases

| Use Case | Description |
|----------|-------------|
| **External OCXO** | Higher stability reference |
| **GPSDO** | GPS-disciplined oscillator |
| **System sync** | Multi-radar synchronization |

---

## 🔗 JTAG

### Specifications

| Parameter | Value |
|-----------|-------|
| **Connector** | 14-pin JTAG |
| **Voltage** | 3.3V |
| **FPGA** | XC7A50T JTAG interface |
| **Use case** | FPGA programming, debug |

### Pinout

| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | TCK | Test Clock |
| 2 | GND | Ground |
| 3 | TDO | Test Data Out |
| 4 | NC | Not Connected |
| 5 | TMS | Test Mode Select |
| 6 | GND | Ground |
| 7 | TDI | Test Data In |
| 8 | GND | Ground |
| 9 | NC | Not Connected |
| 10 | GND | Ground |
| 11 | NC | Not Connected |
| 12 | GND | Ground |
| 13 | NC | Not Connected |
| 14 | GND | Ground |

---

## 📊 Interface Comparison

| Interface | Speed | Use Case | Priority |
|-----------|-------|----------|----------|
| **10G Ethernet** | 10 Gbps | Primary data transfer | PRIMARY |
| **USB 3.0** | 3.2 Gbps | Backup, local debug | BACKUP |
| **GPIO** | 100 Mbps | Timing, triggers | Auxiliary |
| **Ext Ref** | 10 MHz | Reference clock | Auxiliary |
| **JTAG** | 10 Mbps | Programming, debug | Debug only |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[Firmware and Software]] - Communication protocols
- [[Clock and Timing]] - External reference details

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
