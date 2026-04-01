# Firmware and Software

Documentation for the AERIS-10N firmware and software stack.

---

## 📊 System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                  FIRMWARE & SOFTWARE STACK                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Host PC Software                      │    │
│  │  (Python GUI, Data Display, Control Panel)              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                    10G Ethernet / USB 3.0                        │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     FPGA Firmware                        │    │
│  │  (Waveform Gen, Beamforming, DSP, USB/Eth Interface)    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                    SPI / GPIO / I2C                              │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     MCU Firmware                         │    │
│  │  (System Control, Configuration, Sensors, Monitoring)   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ FPGA Firmware

### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      FPGA (XC7A50T)                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Ethernet   │  │   USB 3.0   │  │    JTAG     │             │
│  │  Interface  │  │  Interface  │  │   Debug     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Chirp     │  │  Beamformer │  │    DSP      │             │
│  │  Generator  │  │   Control   │  │  (FFT/CFAR) │             │
│  │  (DDS/NCO)  │  │  (ADAR1000) │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    DAC      │  │    ADC      │  │   Memory    │             │
│  │  Interface  │  │  Interface  │  │  (FIFO/DDR) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐                               │
│  │    MCU      │  │   Clock     │                               │
│  │  Interface  │  │  Management │                               │
│  │  (SPI/I2C)  │  │   (MMCM)    │                               │
│  └─────────────┘  └─────────────┘                               │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Modules

| Module | Function | Language |
|--------|----------|----------|
| **Ethernet Core** | 10G UDP streaming | Verilog (alexforencich) |
| **USB Core** | USB 3.0 bulk transfer | Verilog (FT601) |
| **Chirp Generator** | DDS/NCO waveform generation | Verilog |
| **Beamformer** | Phase/amplitude control | Verilog |
| **DSP** | FFT, pulse compression, CFAR | Verilog/VHDL |
| **DAC Interface** | 125 MSPS data path | Verilog |
| **ADC Interface** | 500 MSPS capture | Verilog |
| **MCU Interface** | SPI/I2C/GPIO control | Verilog |

### Resource Utilization (Estimated)

| Resource | Used | Available | Utilization |
|----------|------|-----------|-------------|
| **LUT** | ~35,000 | 63,400 | ~55% |
| **FF** | ~25,000 | 126,800 | ~20% |
| **BRAM** | ~150 | 270 | ~55% |
| **DSP48** | ~80 | 240 | ~33% |

---

## 📟 MCU Firmware

### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                  MCU (STM32F746ZGT7)                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   System    │  │   Power     │  │   Sensor    │             │
│  │   Control   │  │  Management │  │  Monitoring │             │
│  │   (Main)    │  │ (Sequencing)│  │ (I2C/SPI)   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │     RF      │  │   Clock     │  │   External  │             │
│  │  Control    │  │  Control    │  │  Interfaces │             │
│  │ (ADAR/LO)   │  │  (AD9523)   │  │ (ETH/USB)   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐                               │
│  │  Calibration│  │    Safety   │                               │
│  │   Control   │  │  (Protection)│                              │
│  └─────────────┘  └─────────────┘                               │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Modules

| Module | Function | Interface |
|--------|----------|-----------|
| **System Control** | Main state machine | — |
| **Power Management** | Voltage rail sequencing | GPIO |
| **Sensor Monitoring** | Temperature, voltage, current | I2C/SPI |
| **RF Control** | ADAR1000, ADF4382 configuration | SPI |
| **Clock Control** | AD9523 configuration | SPI |
| **External Interfaces** | Ethernet, USB handling | MAC/PHY |
| **Calibration** | CAL tone, correction table | SPI/ADC |
| **Safety** | Over-current, over-temp protection | GPIO/ADC |

### Memory Map

| Region | Size | Usage |
|--------|------|-------|
| **Flash** | 1 MB | Firmware, calibration tables |
| **SRAM** | 340 KB | Runtime data, buffers |
| **EEPROM** | 64 KB | Persistent configuration |

---

## 🖥️ Host PC Software

### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Host PC Software                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │     GUI     │  │   Data      │  │   Control   │             │
│  │  (PyQt/Tk)  │  │  Display    │  │   Panel     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Network   │  │   Data      │  │   File      │             │
│  │   Stack     │  │  Processing │  │   I/O       │             │
│  │ (UDP/USB)   │  │  (FFT/CFAR) │  │ (HDF5/MAT)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Features

| Feature | Description |
|---------|-------------|
| **GUI** | Python-based (PyQt/Tkinter) |
| **Data Display** | Real-time spectrum, waterfall, range profile |
| **Control Panel** | Frequency, bandwidth, beam steering |
| **Network Stack** | 10G UDP receiver, USB 3.0 fallback |
| **Data Processing** | FFT, CFAR, tracking (optional) |
| **File I/O** | HDF5, MATLAB format export |

---

## 🔗 Communication Protocols

### Ethernet (UDP Streaming)

```
Packet Format:
┌────────────────────────────────────────┐
│ Destination MAC (6 bytes)              │
├────────────────────────────────────────┤
│ Source MAC (6 bytes)                   │
├────────────────────────────────────────┤
│ EtherType (2 bytes) = 0x0800           │
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

### USB 3.0 (Bulk Transfer)

```
Transfer Format:
┌────────────────────────────────────────┐
│ USB 3.0 Packet Header                  │
├────────────────────────────────────────┤
│ Bulk Endpoint Data                     │
├────────────────────────────────────────┤
│ ADC Samples                            │
├────────────────────────────────────────┤
│ CRC                                    │
└────────────────────────────────────────┘
```

### SPI (MCU ↔ FPGA, MCU ↔ Peripherals)

| Signal | Direction | Description |
|--------|-----------|-------------|
| **SCLK** | MCU → Peripheral | Serial Clock |
| **MOSI** | MCU → Peripheral | Master Out Slave In |
| **MISO** | Peripheral → MCU | Master In Slave Out |
| **CS** | MCU → Peripheral | Chip Select |

### I2C (MCU ↔ Sensors)

| Signal | Direction | Description |
|--------|-----------|-------------|
| **SDA** | Bidirectional | Serial Data |
| **SCL** | MCU → Peripheral | Serial Clock |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[External Interfaces]] - Physical interface details
- [[Testing and Validation]] - Firmware/software testing

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
