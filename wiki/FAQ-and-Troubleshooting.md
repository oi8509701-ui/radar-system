# FAQ and Troubleshooting

Frequently asked questions and troubleshooting guide for the AERIS-10N radar system.

---

## ❓ FAQ

### General Questions

**Q: What is the maximum range of AERIS-10N?**

A: The maximum range depends on configuration:
- **AERIS-10N (Nexus)**: 3 km (8×16 patch array)
- **AERIS-10E/X (Extended)**: 20 km (32×16 waveguide array with QPA2962 PA)

---

**Q: What is the operating frequency?**

A: 10.5 GHz (X-Band), configurable ±500 MHz.

---

**Q: How many antenna elements are there?**

A: 8,192 elements total (16 tiles × 512 elements per tile).

---

**Q: What is the beam steering range?**

A: ±45° theoretical, ±30° practical (with acceptable gain).

---

**Q: What is the power consumption?**

A: 
- **AERIS-10N (Nexus)**: ~500W
- **AERIS-10E/X (Extended)**: ~940W (with QPA2962 PA)

---

**Q: What interfaces are available?**

A:
- **10G Ethernet** (PRIMARY, XAUI SFP+)
- **USB 3.0** (BACKUP, FT601)
- **GPIO** (SMA, PPS/Trigger)
- **Ext Ref** (10 MHz SMA)
- **JTAG** (FPGA debug)

---

**Q: Is this project open-source?**

A: Yes, this is an open-source project. See the main repository for license details.

---

### Hardware Questions

**Q: Can I use FR-4 instead of Rogers RO4350B?**

A: For RF sections, **no**. Rogers RO4350B is required for consistent dielectric properties at 10.5 GHz. For digital sections, FR-4 is acceptable.

---

**Q: What is the substrate thickness?**

A: 
- **Tile boards**: 0.762mm (30 mil)
- **Main board**: 1.6mm

---

**Q: Can I omit the QPA2962 power amplifiers?**

A: Yes, for short-range operation (AERIS-10N configuration). The ADTR1107 internal PA (~1W) is sufficient for 3 km range.

---

**Q: What is the ADC sampling rate?**

A: 500 MSPS (AD9484).

---

**Q: What is the DAC sampling rate?**

A: 125 MSPS (AD9708).

---

### Firmware/Software Questions

**Q: What FPGA is used?**

A: Xilinx Artix-7 XC7A50T-2FTG256 (upgradeable to XC7A100T).

---

**Q: What MCU is used?**

A: STMicroelectronics STM32F746ZGT7 (ARM Cortex-M7 @ 216 MHz).

---

**Q: Is there host PC software?**

A: Yes, Python-based GUI with data display and control panel.

---

**Q: What protocol is used for data transfer?**

A: UDP streaming over 10G Ethernet (primary), USB 3.0 bulk transfer (backup).

---

## 🔧 Troubleshooting

### Power Issues

**Problem: No power on any rail**

| Possible Cause | Solution |
|----------------|----------|
| Power supply off | Turn on power supply |
| XT30 connector loose | Reconnect XT30 |
| Fuse blown | Replace fuse |
| Power switch off | Turn on power switch |

---

**Problem: 1V0_FPGA rail missing**

| Possible Cause | Solution |
|----------------|----------|
| DC/DC converter fault | Check TPS5430 output |
| Enable pin not asserted | Check MCU GPIO |
| Short circuit | Check for shorts on 1V0 net |
| DC/DC current limit | Reduce load, check current |

---

**Problem: Over-current shutdown**

| Possible Cause | Solution |
|----------------|----------|
| Short circuit | Check for shorts |
| Component failure | Replace faulty component |
| Current limit too low | Adjust current limit |
| Inrush current | Soft-start circuit |

---

### Clock Issues

**Problem: No clock on ADC clock input**

| Possible Cause | Solution |
|----------------|----------|
| AD9523 not configured | Check SPI configuration |
| OCXO not oscillating | Check OCXO power |
| Clock output disabled | Check AD9523 register settings |
| Broken trace | Check continuity |

---

**Problem: High phase noise on LO**

| Possible Cause | Solution |
|----------------|----------|
| Reference clock noise | Check OCXO phase noise |
| AD9523 jitter | Check AD9523 configuration |
| ADF4382 PLL unlock | Check PLL lock detect |
| Power supply noise | Check LDO output noise |

---

### RF Issues

**Problem: No TX output**

| Possible Cause | Solution |
|----------------|----------|
| DAC not generating waveform | Check FPGA configuration |
| LO TX not present | Check ADF4382 output |
| Mixer fault | Check LTC5552 bias |
| PA disabled | Check QPA2962 enable |
| RF switch in RX mode | Check switch control |

---

**Problem: No RX signal**

| Possible Cause | Solution |
|----------------|----------|
| Antenna disconnected | Check antenna connection |
| LNA disabled | Check ADTR1107 bias |
| LO RX not present | Check ADF4382 output |
| Mixer fault | Check LTC5552 bias |
| ADC not capturing | Check FPGA configuration |

---

**Problem: Low TX power**

| Possible Cause | Solution |
|----------------|----------|
| PA bias incorrect | Check QPA2962 gate voltage |
| PA supply voltage low | Check VIN_PA voltage |
| Mismatched load | Check antenna VSWR |
| PA overheating | Check thermal management |

---

### Beamforming Issues

**Problem: Beam steering not working**

| Possible Cause | Solution |
|----------------|----------|
| ADAR1000 not configured | Check SPI configuration |
| Phase/amplitude tables wrong | Check FPGA beamforming coefficients |
| MCU communication fault | Check SPI bus |
| Tile sync not present | Check SYNC signal |

---

**Problem: Asymmetric beam pattern**

| Possible Cause | Solution |
|----------------|----------|
| Phase calibration required | Run calibration procedure |
| Amplitude imbalance | Check ADAR1000 amplitude settings |
| Element failure | Check individual tile operation |
| Mutual coupling | Update beamforming coefficients |

---

### Thermal Issues

**Problem: Over-temperature shutdown**

| Possible Cause | Solution |
|----------------|----------|
| Fans not running | Check fan power and control |
| Heatsink not mounted | Check heatsink mounting |
| Thermal paste missing | Apply thermal paste |
| Airflow blocked | Clear airflow path |
| Ambient temperature too high | Improve cooling |

---

**Problem: High PA temperature**

| Possible Cause | Solution |
|----------------|----------|
| Duty cycle too high | Reduce duty cycle |
| PA bias incorrect | Check QPA2962 gate voltage |
| Thermal resistance too high | Improve thermal path |
| Airflow insufficient | Increase fan speed |

---

### Communication Issues

**Problem: No Ethernet connection**

| Possible Cause | Solution |
|----------------|----------|
| SFP+ module not detected | Check SFP+ module |
| FPGA Ethernet core not running | Check FPGA configuration |
| Cable fault | Replace Ethernet cable |
| IP address conflict | Check IP configuration |

---

**Problem: No USB connection**

| Possible Cause | Solution |
|----------------|----------|
| FT601 not configured | Check FPGA configuration |
| USB driver not installed | Install FTDI drivers |
| Cable fault | Replace USB cable |
| Power insufficient | Check USB power |

---

## 📞 Getting Help

### Before Asking for Help

1. **Check this FAQ** - Your question may already be answered
2. **Check existing issues** - Someone may have had the same problem
3. **Gather information**:
   - System configuration
   - Error messages
   - Test results
   - Photos (if relevant)

### How to Ask for Help

1. **Open an issue on GitHub**
2. **Provide detailed description**:
   - What you're trying to do
   - What you expected
   - What actually happened
3. **Include relevant information**:
   - Hardware revision
   - Firmware version
   - Test results
   - Logs (if available)

---

## 🔗 Related Pages

- [[Testing and Validation]] - Test procedures
- [[Assembly Guide]] - Assembly instructions
- [[System Architecture]] - System overview

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
