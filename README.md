 ✦ AERIS-10 Fractal Antenna 32x16  Releases v0.1
  -----------------------------------------------------------
  •	Overview
	•	Repository structure
	•	How to open in KiCad
	•	What is simulated vs what is measured
	•	Roadmap
  -------------------------------------------------------------
  Simulation status
  •	single element
	•	4×4 tile
	•	256 array
	•	method used
	•	validated / not validated
  --------------------------------------------------------------
  
<img width="477" height="695" alt="FAR" src="https://github.com/user-attachments/assets/8e632f1f-8ae0-4d82-8858-048c7216fd88" />

--------------------------------------------------------------
# Architecture

## Industry approach

Large phased-array systems are not built as a single PCB.  
Instead, a **tile-based architecture** is used.

Each tile = a 4×4 module (~90×120 mm).  
Tiles are mechanically assembled into a single aperture and synchronized by a central controller.

### Advantages

- Single reusable PCB  
- Fault tolerance (replace one tile instead of the whole array)  
- Lower cost (2-layer PCB possible)  
- Per-tile testing  
- Scalable: 4 → 16 → 64 tiles  

### Conclusion

| Question | Answer |
|--------|------|
| 4×4 (16 channels) feasible? | Yes |
| 256 elements on one PCB? | Possible, but not practical |
| Recommended approach | 16 tiles (4×4 each) |
| Cost (tile-based) | ~$3k–5k (prototype, estimate) |
| Cost (monolithic) | ~$10k–15k |

Tile-based architecture is the practical way to scale phased-array radar systems.
--------------------------------------------------------------

<img width="732" height="422" alt="099" src="https://github.com/user-attachments/assets/6e48a4cf-4d29-4e43-b7c7-5b403c72d409" />

--------------------------------------------------------------

This is an ideal model. In reality, the actual range will be lower due to:

losses
calibration
phase errors
clutter
mechanical factors
But the pure scaling based on the table is exactly as shown above.

---------------------------------------------------------------
  
    10.5 GHz Phased Array Radar Antenna
    Key Results:
     - Frequency: 10.5 GHz
     - S11 @ 10.5 GHz: -18.3 dB
     - VSWR: 1.28
     - Input Impedance: 49.3 + j12.2 Ohm
     - Directivity: 12.0 dBi (single) / 33.0 dBi (256 array)
     - Estimated Gain: 10.4 dBi
     - Beam Steering: +/-30 degrees

    Fractal H-Resonators (Multi-band):
     - L0: 10.5 GHz, 9.16 mm (main)
     - L1: 21.0 GHz, 4.58 mm
     - L2: 42.0 GHz, 2.29 mm
     - L3: 84.0 GHz, 1.15 mm

    16-Channel Phased Array:
     - Grid: 4x4 = 16 H-fractal subarrays
     - Substrate: Rogers RO4350B (er=3.48, h=0.762mm)
     - Element Spacing: 18.32 mm
     - Board Size: 90 x 120 mm
     - Phase Shifters: 4x ADAR1000

    Files:
     - AERIS_10N_Fractal_32x16.kicad_pcb
     - BACKPLANE_16T_v1.kicad_pcb
     - 32x16.png
     - split_32x16.png
     - Fractal_32x16_SimReport.pdf (9 pages)
     - Array_256elem_SimReport.pdf (10 pages)
	 ------------------------------------------------------

<img width="1440" height="900" alt="AERIS_10N_Complete_System" src="https://github.com/user-attachments/assets/41a7a62b-2e04-4728-a696-6d5bd06ef65f" />

	 ------------------------------------------------------
  
    System Scaling: rough estimate / non-retail assumption
     
	 - 2x2: 4 elements, 12.0 dBi, ~$100
     - 4x4: 16 elements, 18.6 dBi, ~$400
     - 16x16: 256 elements, 33.0 dBi, ~$2,500

    Prototype Budget (256 elements): rough estimate / non-retail assumption
     
	 - ADAR1000 beamformers: $1,280
     - Rogers RO4350B tiles: $480
     - Backplane PCB: $250
     - Assembly: $300

    Important Note:
    This is a semi-analytical model, not full-wave EM (HFSS/CST). For production validation, VNA measurement or full-wave solver is required.

    Tools Used:
     - KiCad 9.0
     - Python
     - ADAR1000 (Analog Devices)
	 
	 Full Project: https://github.com/NawfalMotii79/PLFM_RADAR
	 
     - Last updated: 2026-03-31

