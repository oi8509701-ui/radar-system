# 📐 Чертежи Main Board

## Ожидающие PDF файлы

Этот каталог должен содержать следующие PDF чертежи:

### 1. Schematic_MainBoard.pdf
**Содержание:**
- Полная схема Main Board
- Все страницы (если многостраничная)
- Список компонентов (если включён в экспорт)

**Страницы:**
1. Block Diagram
2. FPGA (XC7A50T/XC7A100T)
3. MCU (STM32F746ZGT7)
4. ADC/DAC (AD9484/AD9708)
5. Clock Distribution (AD9523-1)
6. PLL Synthesizers (ADF4382A ×2)
7. Beamforming (ADAR1000 ×4)
8. Front-end (ADTR1107 ×16)
9. Mixers (LTC5552 ×2)
10. Power Distribution
11. USB Interface (FT601)
12. Connectors & Test Points

**Как экспортировать:** См. `../Docs/EXPORT_PDF_GUIDE.md`

---

### 2. Assembly_Top_MainBoard.pdf
**Содержание:**
- Top silkscreen
- Reference designators
- Component outlines
- Board outline

**Как экспортировать:** Слои 21, 25, 51, 20

---

### 3. Assembly_Bottom_MainBoard.pdf
**Содержание:**
- Bottom silkscreen
- Reference designators (bottom)
- Component outlines (bottom)

**Как экспортировать:** Слои 22, 26, 52, 20

---

### 4. Fabrication_MainBoard.pdf
**Содержание:**
- Top/Bottom copper
- Solder mask
- Drill drawing
- Board outline
- Dimension notes

**Требования:**
- Масштаб: 1:1
- Размер: A2 или A3
- Включить impedance control notes

**Как экспортировать:** Слои 1, 16, 29, 30, 44, 45, 20

---

### 5. Stackup_MainBoard.pdf
**Содержание:**
- Layer stackup diagram
- Material specifications
- Impedance control table
- Via specifications

**Stackup (8 layers):**
| Layer | Material | Thickness | Copper |
|-------|----------|-----------|--------|
| 1 Top | Rogers/FR4 | 0.2mm | 1 oz |
| 2 GND | Prepreg | 0.1mm | — |
| 3 Signal | Core | 0.2mm | 1 oz |
| 4 GND | Prepreg | 0.1mm | — |
| 5 Power | Core | 0.2mm | 1 oz |
| 6 GND | Prepreg | 0.1mm | — |
| 7 Signal | Core | 0.2mm | 1 oz |
| 8 Bottom | FR4 | 0.2mm | 1 oz |

**Total:** ~1.6mm

---

## 📎 Примечания для производителя

### Impedance Control
- **RF traces:** 50Ω ±10%
- **Differential pairs (USB):** 100Ω ±10%
- **Clock lines:** 50Ω controlled

### Via Requirements
- **Via-in-pad:** Для BGA FPGA
- **Filled and plated:** Да
- **Min drill:** 0.2mm
- **Annular ring:** 0.15mm min

### Surface Finish
- **Тип:** ENIG (Immersion Gold)
- **Gold thickness:** 0.05-0.1 μm
- **Nickel thickness:** 3-6 μm

---

## ✅ Checklist перед отправкой

- [ ] Schematic PDF экспортирован
- [ ] Assembly Top PDF экспортирован
- [ ] Assembly Bottom PDF экспортирован
- [ ] Fabrication PDF экспортирован
- [ ] Stackup diagram создан
- [ ] Все PDF проверены в viewer
- [ ] Размеры соответствуют
- [ ] Текст читаемый

---

**Статус:** ⏳ Ожидает экспорта из Eagle
