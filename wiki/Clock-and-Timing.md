# Clock and Timing

Documentation for the AERIS-10N clock distribution and timing system.

---

## 📊 Clock Tree

```
┌──────────────────────────────────────────────────────────────────┐
│                      CLOCK DISTRIBUTION                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  OCXO (ECOC-2522)                                                │
│  10 MHz                                                          │
│       │                                                           │
│       ├──────────────────┐                                       │
│       │                  │                                       │
│       ▼                  ▼                                       │
│  XO (CCHD-957)      VCXO (CVHD-950)                              │
│  100 MHz            100 MHz                                      │
│       │                  │                                       │
│       └────────┬─────────┘                                       │
│                │                                                 │
│                ▼                                                 │
│       ┌────────────────┐                                        │
│       │  AD9523-1      │  Clock Synthesizer                     │
│       │  (Low-Jitter)  │                                        │
│       └────────┬───────┘                                        │
│                │                                                 │
│       ┌────────┼────────┬────────────────┬────────            │
│       │        │        │        │        │        │            │
│       ▼        ▼        ▼        ▼        ▼        ▼            │
│   CMOS     LVDS     CMOS     LVDS    LO TX    LO RX            │
│   120MHz   400MHz   100MHz   300MHz   10.5GHz  10.5GHz         │
│   (DAC)    (ADC)    (FPGA)   (MCU)    (TX)     (RX)            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📡 Reference Oscillators

### OCXO (Primary Reference)

| Parameter | Value |
|-----------|-------|
| **Model** | ECOC-2522-10.000-3-F-C |
| **Frequency** | 10 MHz |
| **Stability** | ±0.1 ppm |
| **Phase Noise** | -150 dBc/Hz @ 10kHz offset |
| **Aging** | ±0.5 ppb/day |
| **Operating Temp** | -40°C to +85°C |

### XO (Backup Reference)

| Parameter | Value |
|-----------|-------|
| **Model** | CCHD-957-100 |
| **Frequency** | 100 MHz |
| **Phase Noise** | -140 dBc/Hz @ 10kHz offset |
| **Operating Temp** | -40°C to +85°C |

### VCXO (For PLL)

| Parameter | Value |
|-----------|-------|
| **Model** | CVHD-950-100.000 |
| **Frequency** | 100 MHz |
| **Pull Range** | ±100 ppm |
| **Phase Noise** | -135 dBc/Hz @ 10kHz offset |

---

## ⏱️ Clock Synthesizer (AD9523)

### Specifications

| Parameter | Value |
|-----------|-------|
| **Model** | Analog Devices AD9523-1 |
| **Input** | 10 MHz (OCXO), 100 MHz (XO/VCXO) |
| **Outputs** | 12 LVDS/CMOS outputs |
| **Jitter** | <100 fs RMS |
| **PLL** | Integrated |

### Output Clocks

| Output | Frequency | Type | Destination |
|--------|-----------|------|-------------|
| **OUT0** | 120 MHz | CMOS | DAC (AD9708) |
| **OUT1/2** | 400 MHz | LVDS | ADC (AD9484) |
| **OUT3** | 100 MHz | CMOS | FPGA (system/reference) |
| **OUT4/5** | 300 MHz | LVDS | MCU (STM32F746) |
| **OUT6** | 5 MHz | LVDS | MCU (sync) |
| **OUT7** | 100 MHz | CMOS | LO TX (ADF4382) |
| **OUT8** | 100 MHz | CMOS | LO RX (ADF4382) |

---

## 📡 LO Synthesizers

### TX LO (ADF4382)

| Parameter | Value |
|-----------|-------|
| **Model** | Analog Devices ADF4382 |
| **Frequency** | 10.5 GHz |
| **Phase Noise** | -95 dBc/Hz @ 10kHz offset |
| **Output Power** | +10 dBm |
| **Reference** | 100 MHz from AD9523 |

### RX LO (ADF4382)

| Parameter | Value |
|-----------|-------|
| **Model** | Analog Devices ADF4382 |
| **Frequency** | 10.5 GHz ± IF |
| **Phase Noise** | -95 dBc/Hz @ 10kHz offset |
| **Output Power** | +10 dBm |
| **Reference** | 100 MHz from AD9523 |

---

## 🔗 Clock Distribution

### DAC Clock (120 MHz CMOS)

```
AD9523 (OUT0)
  │
  ▼
DAC (AD9708)
  │
  └── Clock input: 120 MHz CMOS
  └── Jitter requirement: <1 ps RMS
```

### ADC Clock (400 MHz LVDS)

```
AD9523 (OUT1/2)
  │
  ▼
ADC (AD9484)
  │
  └── Clock input: 400 MHz LVDS
  └── Jitter requirement: <200 fs RMS
```

### FPGA Clock (100 MHz CMOS)

```
AD9523 (OUT3)
  │
  ▼
FPGA (XC7A50T)
  │
  └── Clock input: 100 MHz CMOS
  └── Global clock buffer (BUFG)
```

### MCU Clock (300 MHz LVDS + 5 MHz Sync)

```
AD9523 (OUT4/5) ──→ MCU (300 MHz LVDS)
AD9523 (OUT6) ──→ MCU (5 MHz LVDS Sync)
```

---

## 📊 Jitter Budget

| Component | Added Jitter | Cumulative Jitter |
|-----------|--------------|-------------------|
| **OCXO** | — | 100 fs |
| **AD9523** | 80 fs | 128 fs |
| **DAC clock path** | 50 fs | 137 fs |
| **ADC clock path** | 30 fs | 131 fs |
| **LO TX** | 100 fs | 167 fs |
| **LO RX** | 100 fs | 167 fs |

---

## 🔄 Synchronization

### System Synchronization

```
External PPS (GPIO)
  │
  ▼
MCU (STM32F746)
  │
  ├──→ FPGA (sync pulse)
  │
  └──→ AD9523 (sync)
         │
         └──→ All clocks synchronized
```

### Multi-Board Synchronization

| Signal | Purpose |
|--------|---------|
| **10 MHz Ref** | Common reference for all boards |
| **PPS** | Pulse-per-second synchronization |
| **Trigger** | System trigger for coordinated operation |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[RF Chain Documentation]] - LO distribution details
- [[External Interfaces]] - External reference input

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
