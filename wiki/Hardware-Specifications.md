# Hardware Specifications

Complete hardware specifications for the AERIS-10N radar system.

---

## 📋 Bill of Materials (BOM)

### Control Subsystem

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| U1 | FPGA | XC7A50T-2FTG256 | Xilinx | 1 | FTG256 |
| U2 | MCU | STM32F746ZGT7 | STMicroelectronics | 1 | LQFP144 |
| U3 | USB 3 PHY | FT601Q | FTDI | 1 | QFP48 |

---

### Clock System

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| Y1 | OCXO | ECOC-2522-10.000-3-F-C | ECS Inc | 1 | — |
| Y2 | XO | CCHD-957-100 | Crystek | 1 | — |
| Y3 | VCXO | CVHD-950-100.000 | Crystek | 1 | — |
| U4 | Clock Synth | AD9523-1 | Analog Devices | 1 | 64-LFCSP |

---

### LO System

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| U5 | LO TX | ADF4382ABCCZ | Analog Devices | 1 | 32-LFCSP |
| U6 | LO RX | ADF4382ABCCZ | Analog Devices | 1 | 32-LFCSP |
| T1 | Balun | MTX2-143+ | Mini-Circuits | 2 | — |
| ATT1 | Attenuator | ATS1005-3DB-FD-T05 | Mini-Circuits | 2 | 0402 |

---

### RF Chain

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| U7 | DAC | AD9708 | Analog Devices | 1 | LQFP48 |
| U8 | Mixer TX | LTC5552IUDB#TRMPBF | Linear Technology | 1 | 20-DFN |
| U9 | Mixer RX | LTC5552IUDB#TRMPBF | Linear Technology | 1 | 20-DFN |
| SW1 | RF Switch TX | M3SWA2-34DR+ | Mini-Circuits | 1 | — |
| SW2 | RF Switch RX | M3SWA2-34DR+ | Mini-Circuits | 1 | — |
| U10 | Combiner | EP4RKU+ | Mini-Circuits | 1 | — |
| U11-U14 | Beamformer | ADAR1000 | Analog Devices | 4 | LGA40 |
| U15-U30 | Front-End | ADTR1107 | Analog Devices | 16 | LGA24 |
| U31-U46 | PA | QPA2962 | Qorvo | 16 | DFN6 |
| U47 | ADC | AD9484 | Analog Devices | 1 | TQFP128 |

---

### PA Control

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| U48 | CAL DAC | AD9708 | Analog Devices | 1 | LQFP48 |
| U49-U50 | PA Driver | OPA4703NA/250 | Texas Instruments | 2 | SOT23-5 |
| K1 | VD RELAY | High-voltage relay | — | 1 | — |

---

### Monitoring

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| U51-U66 | Current Sense | INA241A3 | Texas Instruments | 16 | — |
| U67-U69 | Monitoring ADC | ADS7830 | Texas Instruments | 3 | TSSOP16 |
| U70-U85 | VSWR Detect | — | — | 16 | — |
| U86-U101 | Temp Sensor | TMP37 | Analog Devices | 16 | SOT23 |

---

### Sensors & Misc

| Ref | Component | Model | Manufacturer | Qty | Package |
|-----|-----------|-------|--------------|-----|---------|
| U102 | IMU | GY-85 | — | 1 | — |
| U103 | Barometer | BMP180 | Bosch | 1 | — |
| U104 | GPS | NEO-6M | u-blox | 1 | — |
| U105 | Stepper Driver | TBS6600 | Texas Instruments | 1 | — |

---

## 🔌 Connectors

| Ref | Type | Pins | Function |
|-----|------|------|----------|
| J1 | 6×2 Header | 12 | To Microcontroller (Control signals) |
| J2 | 7×2 Header | 14 | To Microcontroller (300 MHz LVDS + 5 MHz Sync) |
| J3 | 2×(2×1) Power | 4 | To LOs (+5V0, +3V3_LO, GND) |
| J4 | 2×(2×1) Power | 4 | To Clock Synth (+1V8_CLOCK, +3V3_CLOCK) |
| J5 | 2×1 Power | 2 | To XOs (+3V3_XO, GND) |
| J6 | XT30 | 2 | Power Input (12-24V, 30A) |
| J7 | XAUI SFP+ | 20 | 10G Ethernet |
| J8 | USB 3.0 Type-B | 9 | USB 3.0 Backup |
| J9 | SMA | 1 | GPIO (PPS/Trigger) |
| J10 | SMA | 1 | Ext Ref (10 MHz) |
| J11 | Connector | 14 | JTAG |

---

## 📐 PCB Specifications

### Main Board

| Parameter | Value |
|-----------|-------|
| **Dimensions** | TBD |
| **Layers** | 8-10 layers |
| **Material** | FR-4 / Rogers RO4350B (RF sections) |
| **Thickness** | 1.6 mm |
| **Copper** | 1 oz (35 μm) |
| **Surface Finish** | ENIG |
| **Impedance Control** | 50Ω RF traces, 100Ω differential |

### Tile Boards (×16)

| Parameter | Value |
|-----------|-------|
| **Dimensions** | ~73 × 73 mm per tile |
| **Layers** | 4-6 layers |
| **Material** | Rogers RO4350B |
| **Thickness** | 0.762 mm |
| **Copper** | 1 oz (35 μm) |
| **Surface Finish** | ENIG |

---

## ⚡ Power Requirements

### Voltage Rails

| Rail | Voltage | Current | Power | Notes |
|------|---------|---------|-------|-------|
| **VIN_MAIN** | 12-24V | 10A | 120-240W | FPGA, MCU, Digital |
| **VIN_RF** | 12-24V | 5A | 60-120W | Clock, LO, ADAR |
| **VIN_PA** | 12-28V | 25A | 300-700W | QPA2962 (Extended) |
| **1V0_FPGA** | 1.0V | 4A | 4W | FPGA Core |
| **1V8_AUX** | 1.8V | 1A | 1.8W | FPGA I/O, AUX |
| **2V5_ANA** | 2.5V | 1A | 2.5W | Analog |
| **3V3_DIG** | 3.3V | 2A | 6.6W | Digital |
| **3V3_RF** | 3.3V | 1A | 3.3W | RF |
| **5V0_IO** | 5V | 2A | 10W | IO |

**Total Power:** ~500-940W (depending on configuration)

---

## 🌡️ Environmental Specifications

| Parameter | Value |
|-----------|-------|
| **Operating Temperature** | -20°C to +60°C |
| **Storage Temperature** | -40°C to +85°C |
| **Humidity** | 5% to 95% (non-condensing) |
| **Cooling** | Forced air (fans + heatsink) |

---

## 📊 Mechanical Specifications

| Parameter | Value |
|-----------|-------|
| **Full Array Size** | ~2.5m × ~1.3m |
| **Tile Size** | ~73mm × 73mm |
| **Weight** | TBD |
| **Mounting** | M3 standoffs (4 per tile) |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[Assembly Guide]] - How to assemble the hardware
- [[Power System]] - Detailed power distribution

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
