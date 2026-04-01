# Assembly Guide

Step-by-step assembly instructions for the AERIS-10N radar system.

---

## 📋 Required Tools

| Tool | Specification | Purpose |
|------|---------------|---------|
| **Hex Driver Set** | 1.5mm, 2.0mm, 2.5mm | M3 standoffs |
| **Screwdriver Set** | Phillips #0, #1 | General assembly |
| **Torque Wrench** | 0.1-0.5 N·m | Precise torque |
| **ESD Mat** | Conductive | ESD protection |
| **ESD Wrist Strap** | Adjustable | ESD protection |
| **Tweezers** | Anti-static | Small component handling |
| **Cable Ties** | Various sizes | Cable management |
| **Thermal Paste** | High conductivity | Heat sink mounting |

---

## 🔧 Step 1: Prepare Work Area

### ESD Safety

1. Place ESD mat on work surface
2. Connect ESD mat to ground
3. Wear ESD wrist strap
4. Verify continuity (resistance < 1MΩ)

### Component Layout

```
┌──────────────────────────────────────────────────────────────────┐
│                      WORK AREA LAYOUT                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Tiles     │  │   Main      │  │   Power     │             │
│  │   (1-16)    │  │   Board     │  │   Board     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Hardware   │  │   Tools     │  │  Cables     │             │
│  │  (screws)   │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Step 2: Mount Tiles to Frame

### Tile Placement

```
┌──────────────────────────────────────────────────────────────────┐
│                    TILE MOUNTING (4×4 GRID)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   Tile 1    Tile 2    Tile 3    Tile 4                           │
│   ┌───┐    ┌───┐    ┌───    ┌───┐                             │
│   │   │    │   │    │   │    │   │  ← M3 standoffs (4 per tile)│
│   └───    └───┘    └───┘    └───┘                             │
│                                                                   │
│   Tile 5    Tile 6    Tile 7    Tile 8                           │
│   ┌───┐    ┌───    ┌───┐    ┌───┐                             │
│   │   │    │   │    │   │    │   │  ← 5mm gap between tiles    │
│   └───┘    └───┘    └───    └───┘                             │
│                                                                   │
│   Tile 9    Tile 10   Tile 11   Tile 12                          │
│   ┌───┐    ┌───    ┌───┐    ┌───┐                             │
│   │   │    │   │    │   │    │   │  ← Torque: 0.3 N·m          │
│   └───┘    └───┘    └───    └───┘                             │
│                                                                   │
│   Tile 13   Tile 14   Tile 15   Tile 16                          │
│   ┌───┐    ┌───┐    ┌───    ┌───┐                             │
│   │   │    │   │    │   │    │   │                             │
│   └───┘    └───┘    └───    └───┘                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Procedure

1. **Prepare frame**
   - Verify frame is level
   - Clean mounting surfaces

2. **Install standoffs**
   - Insert M3 standoffs at tile mounting points
   - Torque to 0.2 N·m

3. **Mount Tile 1**
   - Align Tile 1 with standoffs
   - Secure with M3 screws
   - Torque to 0.3 N·m (cross pattern)

4. **Repeat for Tiles 2-16**
   - Maintain 5mm gap between tiles
   - Verify alignment

---

## 🔧 Step 3: Connect RF Cables

### Cable Routing

```
┌──────────────────────────────────────────────────────────────────┐
│                      RF CABLE ROUTING                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────┐  ┌─────┐  ┌─────  ┌─────┐                          │
│   │ T1  │──│ T2  │──│ T3  │──│ T4  │                          │
│   └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘                          │
│      │        │        │        │                               │
│      │   ┌────┴────────┴────┐  │                               │
│      │   │   Combiner       │  │                               │
│      │   │   (EP4RKU+)      │  │                               │
│      │   └────────┬─────────  │                               │
│      │            │            │                               │
│      └────────────┴────────────┘                               │
│                   │                                             │
│                   ▼                                             │
│            To Main Board                                        │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Procedure

1. **Route cables from tiles to combiner**
   - Use semi-rigid cables
   - Minimum bend radius: 10mm

2. **Connect to combiner**
   - Torque SMA connectors: 0.5 N·m
   - Verify tight connection

3. **Route combiner output to main board**
   - Secure cable with cable ties
   - Avoid sharp bends

---

## 🔧 Step 4: Connect Power Cables

### Power Distribution

```
┌──────────────────────────────────────────────────────────────────┐
│                     POWER CABLE ROUTING                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   Power Input (XT30)                                             │
│         │                                                        │
│         ▼                                                        │
│   ┌─────────────┐                                               │
│   │ Power Board │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│     ┌────┴────┬────────────┬────────────┐                       │
│     │         │            │            │                       │
│     ▼         ▼            ▼            ▼                       │
│  VIN_MAIN  VIN_RF       VIN_PA       Other                      │
│     │         │            │                                    │
│     ▼         ▼            ▼                                    │
│  FPGA,    Clock,       QPA2962                                  │
│  MCU      LO, ADAR                                              │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Procedure

1. **Connect power input**
   - Connect XT30 connector to power board
   - Verify polarity

2. **Connect VIN_MAIN**
   - Route to main board
   - Connect to FPGA, MCU

3. **Connect VIN_RF**
   - Route to clock/LO boards
   - Connect to AD9523, ADF4382

4. **Connect VIN_PA**
   - Route to tile frame
   - Connect to QPA2962 (×16)

---

## 🔧 Step 5: Connect Signal Cables

### Signal Routing

```
┌──────────────────────────────────────────────────────────────────┐
│                    SIGNAL CABLE ROUTING                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   Main Board ──→ Tile Sync Controller ──→ 16 Tiles              │
│       │                                       │                  │
│       │                                       │                  │
│       ├──→ Clock Synth ──→ LO TX/RX          │                  │
│       │                                       │                  │
│       ├──→ Sensors (IMU, GPS, BMP)           │                  │
│       │                                       │                  │
│       └──→ External Interfaces                │                  │
│           (ETH, USB, GPIO, Ext Ref)          │                  │
│                                               │                  │
└──────────────────────────────────────────────────────────────────┘
```

### Procedure

1. **Connect tile sync cables**
   - Connect CLK, SYNC, CS to each tile
   - Verify pinout

2. **Connect clock cables**
   - Connect AD9523 outputs to LO boards
   - Verify 100 MHz reference

3. **Connect sensor cables**
   - Connect I2C/SPI to sensors
   - Verify pull-up resistors

4. **Connect external interface cables**
   - Connect Ethernet SFP+
   - Connect USB 3.0
   - Connect GPIO (SMA)
   - Connect Ext Ref (SMA)

---

## 🔧 Step 6: Final Inspection

### Visual Inspection Checklist

- [ ] All tiles mounted securely
- [ ] All cables routed properly
- [ ] No cable sharp bends
- [ ] All connectors tight
- [ ] No loose screws
- [ ] ESD straps removed
- [ ] Work area clean

### Electrical Inspection Checklist

- [ ] Power input polarity correct
- [ ] No short circuits (multimeter check)
- [ ] All grounds connected
- [ ] Signal continuity verified

---

## 🔧 Step 7: Power-On Test

### Initial Power-On

1. **Connect power supply**
   - Set to 12V, 5A current limit
   - Connect to XT30

2. **Apply power**
   - Turn on power supply
   - Verify VIN_MAIN voltage (12V)

3. **Check voltage rails**
   - Measure 1V0_FPGA
   - Measure 1V8_AUX
   - Measure 3V3_DIG
   - Measure 5V0_IO

4. **Verify no over-current**
   - Check current draw (<5A expected)
   - If >5A, power off immediately

---

## 🔗 Related Pages

- [[Hardware Specifications]] - Component details
- [[Power System]] - Power distribution details
- [[Testing and Validation]] - Post-assembly testing

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
