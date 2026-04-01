# RF Chain Documentation

Detailed documentation of the RF signal paths in the AERIS-10N system.

---

## 📡 TX Signal Path

### Block Diagram

```
FPGA
  │ (I/Q data)
  ▼
DAC (AD9708)
  │ (IF chirp, 125 MSPS)
  ▼
TX LPF (~30 MHz)
  │ (Filtered IF)
  ▼
Mixer TX (LTC5552) ← LO TX (10.5 GHz from ADF4382)
  │ (Upconverted RF)
  ▼
TX BPF (10-11 GHz)
  │ (Filtered RF)
  ▼
RF Switch TX (M3SWA2-34DR+)
  │
  ▼
Combiner (EP4RKU+)
  │ (4-way split)
  ▼
ADAR1000 (×4) ← Phase/Amplitude control
  │ (16 channels)
  ▼
ADTR1107 (×16) ← TX/RX switch
  │ (TX mode)
  ▼
QPA2962 (×16) ← 10W GaN PA
  │ (10W per channel)
  ▼
Circulator (×16)
  │
  ▼
Antenna Array (16 tiles, 8,192 elements)
```

### TX Gain Budget

| Stage | Gain/Loss | Cumulative |
|-------|-----------|------------|
| DAC Output | 0 dBm | 0 dBm |
| TX LPF | -1 dB | -1 dBm |
| Mixer TX (Conversion Loss) | -6 dB | -7 dBm |
| TX BPF | -2 dB | -9 dBm |
| RF Switch | -1 dB | -10 dBm |
| Combiner | -6 dB | -16 dBm |
| ADAR1000 (per channel) | +20 dB | +4 dBm |
| ADTR1107 (TX mode) | -2 dB | +2 dBm |
| QPA2962 | +40 dBm (10W) | +42 dBm |
| Circulator | -0.5 dB | +41.5 dBm |
| **Per element** | | **+41.5 dBm** |
| **Array gain (8,192 elem)** | +39 dB | **+80.5 dBm EIRP** |

---

## 📡 RX Signal Path

### Block Diagram

```
Antenna Array (16 tiles, 8,192 elements)
  │
  ▼
Circulator (×16)
  │
  ▼
ADTR1107 (×16) ← RX mode (LNA)
  │ (16 channels)
  ▼
ADAR1000 (×4) ← Phase/Amplitude control
  │ (Combined to 4 channels)
  ▼
RF Switch RX (M3SWA2-34DR+)
  │
  ▼
RX BPF (10-11 GHz)
  │ (Filtered RF)
  ▼
Mixer RX (LTC5552) ← LO RX (10.5 GHz ± IF from ADF4382)
  │ (Downconverted IF)
  ▼
RX LPF 1 (~50 MHz)
  │ (Filtered IF)
  ▼
Opamp (AD8352) ← Gain block
  │
  ▼
RX LPF 2 (Anti-aliasing)
  │
  ▼
ADC (AD9484, 500 MSPS)
  │ (Digital IF)
  ▼
FPGA ← Digital beamforming, DSP
```

### RX Gain Budget

| Stage | Gain/Loss | Cumulative |
|-------|-----------|------------|
| Antenna (per element) | -20 dBi | -20 dBi |
| Circulator | -0.5 dB | -20.5 dBi |
| ADTR1107 (LNA) | +15 dB | -5.5 dBi |
| ADAR1000 (per channel) | +20 dB | +14.5 dBi |
| RF Switch | -1 dB | +13.5 dBi |
| RX BPF | -2 dB | +11.5 dBi |
| Mixer RX (Conversion Loss) | -6 dB | +5.5 dBi |
| RX LPF 1 | -1 dB | +4.5 dBi |
| Opamp (AD8352) | +20 dB | +24.5 dBi |
| RX LPF 2 | -1 dB | +23.5 dBi |
| ADC Input | | +23.5 dBi |

---

## 📡 LO Distribution

### LO Architecture

```
OCXO (10 MHz)
  │
  ▼
AD9523 (Clock Synthesizer)
  │ (100 MHz reference)
  ├──────────────────────┐
  ▼                      ▼
LO TX (ADF4382)      LO RX (ADF4382)
  10.5 GHz              10.5 GHz ± IF
  │                      │
  ▼                      ▼
Balun (MTX2-143+)    Balun (MTX2-143+)
  │                      │
  ▼                      ▼
Attenuator (-3dB)    Attenuator (-3dB)
  │                      │
  ▼                      ▼
Mixer TX              Mixer RX
```

### LO Specifications

| Parameter | TX LO | RX LO |
|-----------|-------|-------|
| **Frequency** | 10.5 GHz | 10.5 GHz ± IF |
| **Phase Noise** | -95 dBc/Hz @ 10kHz | -95 dBc/Hz @ 10kHz |
| **Output Power** | +10 dBm | +10 dBm |
| **After Attenuator** | +7 dBm | +7 dBm |

---

## 📊 Filter Specifications

### TX LPF (Reconstruction Filter)

| Parameter | Value |
|-----------|-------|
| **Type** | Low-pass |
| **Cutoff** | ~30 MHz |
| **Purpose** | Remove DAC images |

### TX/RX BPF

| Parameter | Value |
|-----------|-------|
| **Type** | Band-pass |
| **Passband** | 10-11 GHz |
| **Insertion Loss** | -2 dB |
| **Purpose** | Select operating frequency |

### RX LPF 1 (IF Filter)

| Parameter | Value |
|-----------|-------|
| **Type** | Low-pass |
| **Cutoff** | ~50 MHz |
| **Purpose** | Select IF frequency |

### RX LPF 2 (Anti-aliasing)

| Parameter | Value |
|-----------|-------|
| **Type** | Low-pass |
| **Cutoff** | ~250 MHz |
| **Purpose** | Prevent aliasing in ADC |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[Clock and Timing]] - LO and clock details
- [[Antenna Array]] - Antenna specifications

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
