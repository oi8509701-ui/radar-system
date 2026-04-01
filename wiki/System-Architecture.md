# System Architecture

This page provides a complete overview of the AERIS-10N system architecture.

---

## 📐 Architecture Overview

```
                              ┌─────────────────────────────┐
                              │          HOST PC            │
                              │ Beam steering / UI / logs   │
                              └──────────────┬──────────────┘
                                             │ Ethernet / USB
                                             ▼
                              ┌─────────────────────────────┐
                              │         MAIN FPGA           │
                              │ XC7A50T-2FTG256             │
                              │ Waveform / control / DSP    │
                              └───────┬─────────┬───────────┘
                                      │         │
                             SPI cfg  │         │ IF / ADC data
                                      ▼         ▼
                         ┌─────────────────┐   ┌─────────────────┐
                         │ Tile Sync Ctrl  │   │   RX/DSP path   │
                         │ CLK / SYNC / CS │   │ ADC / FPGA merge │
                         └────────────────┘   ─────────────────┘
                                │
                    100 MHz ref │ SYNC / TRX / CS
                                ▼
          ┌──────────────────────────────────────────────────────────────┐
          │                        16 TILES                              │
          │                                                              │
          │  Tile 1    Tile 2    Tile 3   ...                Tile 16    │
          │ ┌───────┐ ┌───────┐ ┌───────┐                    ┌───────┐   │
          │ │Ref in │ │Ref in │ │Ref in │                    │Ref in │   │
          │ │PLL/LO │ │PLL/LO │ │PLL/LO │                    │PLL/LO │   │
          │ │ADAR   │ │ADAR   │ │ADAR   │                    │ADAR   │   │
          │ │TX/RX  │ │TX/RX  │ │TX/RX  │                    │TX/RX  │   │
          │ │4×4 AF │ │4×4 AF │ │4×4 AF │                    │4×4 AF │   │
          │ └──┬────┘ └──┬────┘ └──┬────┘                    └──┬────┘   │
          └────┼──────────────────┼─────────────────────────────┼────────┘
               │         │         │                             │
               └─────────┴─────────┴───── RX IF / subarray ─────┘
                                       │
                                       ▼
                           ┌──────────────────────────┐
                           │ Hybrid RX Combining      │
                           │ per tile / per subarray  │
                           └────────────┬─────────────┘
                                        ▼
                                  ADC / FPGA DSP
```

---

## 🎯 Key Design Decisions

### 1. LO Topology

**Decision:** Master reference + local PLL per tile

```
Master reference (100 MHz from AD9523)
         ↓
Local ADF4382 LO on each tile
         ↓
Phase calibration
```

**Rationale:**
- Avoids distributing 10.5 GHz across 16 paths (high loss, phase mismatch)
- Easier to scale
- Simpler calibration

---

### 2. TX/RX Synchronization

**Decision:** Hardware SYNC line

```
SPI loads configuration
         ↓
GPIO SYNC line switches all 16 tiles simultaneously
```

**Rationale:**
- All tiles switch at the same time (no skew)
- Deterministic timing
- Simple implementation

---

### 3. RX Combining

**Decision:** Hybrid approach

```
16 Tiles → 4× ADAR1000 → Combiner → ADC → FPGA
              (analog)              (digital)
```

**Rationale:**
- Compromise between analog (lossy) and full digital (expensive)
- Fewer ADC channels required
- Maintains beamforming flexibility

---

### 4. Calibration

**Decision:** Built-in calibration loop

```
CAL Tone Generator (10.5 GHz)
         ↓
1-to-16 coupler → All tiles
         ↓
ADC measurement → FPGA calculates error
         ↓
Correction table in EEPROM
```

**Rationale:**
- Essential for phase coherence
- Compensates for temperature drift
- Corrects component variations

---

## 📦 Major Subsystems

### Control Subsystem

| Component | Model | Function |
|-----------|-------|----------|
| **FPGA** | Xilinx Artix-7 XC7A50T-2FTG256 | Waveform generation, digital beamforming, DSP |
| **MCU** | STMicroelectronics STM32F746ZGT7 | System control, configuration, sensor monitoring |
| **USB 3 PHY** | FTDI FT601Q | USB 3.0 interface (5 Gbps) |

---

### Clock System

| Component | Model | Function |
|-----------|-------|----------|
| **OCXO** | ECOC-2522-10.000-3-F-C | 10 MHz ultra-stable reference |
| **XO** | CCHD-957-100 | 100 MHz low phase noise oscillator |
| **VCXO** | CVHD-950-100.000 | 100 MHz voltage-controlled for PLL |
| **Clock Synth** | Analog Devices AD9523 | Low-jitter clock distribution |

**Clock Frequencies:**

| Signal | Frequency | Destination |
|--------|-----------|-------------|
| CMOS | 120 MHz | DAC (AD9708) |
| LVDS | 400 MHz | ADC (AD9484) |
| CMOS | 100 MHz | FPGA (system/reference) |
| LVDS | 300 MHz | MCU |
| LVDS Sync | 5 MHz | MCU (synchronization) |

---

### LO System

| Component | Model | Function |
|-----------|-------|----------|
| **LO TX** | Analog Devices ADF4382 | 10.5 GHz synthesized LO for TX upconversion |
| **LO RX** | Analog Devices ADF4382 | RX 10.5 GHz ± IF synthesized LO |
| **Balun** | Mini-Circuits MTX2-143+ (×2) | Single-to-differential, IL=1dB |
| **Attenuator PAD** | ATS1005-3DB-FD-T05 (×2) | -3 dB fixed attenuation |

---

### RF Chain

| Component | Model | Function |
|-----------|-------|----------|
| **DAC** | Analog Devices AD9708 | 8-bit, 125 MSPS, IF chirp waveform |
| **Mixer TX/RX** | Linear Technology LTC5552 (×2) | Up/downconversion to/from 10.5 GHz |
| **RF Switch** | Mini-Circuits M3SWA2-34DR+ (×2) | TX/RX path switching, 30 dB isolation |
| **Combiner** | Mini-Circuits EP4RKU+ | 4-way power divider |
| **Beamformer** | Analog Devices ADAR1000 (×4) | 16 channels, phase & amplitude control |
| **Front-End** | Analog Devices ADTR1107 (×16) | TX/RX switch + LNA + PA driver |
| **PA** | Qorvo QPA2962 (×16) | 10W GaN per channel (Extended) |
| **ADC** | Analog Devices AD9484 | 8-bit, 500 MSPS, IF digitization |

---

### Antenna Array

| Parameter | Value |
|-----------|-------|
| **Configuration** | 16 tiles (4×4 grid) |
| **Elements per tile** | 512 (32×16) |
| **Total elements** | 8,192 |
| **Beam steering** | ±45° (electronic) |

---

### PA Control

| Component | Model | Function |
|-----------|-------|----------|
| **CAL DAC** | Analog Devices AD9708 | Calibration tone generation |
| **PA Driver** | Texas Instruments OPA4703NA/250 (×2) | Drives QPA2962 Gate voltage |
| **VD RELAY** | High-voltage relay | Drain voltage switch (28V) |

---

### Monitoring

| Component | Model | Function |
|-----------|-------|----------|
| **Current Sense** | Texas Instruments INA241A3 (×16) | Per-tile PA current monitoring |
| **Monitoring ADC** | Texas Instruments ADS7830 (×3) | 8-bit I2C ADC, voltage monitoring |
| **VSWR Detect** | ×16 | Per-tile reflected power detection |
| **Temp Sensors** | TMP37 (×16) | Per-tile temperature monitoring |

---

### External Interfaces

| Interface | Type | Function |
|-----------|------|----------|
| **10G Ethernet** | XAUI SFP+ | PRIMARY: 10Gbps UDP streaming |
| **USB 3.0** | FT601 | BACKUP: 3.2Gbps local debug |
| **GPIO** | SMA Connectors | PPS/Trigger/Sync |
| **Ext Ref** | 10 MHz SMA | External OCXO/GPSDO |
| **JTAG** | Connector | FPGA debug & programming |

---

## 📊 Signal Flow

### TX Path

```
FPGA → DAC → LPF → Mixer (LO) → BPF → RF Switch → Combiner
       ↓
    ADAR1000 (×4) → ADTR1107 (×16) → QPA2962 (×16)
       ↓
    Circulator (×16) → Antenna Array (16 tiles)
```

### RX Path

```
Antenna Array → Circulator → ADTR1107 → ADAR1000 → RF Switch
       ↓
    BPF → Mixer (LO) → LPF → Opamp → LPF → ADC → FPGA
```

---

## 🔗 Related Pages

- [[Hardware Specifications]] - Complete component details
- [[RF Chain Documentation]] - Detailed TX/RX signal paths
- [[Antenna Array]] - Tile architecture and beamforming
- [[Clock and Timing]] - Clock distribution details

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
