# Power System

Documentation for the AERIS-10N power distribution system.

---

## 📊 Power Distribution Tree

```
Power Input (XT30)
12-24V DC, 30A
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                    Power Distribution Board               │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  DC/DC #1   │  │  DC/DC #2   │  │  DC/DC #3   │      │
│  │  TPS5430    │  │  TPS5420    │  │  LT8610     │      │
│  │  3A         │  │  2A         │  │  3.5A       │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  LDO #1     │  │  LDO #2     │  │  LDO #3     │      │
│  │  TPS7a8300  │  │  ADM7150    │  │  ADM7151    │      │
│  │  3A         │  │  800mA      │  │  800mA      │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                           │
└──────────────────────────────────────────────────────────┘
       │
       ├──────────────────┬──────────────────┬─────────────┐
       ▼                  ▼                  ▼             ▼
  VIN_MAIN           VIN_RF             VIN_PA        Other
  12-24V, 10A        12-24V, 5A         12-28V, 25A   
       │                  │                  │
       ▼                  ▼                  ▼
   FPGA, MCU         Clock, LO         QPA2962
   Digital           RF Analog         (Extended)
```

---

## ⚡ Voltage Rails

### Main Power Rails

| Rail | Voltage | Current | Power | Destination |
|------|---------|---------|-------|-------------|
| **VIN_MAIN** | 12-24V | 10A | 120-240W | FPGA, MCU, Digital logic |
| **VIN_RF** | 12-24V | 5A | 60-120W | Clock synthesizer, LO, ADAR |
| **VIN_PA** | 12-28V | 25A | 300-700W | QPA2962 power amplifiers |

### Derived Rails

| Rail | Voltage | Current | Source | Destination |
|------|---------|---------|--------|-------------|
| **1V0_FPGA** | 1.0V | 4A | DC/DC | FPGA core |
| **1V8_AUX** | 1.8V | 1A | LDO | FPGA I/O, AUX |
| **2V5_ANA** | 2.5V | 1A | LDO | Analog circuits |
| **3V3_DIG** | 3.3V | 2A | LDO | Digital logic |
| **3V3_RF** | 3.3V | 1A | LDO | RF circuits |
| **5V0_IO** | 5V | 2A | DC/DC | IO interfaces |
| **1V2_SYNTH** | 1.2V | 500mA | LDO | Clock synthesizer |
| **3V3_LO** | 3.3V | 500mA | LDO | LO synthesizers |

---

## 🔌 Power Sequencing

### Startup Sequence

```
T=0ms:    VIN_MAIN applied
          │
          ▼
T=10ms:   1V0_FPGA enabled
          │
          ▼
T=20ms:   1V8_AUX enabled
          │
          ▼
T=30ms:   3V3_DIG enabled
          │
          ▼
T=40ms:   VIN_RF applied
          │
          ▼
T=50ms:   1V2_SYNTH enabled
          │
          ▼
T=60ms:   3V3_LO enabled
          │
          ▼
T=100ms:  VIN_PA applied (if Extended)
          │
          ▼
T=500ms:  PGOOD asserted
          │
          ▼
          System ready
```

### Shutdown Sequence

```
1. Deassert PGOOD
   │
   ▼
2. Disable VIN_PA
   │
   ▼
3. Disable 3V3_LO
   │
   ▼
4. Disable 1V2_SYNTH
   │
   ▼
5. Disable VIN_RF
   │
   ▼
6. Disable 3V3_DIG
   │
   ▼
7. Disable 1V8_AUX
   │
   ▼
8. Disable 1V0_FPGA
   │
   ▼
9. Disable VIN_MAIN
```

---

## 🛡️ Protection Mechanisms

### Over-Current Protection

| Rail | Protection | Threshold | Action |
|------|------------|-----------|--------|
| **VIN_MAIN** | Current sense + fuse | 12A | Shutdown |
| **VIN_RF** | Current sense | 6A | Shutdown |
| **VIN_PA** | Current sense (per-tile) | 1.5A per tile | Shutdown affected tile |
| **1V0_FPGA** | DC/DC internal | 5A | Current limit |
| **3V3_DIG** | LDO internal | 3A | Current limit |

### Over-Voltage Protection

| Rail | Protection | Threshold | Action |
|------|------------|-----------|--------|
| **VIN_MAIN** | TVS diode | 30V | Clamp |
| **VIN_PA** | OVP circuit | 32V | Shutdown |
| **1V0_FPGA** | DC/DC internal | 1.2V | Shutdown |

### Under-Voltage Lockout (UVLO)

| Rail | UVLO Threshold | Action |
|------|----------------|--------|
| **VIN_MAIN** | <10V | Disable outputs |
| **VIN_RF** | <10V | Disable outputs |
| **VIN_PA** | <10V | Disable outputs |
| **1V0_FPGA** | <0.9V | Power good deassert |

---

## 🌡️ Thermal Management

### Power Dissipation

| Subsystem | Power Dissipation | Cooling Method |
|-----------|-------------------|----------------|
| **FPGA** | ~3-5W | Heatsink + airflow |
| **QPA2962 (×16)** | ~500-700W (total) | Forced air + heatsink |
| **DC/DC converters** | ~20-30W | PCB copper + airflow |
| **LDOs** | ~10-15W | PCB copper |

### Cooling Requirements

| Component | Max Temperature | Required Airflow |
|-----------|-----------------|------------------|
| **FPGA** | 85°C | 200 LFM |
| **QPA2962** | 150°C (junction) | 400 LFM |
| **DC/DC** | 125°C | 200 LFM |
| **LDO** | 125°C | 100 LFM |

### Fan Control

| Temperature | Fan Speed |
|-------------|-----------|
| **<40°C** | Off |
| **40-50°C** | 25% |
| **50-60°C** | 50% |
| **60-70°C** | 75% |
| **>70°C** | 100% |

---

## 📊 Power Monitoring

### Monitored Parameters

| Parameter | Sensor | Location | Purpose |
|-----------|--------|----------|---------|
| **VIN_MAIN current** | INA219 | Power board | System power monitoring |
| **VIN_PA current** | INA241A3 (×16) | Per-tile | PA protection |
| **Tile temperatures** | TMP37 (×16) | Per-tile | Thermal management |
| **Rail voltages** | ADS7830 (×3) | Power board | Voltage monitoring |

### Monitoring Interface

```
INA241A3 (×16) ──┐
                 │
ADS7830 (×3) ────┼──→ MCU (STM32F746)
                 │                      │
TMP37 (×16) ─────                      ▼
                              I2C / SPI
                              Host PC
```

---

## 🔌 Connectors

### Power Input

| Connector | Type | Rating |
|-----------|------|--------|
| **J6** | XT30 | 12-24V, 30A |

### Power Output (to subsystems)

| Connector | Type | Pins | Function |
|-----------|------|------|----------|
| **J3** | 2×(2×1) | 4 | To LOs (+5V0, +3V3_LO, GND) |
| **J4** | 2×(2×1) | 4 | To Clock Synth (+1V8, +3V3) |
| **J5** | 2×1 | 2 | To XOs (+3V3_XO, GND) |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[Hardware Specifications]] - Component details
- [[Assembly Guide]] - Power system assembly

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
