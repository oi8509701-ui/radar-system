# Power Board — PLFM Radar power distribution

This document matches the current **`PowerBoard.kicad_pcb`** layout (**v13**: Kelvin vias and reinforced decoupling). The older README described a different architecture (other ICs, sequencer, current monitoring) and **does not apply** to this board.

## Purpose

Centralized power for radar subsystems: many independent rails, low-noise LDOs for clock/PLL, negative rails from charge pumps, and high-current outputs for the FPGA, RF (ADAR), frequency synthesizer, power amplifier (PA), and auxiliaries (USB bridge, sensors, fans, passthrough feeds).

## Primary artifacts

| File | Description |
|------|-------------|
| `PowerBoard.kicad_pcb` | Current PCB (placement, copper, vias, silkscreen) |
| `PowerBoard_BOM.txt` | Aggregated bill of materials by footprint / value |

**Board size:** 280 × 300 mm.  
**Recommended stackup:** 4 layers — `F.Cu` | `In1.Cu` (GND) | `In2.Cu` (PWR) | `B.Cu` (GND). The file may show a different stack; align stackup with your fab before production.

**Power input (design intent):** **12–17 V DC** bus (`VIN`), plus a separate PA feed (`J_PA_IN` and related routing).

## Active ICs

What is actually on this revision:

| Type | MPN / family | Qty | Role |
|------|----------------|-----|------|
| Buck | **TPS562208DDCT** | 22 | Step-down converters, ~2 A, 4.5–17 V |
| LDO | **ADM7151ACPZ** (series) | 8 | Ultra-low-noise linear regulators |
| LDO | **TPS7A8300RGRR** | 2 | Adjustable low-noise LDO, ~1 A |
| Charge pump | **LM2662MX/NOPB** | 5 | Inverters / negative rails |

**Not used** on this revision (unlike the legacy README): MAX16064, INA219, TPS5430/TPS5420, LT861x, ADM7150 as the sole LDO, dedicated OVP/OCP/UVLO ASIC — add those in schematic or a future spin if required.

## Input stage and protection

The PCB includes (see silk and refdes):

- **SW1** — main power switch  
- **F1** — fuse holder (5 × 20 mm cartridge)  
- **TVS1** — transient suppressor (e.g. SMAJ package)  
- **Q_PROT** — P-channel MOSFET reverse-polarity protection  
- **NTC1** — inrush current limiting NTC  
- **C_BULK1 / C_BULK2** and other **bulk** parts — electrolytics / large capacitance at input and buses  

## Inductors and filtering

- Power inductors **VLP8040T** (2.2 µH / 3.3 µH / 1 µH per converter), including **L22** for a dedicated buck.  
- **L_PA_FILT** — inductor in the LC network at the heavy PA output (1210; value per **Value** on the board).

## Negative rails

Five **LM2662** inverters generate negative supplies (including ADAR/PA-related buses). Extra output filter capacitors were added on charge-pump outputs (v13).

## Additional rails (aligned with Main / Clock / PA)

Net list highlights:

- **+3V3_FT**, **+1V1_FT** — USB bridge (FT601) I/O and core  
- **+3V3_SENSOR** — IMU / GPS / baro / temperature  
- **+5V_FAN** — cooling fans  
- **EN_+3V3_FT**, **EN_+1V1_FT**, **EN_+3V3_SENSOR** — regulator enables  

Passthrough screw terminals **J_MTR** (12 V for actuator/mechanics per system definition) and **J_22V** (high-voltage PA feed, e.g. QPA2962) sit alongside **J_VIN**, **J_PA_IN**, and **X1**.

## Output rail groups (net-name overview)

Below are **net names** in `PowerBoard.kicad_pcb`. Final current capability is not locked without schematic review and DRC; validate against load.

**FPGA / digital:** `+1V0_FPGA`, `+1V8_FPGA`, `+3V3_FPGA`, `+3V3`, intermediate `N$*` at bucks.  
**RF / ADAR:** `+3V3_ADAR_12`, `+3V3_ADAR_34`, `+5V0_ADAR`, `+5V0_PA_1` … `_3`, `+5V5_PA`, negatives `-5V0_ADAR12`, `-5V0_ADAR34`, `-5V5_PA`, etc.  
**Switch / datapath:** `+3V3_SW`, `+3V3_VDD_SW`, `-3V3_SW`, `-3V4`, `+3V4`, `+5V0_0` … `+5V0_5`, `+5V0_LO`, `+3V3_LO_1`, `+3V3_LO_2`.  
**Synth / clocking:** `+1V8_CLOCK`, `+3V3_CLOCK`, `+3V3_XO`, `+3V3_AN`.  
**Other:** `+3V3_ADTR`, `+5V0_ADTR`, `+5V0_4`, plus FT/sensor/fan rails above.

`EN_+…` enable nets go to jumpers/headers and partly to **SV1** / **J_CTRL** (see PCB).

## Connectors, indication, control

- **Screw terminals:** `J_VIN`, `J_PA_IN`, `J_PA_PWR` (4P, heavy PA), `J_MTR`, `J_22V`, duplicate input **X1**  
- **Grouped pin headers:** `J_FPGA`, `J_RF`, `J_CLK`, `J_PA_OUT`, `J_SENSOR`, `J_USB`  
- **J_CTRL** — status/control (including PGOOD and Kelvin sense lines from latest script iterations)  
- **SV1** — 2×10 header for enable / bus distribution  
- **J_EN_DIG**, **J_EN_RF**, **J_EN_PA**, **J_EN_SEN**, **J_EN_USB1**, **J_EN_USB2** — 3-pin jumpers for enable groups  
- **X2–X35** etc. — distributed 2-pin Molex KK-style headers per rail  
- **LED1–LED5** + resistors — status LEDs  
- **TP_*** — test points (voltages, GND)  
- **MH1–MH4** — M3 mounting holes  

Silkscreen includes polarity, current-limit notes, and a pre-route checklist (see PCB).

## Bill of materials

Full aggregated list: **`PowerBoard_BOM.txt`**.

Roughly **~393** placements to procure (**~45** unique part types/sizes), plus separately: M3 hardware, 2.54 mm jumper shunts, test pads, bare PCB, and stencil.

## PCB generation scripts

Automation history in `PowerBoard/`:

- `fix_powerboard.py` — pull components inside board outline after conversion  
- `auto_layout_v8.py` — placement, power zones, edge connectors  
- `add_components_v9.py` … `add_components_v10.py` — input, protection, bulk, grouped headers  
- `add_missing_rails_v11.py` — FT601, sensor, fan rails, passthrough terminals  
- `add_hardening_v12.py` — via stitching, bus capacitors  
- `add_kelvin_v13.py` — Kelvin vias at IC/cap pads, CP filters, silk  

Re-running scripts without idempotence may duplicate geometry; the working source is **`PowerBoard.kicad_pcb`**.

## Important notes

1. **Schematic vs PCB:** The source of truth for nets and values is the current KiCad schematic (if present) plus this PCB; reconcile mismatches manually.  
2. **Routing:** The repo emphasizes placement, pours, and vias; finish traces, clearances, and DRC per your rules and fab.  
3. **Four layers** are strongly recommended for this many DC/DC converters and buses to limit EMI and PDN impedance.

## System cross-reference

Rails are coordinated with **MainBoard**, **FrequencySynthesizerBoard**, and **PowerAmplifierBoard** (see the corresponding `.sch` files in the repository).

## Russian documentation

See **`README.md`** for the Russian version of this document.
