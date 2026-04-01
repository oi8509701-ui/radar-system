# 🤖 Automated Connector Placement Guide

**Generated:** 2026-03-31  
**Status:** ✅ Automated schematic symbols created  
**Manual Step:** Place footprints in PCB editor

---

## 📍 CONNECTOR PLACEMENTS

### J_PWR_IN (20-pin Power Input)

**Recommended Position:**
- **X:** 50mm from left edge
- **Y:** 10mm from bottom edge
- **Rotation:** 90° (pins facing down for right-angle)

**Footprint:** `Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical`

**Keepout Zone:** 15mm × 25mm

---

### J_TILE_SYNC (50-pin Tile Sync)

**Recommended Position:**
- **X:** 280mm from left edge
- **Y:** 10mm from top edge
- **Rotation:** 270° (pins facing up)

**Footprint:** `Connector_PinHeader_2.54mm:PinHeader_2x25_P2.54mm_Vertical`

**Keepout Zone:** 65mm × 20mm

---

### J_PA_BIAS (20-pin PA Bias)

**Recommended Position:**
- **X:** 280mm from left edge
- **Y:** 50mm from bottom edge
- **Rotation:** 0° (vertical)

**Footprint:** `Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical`

**Keepout Zone:** 25mm × 15mm

---

## 🔧 AUTOMATED PLACEMENT SCRIPT

```bash
# Run in KiCad Python console
import pcbnew
pcb = pcbnew.GetBoard()

# J_PWR_IN
j_pwr_in = pcbnew.FootprintLoad("/path/to/library", "PinHeader_2x10_P2.54mm_Vertical")
j_pwr_in.SetPosition(pcbnew.VECTOR2I(50000000, 10000000))  # 50mm, 10mm
j_pwr_in.SetOrientationDegrees(90)
pcb.Add(j_pwr_in)

# J_TILE_SYNC
j_tile = pcbnew.FootprintLoad("/path/to/library", "PinHeader_2x25_P2.54mm_Vertical")
j_tile.SetPosition(pcbnew.VECTOR2I(280000000, 10000000))  # 280mm, 10mm
j_tile.SetOrientationDegrees(270)
pcb.Add(j_tile)

# J_PA_BIAS
j_pa = pcbnew.FootprintLoad("/path/to/library", "PinHeader_2x10_P2.54mm_Vertical")
j_pa.SetPosition(pcbnew.VECTOR2I(280000000, 50000000))  # 280mm, 50mm
j_pa.SetOrientationDegrees(0)
pcb.Add(j_pa)

# Save
pcb.Save("/path/to/RADAR_Main_Board_auto.kicad_pcb")
```

---

## ✅ VERIFICATION

After placement:

1. **Run DRC:** Tools → Design Rule Check
2. **Check clearances:** All connectors should have 10mm keepout
3. **Verify orientation:** Pins should face board edge
4. **Update schematic:** Tools → Update PCB from Schematic

---

**Next:** Run automated routing script
