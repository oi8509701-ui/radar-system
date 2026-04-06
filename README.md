X-Band T/R Module (10 GHz) with Fractal Antenna

High-performance single-channel Transmit/Receive (T/R) module for X-band phased array systems (~10–10.5 GHz), featuring integrated beamforming and a compact fractal antenna.
---------------------------------

<img width="342" height="679" alt="TR_Module_10GHz kicad" src="https://github.com/user-attachments/assets/77c6f4d4-0f27-47eb-a78c-3ea46b9e804b" />

---------------------------------
 X-Band T/R Module (10 GHz) with Fractal Antenna

High-performance single-channel Transmit/Receive (T/R) module for X-band phased array systems (~10–10.5 GHz), featuring integrated beamforming and a compact fractal antenna.

⸻
 
 Overview

This project implements a single RF front-end module (tile) designed for scalable phased array systems.

Key features:

	•	X-band operation (~10–10.5 GHz)
	•	Integrated PA + LNA + T/R switch (QPM1002)
	•	Beamforming support (phase + amplitude control)
	•	Compact fractal antenna (14×14 mm)
	•	Designed for array scaling (e.g., 256+ elements)
	•	Optimized for automated routing (Freerouting)

⸻
 
 Architecture

RF IN → Phase Shifter → Attenuator → TXIN → [QPM1002] → ANT → Antenna
                                            ▲
RF OUT ← Phase Shifter ← Attenuator ← RXOUT ┘

QPM1002 Internal Structure:

	•	TX path: PA (~35 dBm pulsed)
	•	RX path: LNA (~2.2 dB NF, ~25 dB gain)
	•	Internal T/R switch
	•	Built-in power detector (VDET)

⸻
 
 Power Architecture

Rail	Voltage	Purpose
TX_VD	+25V	Power Amplifier
RX_VD	+10V	LNA
VDD_LOGIC	+5V	Digital logic
VDD_IO	+3.3V	Control interface
VG	-2.5V	GaN gate bias

Converters:

	•	LM5156 (SEPIC) → 25V
	•	LM5017 → 10V / 5V
	•	Charge pump → -2.5V

⸻

RF Components

Component	Function	Notes

QPM1002	T/R front-end	Core RF IC
TGP2109	Phase shifter (6-bit)	8–12 GHz
PE43705	Attenuator (6-bit)	0.5–12 GHz


⸻

 PCB
 
	•	Substrate: Rogers 4350B
	•	Stackup: 4 layers (RF + GND + PWR + CTRL)
	•	Controlled impedance (50 Ω)
	•	Dense via stitching for RF grounding
	•	Optimized for high-frequency layout

⸻

 Thermal Design

Per module dissipation:

Block	Power
PA	~8 W
DC-DC	~5.5 W
Beamforming	~1.3 W
Other	~1 W

Total: ~16 W per module

For 256 modules:

	•	Total ≈ 4 kW
	•	Requires liquid cooling

⸻
 
 Control Interface
 
	•	SPI (phase + attenuation control)
	•	GPIO (TX/RX switching)
	•	I²C (temperature sensors)

Logic:

	•	SN74HC595 (shift register)
	•	SN74LVTH573 (latch)

⸻
 
 Monitoring
 
	•	4× TMP117 temperature sensors:
	•	RF front-end
	•	Power stage
	•	Beamforming chain
	•	PCB ambient

⸻
 
 Power Sequencing

Power-Up:

	1.	Apply VG (-2.5V)
	2.	Disable TX/RX
	3.	Enable RX_VD (10V)
	4.	Enable TX_VD (25V)
	5.	Enable TX/RX

Power-Down:

	1.	Disable TX/RX
	2.	Disable TX_VD
	3.	Disable RX
