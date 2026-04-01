# AERIS-10N 16-Tile Phased Array Radar

**Welcome to the official documentation for the AERIS-10N radar system!**

---

## 📋 Project Overview

The AERIS-10N is a **10.5 GHz phased array radar** system using a tile-based architecture with **16 identical tiles** arranged in a 4×4 grid. Each tile contains **512 antenna elements** (32×16), resulting in a total of **8,192 radiating elements**.

### Key Features

| Feature | Specification |
|---------|---------------|
| **Frequency** | 10.5 GHz (X-Band) |
| **Total Elements** | 8,192 (16 tiles × 512) |
| **Gain** | 40-43 dBi (estimated) |
| **Beam Steering** | ±45° (electronic) |
| **Max Range** | 3-20 km (configuration dependent) |
| **Bandwidth** | 100-500 MHz (configurable) |

---

## 📚 Documentation Index

### Core Documentation

| Page | Description |
|------|-------------|
| [[System Architecture]] | Complete system block diagram and subsystem descriptions |
| [[Hardware Specifications]] | Full BOM, component details, PCB specifications |
| [[RF Chain Documentation]] | TX/RX signal paths, LO distribution, gain budget |
| [[Antenna Array]] | 16-tile architecture, beamforming, calibration |
| [[Power System]] | Power distribution, voltage rails, sequencing |
| [[Clock and Timing]] | Clock tree, frequencies, jitter specifications |
| [[External Interfaces]] | 10G Ethernet, USB 3.0, GPIO, Ext Ref, JTAG |

### Implementation Guides

| Page | Description |
|------|-------------|
| [[Firmware and Software]] | FPGA firmware, MCU firmware, host software |
| [[Assembly Guide]] | Step-by-step assembly instructions |
| [[Testing and Validation]] | Test procedures, required equipment |
| [[FAQ and Troubleshooting]] | Common issues, solutions, known limitations |

---

## 🚀 Quick Start

### For New Users

1. Start with [[System Architecture]] to understand the overall system
2. Read [[Hardware Specifications]] for component details
3. Follow [[Assembly Guide]] for building the system
4. Use [[Testing and Validation]] for verification

### For Developers

1. Review [[Firmware and Software]] for code documentation
2. Check [[External Interfaces]] for communication protocols
3. Reference [[RF Chain Documentation]] for signal processing details

---

## 📊 System Status

| Subsystem | Status | Last Updated |
|-----------|--------|--------------|
| **Architecture** | ✅ Approved | 2026-03-31 |
| **Hardware Design** | ✅ Complete | 2026-03-31 |
| **Firmware** | 🔄 In Development | 2026-03-31 |
| **Software** | 🔄 In Development | 2026-03-31 |
| **Testing** | ⏳ Pending | — |

**Legend:** ✅ Complete | 🔄 In Progress | ⏳ Not Started

---

## 🔗 External Resources

- **GitHub Repository:** https://github.com/oi8509701-ui/radar-system
- **Full Project:** https://github.com/NawfalMotii79/PLFM_RADAR
- **Architecture PDF:** [AERIS_10N_System_Architecture.pdf](https://github.com/oi8509701-ui/radar-system/blob/main/AERIS_10N_System_Architecture.pdf)
- **Complete Schematic:** [AERIS_10N_Complete_System.pdf](https://github.com/oi8509701-ui/radar-system/blob/main/AERIS_10N_Complete_System.pdf)

---

## 📞 Contact & Support

For questions, issues, or contributions:

- **Issues:** Open an issue on GitHub
- **Discussions:** Use GitHub Discussions for general questions
- **Email:** [Contact project maintainers]

---

## 📝 License

This project is open-source. See the main repository for license details.

---

**Last Updated:** 2026-03-31  
**Version:** 2.0
