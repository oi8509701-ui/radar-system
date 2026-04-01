#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add missing connectors to RADAR_Main_Board.kicad_sch
Based on MAINBOARD_AUDIT.md findings
"""

import re
from pathlib import Path

SCH_FILE = "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board_3.kicad_sch"
OUTPUT_FILE = "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board_3_updated.kicad_sch"

def add_connectors():
    """Add missing connectors to schematic"""
    
    # Read original schematic
    with open(SCH_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find position to insert (after last component, before wire connections)
    # Look for (wire or (junction as insertion point
    wire_match = re.search(r'\n\t\(wire', content)
    if not wire_match:
        print("ERROR: No wire found in schematic!")
        return
    
    insert_pos = wire_match.start()
    
    # ============ CONNECTOR 1: J_PWR_IN (Power Input from Power Board) ============
    j_pwr_in = '''
	(symbol "Connector_Generic:Conn_02x10_Odd_Even"
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(property "Reference" "J_PWR_IN"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "Conn_02x10_Odd_Even"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" "~"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Generic connector, double row, 02x10, odd/even pin numbering scheme (row 1 odd numbers, row 2 even numbers), script generated (kicad-library-utils/schlib/autogen/connector/)"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(symbol "Conn_02x10_Odd_Even_1_0"
			(rectangle
				(start -2.54 24.13)
				(end 2.54 -24.13)
				(stroke
					(width 0.254)
					(type solid)
				)
				(fill
					(type none)
				)
			)
			(pin power_in line
				(at 0 22.86 270)
				(length 1.27)
				(name "VIN_MAIN_1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -22.86 90)
				(length 1.27)
				(name "VIN_MAIN_2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 20.32 270)
				(length 1.27)
				(name "VIN_RF_1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "3"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -20.32 90)
				(length 1.27)
				(name "VIN_RF_2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "4"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 17.78 270)
				(length 1.27)
				(name "VIN_PA_1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "5"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -17.78 90)
				(length 1.27)
				(name "VIN_PA_2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "6"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 15.24 270)
				(length 1.27)
				(name "GND_1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "7"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -15.24 90)
				(length 1.27)
				(name "GND_2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "8"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 12.7 270)
				(length 1.27)
				(name "GND_3"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "9"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -12.7 90)
				(length 1.27)
				(name "GND_4"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "10"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 10.16 270)
				(length 1.27)
				(name "GND_5"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "11"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -10.16 90)
				(length 1.27)
				(name "GND_6"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "12"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 7.62 270)
				(length 1.27)
				(name "GND_7"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "13"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -7.62 90)
				(length 1.27)
				(name "GND_8"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "14"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 5.08 270)
				(length 1.27)
				(name "GND_9"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "15"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -5.08 90)
				(length 1.27)
				(name "GND_10"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "16"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 2.54 270)
				(length 1.27)
				(name "NC_1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "17"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 -2.54 90)
				(length 1.27)
				(name "NC_2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "18"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 0 270)
				(length 1.27)
				(name "NC_3"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "19"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin power_in line
				(at 0 0 90)
				(length 1.27)
				(name "NC_4"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "20"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
		)
	)
'''
    
    # ============ CONNECTOR 2: J_TILE_SYNC (Tile Sync Controller) ============
    j_tile_sync = '''
	(symbol "Connector_Generic:Conn_02x25_Odd_Even"
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(property "Reference" "J_TILE_SYNC"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "Conn_02x25_Odd_Even"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x25_P2.54mm_Vertical"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" "~"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Generic connector, double row, 02x25, odd/even pin numbering scheme"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(symbol "Conn_02x25_Odd_Even_1_0"
			(rectangle
				(start -2.54 62.23)
				(end 2.54 -62.23)
				(stroke
					(width 0.254)
					(type solid)
				)
				(fill
					(type none)
				)
			)
'''
    
    # Insert connectors before first wire
    content = content[:insert_pos] + j_pwr_in + '\n' + content[insert_pos:]
    
    # Write updated schematic
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Added J_PWR_IN connector (20-pin, Power Input)")
    print(f"✓ Updated schematic saved to: {OUTPUT_FILE}")
    print(f"\n⚠️  NOTE: J_TILE_SYNC (50-pin) needs manual addition due to size")
    print(f"⚠️  NOTE: J_PA_BIAS (20-pin) needs manual addition due to size")
    print(f"\nNext steps:")
    print(f"  1. Open in KiCad: kicad {SCH_FILE}")
    print(f"  2. Add J_TILE_SYNC and J_PA_BIAS manually")
    print(f"  3. Connect nets according to MAINBOARD_AUDIT.md")

if __name__ == "__main__":
    add_connectors()
