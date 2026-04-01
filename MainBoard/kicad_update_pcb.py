
import pcbnew

# Load board
pcb = pcbnew.LoadBoard("/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board.kicad_pcb")

# Add J_PWR_IN
j_pwr = pcbnew.FootprintLoad("/Applications/KiCad/KiCad.app/Contents/Share/kicad/modules/Connector_PinHeader_2.54mm.pretty", "PinHeader_2x10_P2.54mm_Vertical")
if j_pwr:
    j_pwr.SetPosition(pcbnew.VECTOR2I(50000000, 10000000))  # 50mm, 10mm
    j_pwr.SetOrientationDegrees(90)
    j_pwr.SetReference("J_PWR_IN")
    pcb.Add(j_pwr)
    print("✅ Added J_PWR_IN")

# Add J_TILE_SYNC
j_tile = pcbnew.FootprintLoad("/Applications/KiCad/KiCad.app/Contents/Share/kicad/modules/Connector_PinHeader_2.54mm.pretty", "PinHeader_2x25_P2.54mm_Vertical")
if j_tile:
    j_tile.SetPosition(pcbnew.VECTOR2I(280000000, 10000000))  # 280mm, 10mm
    j_tile.SetOrientationDegrees(270)
    j_tile.SetReference("J_TILE_SYNC")
    pcb.Add(j_tile)
    print("✅ Added J_TILE_SYNC")

# Add J_PA_BIAS
j_pa = pcbnew.FootprintLoad("/Applications/KiCad/KiCad.app/Contents/Share/kicad/modules/Connector_PinHeader_2.54mm.pretty", "PinHeader_2x10_P2.54mm_Vertical")
if j_pa:
    j_pa.SetPosition(pcbnew.VECTOR2I(280000000, 50000000))  # 280mm, 50mm
    j_pa.SetOrientationDegrees(0)
    j_pa.SetReference("J_PA_BIAS")
    pcb.Add(j_pa)
    print("✅ Added J_PA_BIAS")

# Save updated PCB
pcb.Save("/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board_auto.kicad_pcb")
print("\n✅ PCB saved")
