# 🎯 AERIS-10N 16-Tile Phased Array Radar
## Target Architecture (Полная Целевая Архитектура)

**Версия:** 2.0  
**Дата:** 2026-03-31  
**Статус:** ✅ Утверждена (обновлена по сравнению с RADAR_V6_V2.png)

---

## 📐 АРХИТЕКТУРА СИСТЕМЫ (ОБНОВЛЕННАЯ)

```
                              ┌─────────────────────────────┐
                              │          HOST PC            │
                              │ Beam steering / UI / logs   │
                              └──────────────┬──────────────┘
                                             │ Ethernet / USB
                                             ▼
                              ┌─────────────────────────────┐
                              │         MAIN FPGA           │
                              │ XC7A50T-2FTG256             │
                              │ Waveform / control / DSP    │
                              └───────┬─────────┬───────────┘
                                      │         │
                             SPI cfg  │         │ IF / ADC data
                                      ▼         ▼
                         ┌─────────────────┐   ┌─────────────────┐
                         │ Tile Sync Ctrl  │   │   RX/DSP path   │
                         │ CLK / SYNC / CS │   │ ADC / FPGA merge │
                         └──────┬──────────┘   └─────────────────┘
                                │
                    100 MHz ref │ SYNC / TRX / CS
                                ▼
          ┌──────────────────────────────────────────────────────────────┐
          │                        16 TILES                              │
          │                                                              │
          │  Tile 1    Tile 2    Tile 3   ...                Tile 16    │
          │ ┌───────┐ ┌───────┐ ┌───────┐                    ┌───────┐   │
          │ │Ref in │ │Ref in │ │Ref in │                    │Ref in │   │
          │ │PLL/LO │ │PLL/LO │ │PLL/LO │                    │PLL/LO │   │
          │ │ADAR   │ │ADAR   │ │ADAR   │                    │ADAR   │   │
          │ │TX/RX  │ │TX/RX  │ │TX/RX  │                    │TX/RX  │   │
          │ │4×4 AF │ │4×4 AF │ │4×4 AF │                    │4×4 AF │   │
          │ └──┬────┘ └──┬────┘ └──┬────┘                    └──┬────┘   │
          └────┼──────────────────┼─────────────────────────────┼────────┘
               │         │         │                             │
               └─────────┴─────────┴───── RX IF / subarray ─────┘
                                       │
                                       ▼
                           ┌──────────────────────────┐
                           │ Hybrid RX Combining      │
                           │ per tile / per subarray  │
                           └────────────┬─────────────┘
                                        ▼
                                  ADC / FPGA DSP
```

---

## 🔑 4 КРИТИЧЕСКИХ РЕШЕНИЯ (ОБНОВЛЕНО)

### 1️⃣ LO Topology (Распределение Гетеродина)

```
✅ РЕАЛИЗОВАНО:
   Master reference (100 MHz) → Local PLL/LO на каждом тайле → Калибровка

   OCXO (ECOC-2522-10.000-3-F-C) → 10 MHz
   XO (CCHD-957-100) → 100 MHz
   VCXO (CVHD-950-100.000) → 100 MHz
   ↓
   AD9523 (Clock Synthesizer)
   ↓
   2× ADF4382 (LO TX 10.5 GHz / LO RX 10.5 GHz ± IF)
   ↓
   Balun (MTX2-143+) → Attenuator PAD (ATS1005-3DB-FD-T05) → Mixer (LTC5552)
```

**Почему:**
- Не таскать 10.5 GHz LO на 16 блоков
- Меньше потерь в кабелях/делителях
- Проще масштабировать
- Легче калибровать

---

### 2️⃣ TX/RX Sync (Переключение Приём/Передача)

```
✅ РЕАЛИЗОВАНО:
   SPI загружает регистры → SYNC/TRX линия переключает все тайлы ОДНОВРЕМЕННО

   MCU (STM32F746ZGT7)
   ↓ GPIO
   2× RF Switch (M3SWA2-34DR+) — TX и RX пути
   ↓
   Все 16 тайлов переключаются одновременно
```

**Почему:**
- Аппаратный строб (hardware strobe)
- Все 16 тайлов переключаются одновременно
- Нет рассинхронизации

---

### 3️⃣ RX Combining (Объединение RX Сигналов)

```
✅ РЕАЛИЗОВАНО:
   Hybrid combining:
   • Внутри тайла/подмассива — частичное объединение
   • Наружу выходит меньше каналов
   • FPGA/ADC обрабатывает уже сокращённый набор

   16 Tiles → 16× ADTR1107 → 4× ADAR1000 → Combiner (EP4RKU+)
   → RF Switch → BPF → Mixer → LPF → Opamp (AD8352)
   → ADC (AD9484, 500 MSPS) → FPGA
```

**Почему:**
- Компромисс между analog и digital
- Меньше ADC каналов
- Сохраняется гибкость beamforming

---

### 4️⃣ Calibration (Калибровка)

```
✅ РЕАЛИЗОВАНО:
   Calibration loop:
   • CAL Tone Generator (Separate RF Source, 10.5 GHz)
   • CAL DAC (AD9708) → OPA (OPA4703NA/250) → QPA2962 Gate
   • Phase calibration
   • Amplitude calibration
   • Temperature drift compensation
   • Correction table в EEPROM

   Monitoring:
   • Current Sensor (INA241A3 ×16, per-tile)
   • Monitoring ADC (ADS7830 ×3, 8-bit I2C)
   • QPA2962 VD RELAY (Drain Voltage Switch)
```

**Почему:**
- Без калибровки луч "кривой"
- Температурный дрейф фазы
- Разброс компонентов

---

## 📦 КОМПОНЕНТЫ ПО УРОВНЯМ (ОБНОВЛЕНО)

### Master Level

| Компонент | Модель | Функция |
|-----------|--------|---------|
| **FPGA** | Xilinx Artix-7 XC7A50T-2FTG256 | Waveform Generation, Digital Beamforming, DSP |
| **MCU** | STMicroelectronics STM32F746ZGT7 | System Control, Configuration, Sensor Monitoring |
| **USB 3 PHY** | FTDI FT601Q | USB 3.0 to FPGA (5 Gbps) |
| **OCXO** | ECOC-2522-10.000-3-F-C | 10 MHz Oven-Controlled Ultra-Stable Reference |
| **XO** | CCHD-957-100 | 100 MHz Crystal Oscillator, Low Phase Noise |
| **VCXO** | CVHD-950-100.000 | 100 MHz Voltage-Controlled For PLL |
| **Clock Synth** | Analog Devices AD9523 | Low-Jitter Clock Distribution |

---

### LO System

| Компонент | Модель | Функция |
|-----------|--------|---------|
| **LO TX** | Analog Devices ADF4382 | 10.5 GHz Synthesized LO, For TX Upconversion |
| **LO RX** | Analog Devices ADF4382 | RX 10.5 GHz ± IF_freq Synthesized LO |
| **Balun** | Mini-Circuits MTX2-143+ | Single-to-Differential, IL=1dB (×2) |
| **Attenuator PAD** | ATS1005-3DB-FD-T05 | -3 dB Fixed Attenuation, 0402 Package (×2) |
| **Mixer TX/RX** | Linear Technology LTC5552 | Upconverts/Downconverts IF to/from 10.5 GHz |

---

### RF Chain

| Компонент | Модель | Функция |
|-----------|--------|---------|
| **DAC** | Analog Devices AD9708 | 8-bit, 125 MSPS, Generates IF chirp waveform |
| **TX LPF** | Reconstruction Filter, ~30 MHz | Removes DAC images, Smooths chirp waveform |
| **TX/RX BPF** | 10-11 GHz | Selects TX/RX frequency, Rejects harmonics |
| **RF Switch TX/RX** | Mini-Circuits M3SWA2-34DR+ | Switches TX/RX paths, 30 dB isolation (×2) |
| **Combiner** | Mini-Circuits EP4RKU+ | 4-way power divider, Splits to 4× ADAR1000 |
| **Beamformer** | Analog Devices ADAR1000 ×4 | 4-channel × 4 ICs = 16 channels, Phase & amplitude control |
| **Front-End** | Analog Devices ADTR1107 ×16 | TX/RX switch + LNA + PA driver, 16 independent channels |
| **Power Amplifier** | Qorvo QPA2962 ×16 | 10W GaN per channel, Extended configuration |
| **Circulator** | ×16 | Directs TX to antenna, Protects RX |
| **Opamp (ADC Driver)** | Analog Devices AD8352 | Gain block, ADC driver |
| **ADC** | Analog Devices AD9484 | 8-bit, 500 MSPS, Digitizes IF signal |

---

### Per Tile (каждый из 16 тайлов)

| Компонент | Функция |
|-----------|---------|
| **Ref in** | Приём 100 MHz reference |
| **PLL/LO (ADF4382)** | Локальный гетеродин 10.5 GHz |
| **ADAR1000** | Beamformer (4 канала) |
| **ADTR1107** | TX/RX front-end switch |
| **4×4 AF** | 4×4 антенная решётка (16 элементов) |
| **Local calibration** | Локальная калибровка/коррекция |

---

### Monitoring & Protection

| Компонент | Модель | Функция |
|-----------|--------|---------|
| **Current Sense** | Texas Instruments INA241A3 ×16 | Per-tile PA current monitoring |
| **Monitoring ADC** | Texas Instruments ADS7830 ×3 | 8-bit I2C ADC, Voltage monitoring |
| **Temp Sensors** | TMP37 ×16 | Per-tile temperature monitoring |
| **VSWR Detect** | ×16 | Per-tile reflected power detection |
| **QPA2962 VD RELAY** | High-voltage relay | Drain Voltage Switch |
| **PA Driver** | Texas Instruments OPA4703NA/250 ×2 | Drives QPA2962 Gate |
| **CAL DAC** | Analog Devices AD9708 | For calibration tone |

---

### RX Path

| Компонент | Функция |
|-----------|---------|
| **Hybrid Combiner** | Объединение сигналов (16→4) |
| **ADC (AD9484)** | Оцифровка 500 MSPS, 8-bit |
| **FPGA DSP** | Digital beamforming, обработка |

---

### External Interfaces (ОБНОВЛЕНО)

| Интерфейс | Модель | Скорость | Назначение |
|-----------|--------|----------|------------|
| **10G Ethernet** | XAUI SFP+ | 10 Gbps | **PRIMARY** (UDP streaming) |
| **USB 3.0** | FT601 | 3.2 Gbps | **BACKUP** (Local Debug) |
| **GPIO** | SMA Connectors | 100 Mbps | PPS / Trigger / Sync |
| **Ext Ref In** | SMA Connector | 10 MHz | External OCXO / GPSDO |
| **JTAG** | Connector | 10 Mbps | FPGA Debug & Programming |

---

### Connectors (ОБНОВЛЕНО)

| Коннектор | Назначение |
|-----------|------------|
| **6×2 Connector** | To Microcontroller (Control signals) |
| **7×2 Connector** | To Microcontroller (300 MHz LVDS + 5 MHz LVDS Sync) |
| **2×(2×1) power Connector** | To LOs (+5V0, +3V3_LO, GND) |
| **2×(2×1) power Connector** | To Clock Synth (+1V8_CLOCK, +3V3_CLOCK) |
| **2×1 power Connector** | To XOs (+3V3_XO, GND) |
| **XT30** | Power Input (12-24V, 30A) |

---

### Sensors & Misc

| Компонент | Модель | Функция |
|-----------|--------|---------|
| **IMU** | GY-85 | Motion compensation |
| **Barometer** | BMP180 | Altitude, pressure |
| **GPS** | NEO-6M | Position, timing |
| **Temp Sensor** | TMP37 | Thermal monitoring |
| **Stepper Motor Driver** | TBS6600 | Antenna positioner |
| **Cooling System** | Fans + Heatsink | Thermal management |

---

## ✅ ГЛАВНЫЕ РЕШЕНИЯ (Зафиксировать!)

| № | Решение | Реализация |
|---|---------|------------|
| **1** | **LO topology** | Master ref (OCXO/XO/VCXO) + local PLL per tile (ADF4382) |
| **2** | **TX/RX sync** | Отдельная hardware sync line (GPIO от MCU) |
| **3** | **RX topology** | Hybrid combining (ADAR1000 → Combiner → ADC → FPGA) |
| **4** | **Calibration** | CAL Tone Generator + DAC → OPA → Gate + Correction table |
| **5** | **External Interfaces** | 10G Ethernet (PRIMARY) + USB 3.0 (BACKUP) + GPIO + Ext Ref + JTAG |
| **6** | **Monitoring** | INA241A3 ×16 (per-tile) + ADS7830 ×3 + VSWR Detect ×16 |

---

##  CLOCK DISTRIBUTION (ОБНОВЛЕНО)

| Clock Signal | Frequency | Destination |
|--------------|-----------|-------------|
| **OCXO** | 10 MHz | AD9523 (Clock Synthesizer) |
| **XO** | 100 MHz | AD9523 (Clock Synthesizer) |
| **VCXO** | 100 MHz | AD9523 (For PLL) |
| **CMOS** | 120 MHz | DAC (AD9708) |
| **LVDS** | 400 MHz | ADC (AD9484) |
| **CMOS** | 100 MHz | FPGA (System/reference clock) |
| **LVDS** | 300 MHz | MCU |
| **LVDS Sync** | 5 MHz | MCU (Synchronization) |

---

## 🎯 САМЫЙ КОРОТКИЙ ВЕРДИКТ

```
Правильная 16-tile ФАР = 
  общий reference (OCXO/XO/VCXO → AD9523)
  + sync board (MCU GPIO)
  + локальный LO на тайле (ADF4382 ×2)
  + hybrid RX (ADAR1000 ×4 → Combiner → ADC → FPGA)
  + обязательная calibration loop (CAL Tone + DAC → OPA → Gate)
  + monitoring (INA241A3 ×16 + ADS7830 ×3 + VSWR ×16)
  + external interfaces (10G ETH PRIMARY + USB 3.0 BACKUP + GPIO + Ext Ref + JTAG)
```

---

## 📁 СВЯЗАННЫЕ ФАЙЛЫ

| Файл | Описание |
|------|----------|
| `ARCHITECTURE_16_TILE.md` | Полная документация + Mermaid |
| `AERIS_10N_16_Tile_Architecture.pdf` | Графическая схема |
| `AERIS_10N_MAXIMUM_SIMPLE.pdf` | Простое объяснение (2 стр.) |
| `AERIS_10N_Complete_System.pdf` | Полная схема системы (обновлена) |
| `QWEN.md` | Основная документация проекта |
| `TARGET_ARCHITECTURE_16_TILE.md` | Этот файл (целевая архитектура) |

---

## 🔄 ИЗМЕНЕНИЯ В ВЕРСИИ 2.0 (ОТ 2026-03-31)

| Добавлено | Детали |
|-----------|--------|
| **External Interfaces** | 10G Ethernet (PRIMARY), USB 3.0 (BACKUP), GPIO, Ext Ref, JTAG |
| **Clock System** | OCXO (ECOC-2522), XO (CCHD-957), VCXO (CVHD-950), AD9523 |
| **LO System** | ADF4382 ×2, Balun (MTX2-143+), Attenuator PAD (ATS1005-3DB) |
| **RF Chain** | 2× RF Switch (M3SWA2-34DR+), Combiner (EP4RKU+) |
| **PA Control** | DAC (AD9708) → OPA (OPA4703) → Gate, QPA2962 VD RELAY |
| **Monitoring** | INA241A3 ×16, ADS7830 ×3, VSWR Detect ×16 |
| **Connectors** | 6×2, 7×2, 2×(2×1) power, 2×1 power, XT30 |
| **Misc** | Stepper Driver (TBS6600), Cooling System, Sensors (GY-85, BMP180, NEO-6M, TMP37) |

---

**Этот документ определяет целевую архитектуру AERIS-10N 16-tile Phased Array Radar.**

*Последнее обновление: 2026-03-31 (Версия 2.0 — обновлена по сравнению с RADAR_V6_V2.png)*
