# 📡 AERIS-10N Fractal Antenna 32×16

**10.5 GHz Phased Array Radar Antenna** — H-Fractal 32×16 element array with simulation reports.

---

## 🎯 Key Results

| Parameter | Value |
|-----------|-------|
| **Frequency** | 10.5 GHz (λ₀=28.55mm) |
| **S₁₁ @ 10.5 GHz** | −18.3 dB |
| **VSWR** | 1.28 |
| **Input Impedance** | 49.3 + j12.2 Ω |
| **Directivity** | 12.0 dBi (single) / 33.0 dBi (256 array) |
| **Estimated Gain** | 10.4 dBi (η=70%) |
| **Beam Steering** | ±30° (E-plane) |

---

## 📐 Antenna Architecture

### Fractal H-Resonators (Multi-band):
| Level | Frequency | Bar Length |
|-------|-----------|------------|
| **L0** | 10.5 GHz | 9.16 mm (main) |
| **L1** | 21.0 GHz | 4.58 mm |
| **L2** | 42.0 GHz | 2.29 mm |
| **L3** | 84.0 GHz | 1.15 mm |

### 16-Channel Phased Array:
| Parameter | Value |
|-----------|-------|
| **Grid** | 4×4 = 16 H-fractal subarrays |
| **Substrate** | Rogers RO4350B (εr=3.48, h=0.762mm) |
| **Element Spacing** | 18.32 mm (0.64λ) |
| **Board Size** | 90 × 120 mm |
| **Phase Shifters** | 4× ADAR1000 (4 channels each) |
| **Power Divider** | Corporate 1→4 (equal path lengths) |

---

## 📊 Simulation Reports

| Report | Pages | Content |
|--------|-------|---------|
| **Fractal_32x16_SimReport.pdf** | 9 | S₁₁, Smith chart, 2D/3D patterns, beam steering, current distribution, multi-band resonances |
| **Array_256elem_SimReport.pdf** | 10 | 256-element tiled array, 33 dBi directivity, 5.3° HPBW, 6 scan modes |

---

## 📁 Files in This Repository

```
Fractal_32x16/
├── AERIS_10N_Fractal_32x16.kicad_pcb    # Main antenna PCB (KiCad)
├── BACKPLANE_16T_v1.kicad_pcb           # 16-tile backplane controller
├── 32х16.png                            # Antenna geometry
├── split_32х16.png                      # Split view
├── Fractal_32x16_SimReport.pdf          # 9-page simulation report
└── Array_256elem_SimReport.pdf          # 10-page 256-element report
```

---

## 🔧 System Scaling

| Array | Elements | Directivity | Beam Width | Est. Cost |
|-------|----------|-------------|------------|-----------|
| **2×2 (v37)** | 4 | 12.0 dBi | ~50° | ~$100 |
| **4×4** | 16 | 18.6 dBi | ~25° | ~$400 |
| **16×16 (tile)** | 256 | 33.0 dBi | ~5.3° | ~$2,500 |

---

## 💰 Prototype Budget (256 elements)

| Component | Quantity | Cost |
|-----------|----------|------|
| ADAR1000 beamformers | 64× | $1,280 |
| Rogers RO4350B tiles | 16× | $480 |
| Backplane PCB | 1× | $250 |
| Assembly | — | $300 |
| **Total** | — | **~$2,500** |

---

## ⚠️ Important Note

This is a **semi-analytical model** (Lorentzian impedance + array factor), **not full-wave EM** (HFSS/CST). For production validation, VNA measurement or full-wave solver is required. However, the model is adequate for:
- Antenna behavior estimation
- Resonance analysis
- Radiation pattern prediction
- Gain estimation

---

## 🛠️ Tools Used

- **KiCad 9.0** — PCB design
- **Python** — Fractal generation, simulation
- **ADAR1000** — Beamforming IC (Analog Devices)

---

## 📞 Project Info

- **Frequency:** 10.5 GHz
- **Platform:** AERIS-10N Phased Array Radar
- **Status:** Alpha (simulation validated)
- **License:** Open Source

---

## 🔗 Links

- **GitHub:** https://github.com/oi8509701-ui/radar-system
- **Full Project:** https://github.com/NawfalMotii79/PLFM_RADAR

---

*Last updated: 2026-03-31*
