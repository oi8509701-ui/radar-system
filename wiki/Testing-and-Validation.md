# Testing and Validation

Test procedures and validation for the AERIS-10N radar system.

---

## 📋 Required Equipment

| Equipment | Specification | Purpose |
|-----------|---------------|---------|
| **Power Supply** | 0-30V, 0-30A | System power |
| **Multimeter** | 4.5 digit | Voltage/current measurement |
| **Oscilloscope** | 500 MHz, 2+ channels | Signal analysis |
| **Spectrum Analyzer** | 10 Hz - 18 GHz | RF analysis |
| **Signal Generator** | 10 MHz - 6 GHz | LO injection |
| **VNA** | 10 MHz - 18 GHz | S-parameter measurement |
| **Power Meter** | 10 MHz - 18 GHz | RF power measurement |
| **Attenuators** | 10dB, 20dB, 30dB | Signal attenuation |
| **Cables** | SMA, various lengths | Interconnects |

---

## 🔍 Step 1: Visual Inspection

### Checklist

- [ ] All components mounted correctly
- [ ] No solder bridges
- [ ] All connectors secure
- [ ] No damaged components
- [ ] Proper cable routing
- [ ] No loose screws
- [ ] Thermal paste applied (if required)

---

## ⚡ Step 2: Power-On Test

### Procedure

1. **Set current limit**
   - Power supply: 12V, 5A current limit

2. **Apply power**
   - Turn on power supply
   - Measure input current

3. **Check voltage rails**

| Rail | Expected | Tolerance | Measure |
|------|----------|-----------|---------|
| **VIN_MAIN** | 12V | ±5% | ___ V |
| **VIN_RF** | 12V | ±5% | ___ V |
| **1V0_FPGA** | 1.0V | ±3% | ___ V |
| **1V8_AUX** | 1.8V | ±3% | ___ V |
| **2V5_ANA** | 2.5V | ±3% | ___ V |
| **3V3_DIG** | 3.3V | ±3% | ___ V |
| **5V0_IO** | 5V | ±5% | ___ V |

4. **Verify current draw**

| Rail | Expected | Max | Measure |
|------|----------|-----|---------|
| **VIN_MAIN** | 2-3A | 10A | ___ A |
| **VIN_RF** | 1-2A | 5A | ___ A |
| **VIN_PA** | 0A (idle) | 25A | ___ A |

---

## ⏱️ Step 3: Clock Verification

### Equipment

- Oscilloscope (500 MHz)
- Frequency counter (optional)

### Test Points

| Test Point | Signal | Expected | Measure |
|------------|--------|----------|---------|
| **TP_CLK_DAC** | CMOS 120 MHz | 120 MHz | ___ MHz |
| **TP_CLK_ADC** | LVDS 400 MHz | 400 MHz | ___ MHz |
| **TP_CLK_FPGA** | CMOS 100 MHz | 100 MHz | ___ MHz |
| **TP_CLK_MCU** | LVDS 300 MHz | 300 MHz | ___ MHz |
| **TP_LO_TX** | RF 10.5 GHz | 10.5 GHz | ___ GHz |
| **TP_LO_RX** | RF 10.5 GHz ± IF | 10.5 GHz | ___ GHz |

### Procedure

1. **Measure clock frequencies**
   - Connect oscilloscope to each test point
   - Verify frequency

2. **Check clock quality**
   - Measure rise/fall time
   - Check for overshoot/ringing

3. **Verify phase noise** (if equipment available)
   - Measure phase noise at 10kHz offset
   - Expected: <-90 dBc/Hz

---

## 📡 Step 4: RF Chain Test (TX)

### Equipment

- Spectrum Analyzer (18 GHz)
- Power Meter
- Attenuators (30dB)

### Procedure

1. **Test DAC output**
   - Enable chirp generation
   - Measure IF output (~30 MHz)
   - Expected: 0 dBm

2. **Test Mixer TX output**
   - Enable LO TX (10.5 GHz)
   - Measure RF output
   - Expected: -6 dBm (with conversion loss)

3. **Test PA output** (per channel)
   - Enable QPA2962
   - Measure output power
   - Expected: +40 dBm (10W) per channel

4. **Test full array**
   - Enable all 16 channels
   - Measure EIRP
   - Expected: +80 dBm (with array gain)

### Results

| Test Point | Expected | Measure | Pass/Fail |
|------------|----------|---------|-----------|
| **DAC Output** | 0 dBm | ___ dBm | ___ |
| **Mixer TX Output** | -6 dBm | ___ dBm | ___ |
| **PA Output (per ch)** | +40 dBm | ___ dBm | ___ |
| **Array EIRP** | +80 dBm | ___ dBm | ___ |

---

## 📡 Step 5: RF Chain Test (RX)

### Equipment

- Signal Generator (18 GHz)
- Spectrum Analyzer
- Attenuators (30dB)

### Procedure

1. **Inject test signal**
   - Connect signal generator to antenna input
   - Set frequency: 10.5 GHz
   - Set power: -50 dBm

2. **Test LNA output** (per channel)
   - Measure ADTR1107 output
   - Expected: -35 dBm (with +15 dB gain)

3. **Test ADC input**
   - Measure IF signal at ADC input
   - Expected: 0 dBm (with full gain)

4. **Test ADC output**
   - Capture ADC data
   - Verify signal present in FPGA

### Results

| Test Point | Expected | Measure | Pass/Fail |
|------------|----------|---------|-----------|
| **LNA Output (per ch)** | -35 dBm | ___ dBm | ___ |
| **ADC Input** | 0 dBm | ___ dBm | ___ |
| **ADC Output** | Signal present | ___ | ___ |

---

## 🎯 Step 6: Beamforming Test

### Equipment

- Signal Generator
- Spectrum Analyzer
- Rotating mount (optional)

### Procedure

1. **Test phase control**
   - Set ADAR1000 phase to 0°
   - Measure output phase
   - Repeat for 90°, 180°, 270°

2. **Test amplitude control**
   - Set ADAR1000 amplitude to 0 dB
   - Measure output amplitude
   - Repeat for -15 dB, -31.5 dB

3. **Test beam steering**
   - Set beam to 0° (broadside)
   - Measure received power
   - Set beam to ±30°
   - Measure received power
   - Verify power change (expected: ~3 dB)

### Results

| Test | Expected | Measure | Pass/Fail |
|------|----------|---------|-----------|
| **Phase Control (0°)** | 0° | ___° | ___ |
| **Phase Control (90°)** | 90° | ___° | ___ |
| **Phase Control (180°)** | 180° | ___° | ___ |
| **Phase Control (270°)** | 270° | ___° | ___ |
| **Amplitude Control (0 dB)** | 0 dB | ___ dB | ___ |
| **Amplitude Control (-15 dB)** | -15 dB | ___ dB | ___ |
| **Beam Steering (0°)** | Max power | ___ dBm | ___ |
| **Beam Steering (30°)** | -3 dB | ___ dBm | ___ |

---

## 🌡️ Step 7: Thermal Test

### Equipment

- Thermal camera (optional)
- Thermocouples
- Infrared thermometer

### Procedure

1. **Power on system**
   - Run at full power (all channels)
   - Wait 30 minutes

2. **Measure temperatures**

| Component | Max Temp | Measure | Pass/Fail |
|-----------|----------|---------|-----------|
| **FPGA** | 85°C | ___°C | ___ |
| **QPA2962 (per ch)** | 150°C | ___°C | ___ |
| **DC/DC converters** | 125°C | ___°C | ___ |
| **LDOs** | 125°C | ___°C | ___ |

3. **Verify fan operation**
   - Check fan speed vs temperature
   - Verify airflow

---

## 📊 Step 8: System Performance Test

### Equipment

- Target (corner reflector)
- Rotating mount
- Range measurement equipment

### Procedure

1. **Test range measurement**
   - Place target at known distance (e.g., 100m)
   - Run radar
   - Measure detected range
   - Expected: ±1m accuracy

2. **Test Doppler measurement** (if moving target available)
   - Move target at known velocity
   - Measure Doppler shift
   - Expected: ±1 m/s accuracy

3. **Test beam steering**
   - Steer beam to different angles
   - Measure SNR at each angle
   - Verify beam pattern

### Results

| Test | Expected | Measure | Pass/Fail |
|------|----------|---------|-----------|
| **Range (100m)** | 100m ±1m | ___ m | ___ |
| **Doppler (10 m/s)** | 10 m/s ±1 m/s | ___ m/s | ___ |
| **Beam Steering (0°)** | Max SNR | ___ dB | ___ |
| **Beam Steering (30°)** | -3 dB SNR | ___ dB | ___ |

---

## 📋 Final Checklist

- [ ] All power rails within tolerance
- [ ] All clocks present and correct
- [ ] TX chain operational
- [ ] RX chain operational
- [ ] Beamforming functional
- [ ] Thermal performance acceptable
- [ ] System performance meets specifications

---

## 🔗 Related Pages

- [[Assembly Guide]] - Pre-test assembly
- [[Hardware Specifications]] - Component specifications
- [[FAQ and Troubleshooting]] - Common issues

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
