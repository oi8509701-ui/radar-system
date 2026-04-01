# Rogers RO4350B Properties

**Substrate Material for AERIS-10N Fractal H-Tree Antenna**

---

## 📊 Material Properties

| Property | Value | Unit |
|----------|-------|------|
| **Dielectric Constant (εr)** | 3.48 ± 0.05 | — |
| **Loss Tangent (tan δ)** | 0.0037 | — |
| **Thickness** | 0.762 | mm (30 mil) |
| **Copper Weight** | 1 oz (35 μm) | — |
| **Surface Roughness** | 0.5-1.0 | μm |
| **Thermal Conductivity** | 0.69 | W/m·K |
| **CTE (X/Y)** | 3 | ppm/°C |
| **CTE (Z)** | 30 | ppm/°C |
| **Moisture Absorption** | 0.06 | % |
| **Tg (Glass Transition)** | >280 | °C |

---

## 📐 Microstrip Line Calculations

### For 10.5 GHz on RO4350B (h=0.762mm)

| Impedance | Width | εeff | λg |
|-----------|-------|------|-----|
| **50 Ω** | 1.63 mm | 2.94 | 16.6 mm |
| **70.7 Ω** | 0.95 mm | 2.72 | 17.3 mm |
| **100 Ω** | 0.55 mm | 2.55 | 17.8 mm |

**Formulas:**
```
εeff = (εr + 1)/2 + (εr - 1)/2 × (1 + 12h/W)^(-0.5)
λg = λ0 / √εeff
```

---

## 🎯 Patch Antenna Design

### For 10.5 GHz Patch Element

| Parameter | Value | Formula |
|-----------|-------|---------|
| **Patch Width (W)** | 9.54 mm | c/(2f) × √(2/(εr+1)) |
| **Patch Length (L)** | 7.35 mm | c/(2f√εeff) - 2ΔL |
| **ΔL (Length Extension)** | 0.342 mm | Hammerstad formula |
| **Inset Depth (for 50Ω)** | 1.64 mm | cos²(πy/2L) = 50/Zedge |

---

## 📊 Temperature Stability

| Temperature | εr Change | Dimensional Change |
|-------------|-----------|-------------------|
| **-40°C** | +0.05% | -0.012% |
| **25°C** | 0% | 0% |
| **+85°C** | -0.15% | +0.018% |

**Temperature Coefficient of εr:** -10 ppm/°C

---

## 🔧 Manufacturing Tolerances

| Parameter | Standard | Tight |
|-----------|----------|-------|
| **Dielectric Constant** | ±0.05 | ±0.02 |
| **Thickness** | ±10% | ±5% |
| **Trace Width** | ±0.05 mm | ±0.025 mm |
| **Registration** | ±0.075 mm | ±0.05 mm |

---

## 📈 RF Performance

### Insertion Loss (Microstrip, 10.5 GHz)

| Length | Loss |
|--------|------|
| **10 mm** | 0.05 dB |
| **50 mm** | 0.25 dB |
| **100 mm** | 0.50 dB |

**Breakdown:**
- Conductor loss: ~60%
- Dielectric loss: ~35%
- Radiation loss: ~5%

---

## 🔗 References

- [Rogers RO4350B Datasheet](https://www.rogerscorp.com/advanced-connectivity-solutions/ro4350b-laminates)
- [RO4350B Properties](https://www.rogerscorp.com/-/media/project/rogerscorp/documents/advanced-connectivity-solutions/english/data-sheets/ro4350b-laminates-data-sheet.pdf)

---

**Last Updated:** 2026-03-31  
**Version:** 1.0
