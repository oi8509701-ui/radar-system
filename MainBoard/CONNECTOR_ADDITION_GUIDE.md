# 🔧 MainBoard Connector Addition Guide

**Manual additions required for complete system integration**

---

## ✅ AUTOMATED (Done by Script):

### **J_PWR_IN (Power Input Connector)**

**Added:** `RADAR_Main_Board_3_updated.kicad_sch`

**Connector:** 2×10 pin header (2.54mm pitch)

**Pinout:**
| Pin | Net | Purpose |
|-----|-----|---------|
| 1, 2 | VIN_MAIN_1, VIN_MAIN_2 | Main power (12-24V, 10A) |
| 3, 4 | VIN_RF_1, VIN_RF_2 | RF power (12-24V, 5A) |
| 5, 6 | VIN_PA_1, VIN_PA_2 | PA power (12-28V, 25A) |
| 7-20 | GND_1 - GND_10 | Ground (×14 pins) |

**Footprint:** `Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical`

**Location:** Place near power input edge of PCB

---

## ⚠️ MANUAL ADDITIONS REQUIRED:

### **1. J_TILE_SYNC (Tile Sync Controller Connector)**

**Connector:** 2×25 pin header (2.54mm pitch, high-density)

**Footprint:** `Connector_PinHeader_2.54mm:PinHeader_2x25_P2.54mm_Vertical`

**Pinout:**
```
Row 1 (Odd pins):
├── 1:   CLK_P (100 MHz LVDS+)
├── 3:   CLK_N (100 MHz LVDS-)
├── 5:   SYNC (hardware sync)
├── 7:   SPI_MOSI
├── 9:   SPI_MISO
├── 11:  SPI_SCLK
├── 13:  CS_1 (Tile 1-4)
├── 15:  CS_2 (Tile 5-8)
├── 17:  CS_3 (Tile 9-12)
├── 19:  CS_4 (Tile 13-16)
├── 21:  3.3V
├── 23:  3.3V
├── 25:  GND
├── 27:  GND
├── 29:  RF_TX_OUT (to Tile 1)
├── 31:  RF_TX_OUT (to Tile 2)
├── 33:  RF_TX_OUT (to Tile 3)
├── 35:  RF_TX_OUT (to Tile 4)
├── 37:  RF_RX_IN (from Tile 1)
├── 39:  RF_RX_IN (from Tile 2)
├── 41:  RF_RX_IN (from Tile 3)
├── 43:  RF_RX_IN (from Tile 4)
├── 45:  NC
├── 47:  NC
├── 49:  NC

Row 2 (Even pins):
├── 2:   GND
├── 4:   GND
├── 6:   GND
├── 8:   GND
├── 10:  GND
├── 12:  GND
├── 14:  GND
├── 16:  GND
├── 18:  GND
├── 20:  GND
├── 22:  GND
├── 24:  GND
├── 26:  GND
├── 28:  GND
├── 30:  GND
├── 32:  GND
├── 34:  GND
├── 36:  GND
├── 38:  GND
├── 40:  GND
├── 42:  GND
├── 44:  GND
├── 46:  GND
├── 48:  GND
├── 50:  GND
```

**Connection:** Connects to Tile Sync Controller motherboard

---

### **2. J_PA_BIAS (PA Board Connector)**

**Connector:** 2×10 pin header (2.54mm pitch)

**Footprint:** `Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical`

**Pinout:**
| Pin | Net | Purpose |
|-----|-----|---------|
| 1 | VG_1 | PA Gate Voltage (Tile 1) |
| 2 | VG_2 | PA Gate Voltage (Tile 2) |
| 3 | VG_3 | PA Gate Voltage (Tile 3) |
| 4 | VG_4 | PA Gate Voltage (Tile 4) |
| 5 | VG_5 | PA Gate Voltage (Tile 5) |
| 6 | VG_6 | PA Gate Voltage (Tile 6) |
| 7 | VG_7 | PA Gate Voltage (Tile 7) |
| 8 | VG_8 | PA Gate Voltage (Tile 8) |
| 9 | VG_9 | PA Gate Voltage (Tile 9) |
| 10 | VG_10 | PA Gate Voltage (Tile 10) |
| 11 | VG_11 | PA Gate Voltage (Tile 11) |
| 12 | VG_12 | PA Gate Voltage (Tile 12) |
| 13 | VG_13 | PA Gate Voltage (Tile 13) |
| 14 | VG_14 | PA Gate Voltage (Tile 14) |
| 15 | VG_15 | PA Gate Voltage (Tile 15) |
| 16 | VG_16 | PA Gate Voltage (Tile 16) |
| 17 | DAC_VG_CLR | DAC Clear |
| 18 | DAC_VG_LDAC | DAC Load DAC |
| 19 | +5V | DAC Power |
| 20 | GND | Ground |

**Connection:** Connects to Power Amplifier Board for PA bias control

---

## 📐 PLACEMENT GUIDELINES:

### **J_PWR_IN:**
- **Location:** Bottom edge of PCB (near power input)
- **Orientation:** Pins facing down for right-angle connector
- **Keepout:** 10mm clearance for connector housing

### **J_TILE_SYNC:**
- **Location:** Top edge of PCB (facing Tile Sync Controller)
- **Orientation:** Vertical or right-angle depending on stackup
- **Keepout:** 15mm clearance for cable routing

### **J_PA_BIAS:**
- **Location:** Right edge of PCB (near PA section)
- **Orientation:** Vertical for direct connection
- **Keepout:** 10mm clearance

---

## 🔌 CONNECTION DIAGRAM:

```
┌─────────────────────────────────────────────────────────────┐
│                    MainBoard                                │
│                                                             │
│  ┌──────────┐                                              │
│  │ J_PWR_IN │◄─── Power Board (VIN_MAIN, VIN_RF, VIN_PA)  │
│  └──────────┘                                              │
│                                                             │
│  ┌────────────┐                                            │
│  │ J_TILE_SYNC│◄─── Tile Sync Controller                   │
│  │            │     (CLK, SYNC, CS, SPI, RF)               │
│  └────────────┘                                            │
│                                                             │
│  ┌───────────┐                                             │
│  │ J_PA_BIAS │◄─── PA Board (VG_1-16, DAC control)         │
│  └───────────┘                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ VERIFICATION CHECKLIST:

After adding connectors in KiCad:

- [ ] J_PWR_IN footprint matches Power Board connector
- [ ] J_TILE_SYNC has 50 pins (2×25)
- [ ] J_PA_BIAS has 20 pins (2×10)
- [ ] All nets connected correctly
- [ ] No DRC errors
- [ ] Silkscreen labels added
- [ ] 3D models assigned
- [ ] Board outline updated for connector keepouts

---

## 📝 STEPS IN KICAD:

1. **Open Schematic:**
   ```
   kicad RADAR_Main_Board.kicad_sch
   ```

2. **Add J_TILE_SYNC:**
   - Place symbol: `Connector_Generic:Conn_02x25_Odd_Even`
   - Assign footprint: `PinHeader_2x25_P2.54mm_Vertical`
   - Connect nets according to pinout above

3. **Add J_PA_BIAS:**
   - Place symbol: `Connector_Generic:Conn_02x10_Odd_Even`
   - Assign footprint: `PinHeader_2x10_P2.54mm_Vertical`
   - Connect VG_1-16 nets from DAC

4. **Update PCB:**
   - Open PCB: `kicad RADAR_Main_Board.kicad_pcb`
   - Update from schematic (Tools → Update PCB from Schematic)
   - Place connectors at edge of board
   - Route connections

5. **Run DRC:**
   - Tools → Design Rule Check
   - Fix any errors

6. **Save and Export:**
   - Save schematic and PCB
   - Export Gerbers for production

---

**Last Updated:** 2026-03-31  
**Status:** ⚠️ MANUAL WORK REQUIRED
