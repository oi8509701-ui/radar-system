# Antenna Array

Documentation for the 16-tile phased array antenna system.

---

## 📐 Array Architecture

### Tile Configuration

```
┌─────────────────────────────────────────────────────────────┐
│              16-TILE PHASED ARRAY (4×4 Grid)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Tile 1    Tile 2    Tile 3    Tile 4     ← Row 1        │
│   ┌───┐    ┌───┐    ┌───┐    ┌───                        │
│   │512│    │512│    │512│    │512│                        │
│   │el │    │el │    │el │    │el │                        │
│   └───┘    └───    └───┘    └───┘                        │
│                                                             │
│   Tile 5    Tile 6    Tile 7    Tile 8     ← Row 2        │
│   ┌───┐    ┌───┐    ┌───    ┌───┐                        │
│   │512│    │512│    │512│    │512│                        │
│   │el │    │el │    │el │    │el │                        │
│   └───    └───┘    └───┘    └───┘                        │
│                                                             │
│   Tile 9    Tile 10   Tile 11   Tile 12    ← Row 3        │
│   ┌───    ┌───┐    ┌───┐    ┌───┐                        │
│   │512│    │512│    │512│    │512│                        │
│   │el │    │el │    │el │    │el │                        │
│   └───┘    └───┘    └───┘    └───                        │
│                                                             │
│   Tile 13   Tile 14   Tile 15   Tile 16    ← Row 4        │
│   ┌───┐    ┌───┐    ┌───    ┌───┐                        │
│   │512│    │512│    │512│    │512│                        │
│   │el │    │el │    │el │    │el │                        │
│   └───┘    └───┘    └───┘    └───                        │
│                                                             │
│   Total Elements: 16 × 512 = 8,192                         │
│   Aperture Size: ~2.5m × ~1.3m                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Tile Specifications

### Per-Tile Parameters

| Parameter | Value |
|-----------|-------|
| **Elements per tile** | 512 (32×16) |
| **Tile dimensions** | ~73mm × 73mm |
| **Element spacing** | ~14mm (0.5λ at 10.5 GHz) |
| **Substrate** | Rogers RO4350B |
| **Substrate thickness** | 0.762mm |
| **Dielectric constant** | εr = 3.48 |

### Per-Element Parameters

| Parameter | Value |
|-----------|-------|
| **Element type** | Patch antenna |
| **Operating frequency** | 10.5 GHz |
| **Polarization** | Linear (configurable) |
| **Element gain** | ~5-7 dBi |

---

## 🎯 Beamforming

### Architecture

```
FPGA (Beamforming coefficients)
  │ (SPI control)
  ▼
ADAR1000 (×4)
  │ (16 channels, phase & amplitude control)
  ▼
ADTR1107 (×16)
  │ (Per-element control)
  ▼
Antenna Elements (512 per tile)
```

### Beam Steering

| Parameter | Value |
|-----------|-------|
| **Steering range** | ±45° (theoretical) |
| **Steering resolution** | 5.625° (6-bit phase control) |
| **Amplitude control** | 0 to -31.5 dB (0.5 dB steps) |
| **Phase control** | 0 to 360° (6-bit) |

### Beam Patterns

| Steering Angle | Gain (estimated) | Beamwidth |
|----------------|------------------|-----------|
| **0° (broadside)** | 40-43 dBi | ~3-5° |
| **±30°** | 37-40 dBi | ~4-6° |
| **±45°** | 34-37 dBi | ~5-8° |

---

## 🔧 Calibration

### Calibration Architecture

```
CAL Tone Generator (10.5 GHz)
  │
  ▼
1-to-16 Coupler
  │
  ├─────┬─────┬─────┬─────┐
  ▼     ▼     ▼     ▼     ▼
Tile 1 Tile 2 ... Tile 16
  │     │           │
  └─────┴─────┬─────┘
              ▼
         ADC Measurement
              │
              ▼
         FPGA (Calculate phase/amplitude error)
              │
              ▼
         Correction Table (EEPROM)
              │
              ▼
         Applied to ADAR1000
```

### Calibration Procedure

1. **Startup Calibration**
   - Enable CAL tone generator
   - Measure phase/amplitude for each tile
   - Calculate correction coefficients
   - Store in EEPROM

2. **Periodic Recalibration**
   - Triggered by temperature change (>5°C)
   - Or scheduled interval (e.g., every 10 minutes)

3. **On-Demand Calibration**
   - Manual trigger via host software
   - For diagnostic purposes

### Calibration Parameters

| Parameter | Value |
|-----------|-------|
| **CAL tone frequency** | 10.5 GHz |
| **CAL tone power** | -20 dBm (per tile) |
| **Measurement accuracy** | ±1° phase, ±0.5 dB amplitude |
| **Calibration time** | ~100ms (full array) |

---

## 📊 Performance Metrics

### Array Gain

| Configuration | Gain |
|---------------|------|
| **Single element** | ~5-7 dBi |
| **Single tile (512 elem)** | ~32-34 dBi |
| **Full array (8,192 elem)** | ~40-43 dBi |

### Beamwidth

| Plane | Beamwidth (estimated) |
|-------|----------------------|
| **Azimuth** | ~3-5° |
| **Elevation** | ~5-8° |

### Sidelobe Level

| Condition | Sidelobe Level |
|-----------|----------------|
| **Uniform weighting** | -13 dB |
| **Taylor weighting** | -25 to -30 dB |

---

## 🔗 Related Pages

- [[System Architecture]] - Overall system overview
- [[RF Chain Documentation]] - Signal paths
- [[Hardware Specifications]] - Component details

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
