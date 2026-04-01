# 📦 Production Package - MainBoard

**Дата:** 2026-03-29 09:04  
**Плата:** Main Board - FPGA, MCU, RF Front-end

---

## 📁 Содержимое

### Gerber Files
- `Gerber/` - Gerber файлы для производства PCB
  - `*.gbr` - Слои меди
  - `*.gts` / `*.gbs` - Solder mask
  - `*.gto` / `*.gbo` - Silkscreen
  - `*.gko` - Board outline
  - `*.drl` - Drill file

### 3D Model
- `3D/MainBoard.step` - 3D модель в формате STEP

### Assembly
- `pick_and_place.csv` - Координаты установки компонентов

---

## 🏭 Требования к производству

### PCB Specifications
- **Layers:** 7
- **Material:** FR-4 / Rogers (для RF плат)
- **Thickness:** 1.6mm
- **Copper:** 1 oz (35 μm)
- **Surface Finish:** ENIG
- **Impedance Control:** 50Ω (для RF трасс)

### Notes
- Main Board - FPGA, MCU, RF Front-end
- Проверить импеданс RF трасс
- ENIG покрытие обязательно

---

## 📎 Файлы для отправки производителю

1. **Gerber:** Папка `Gerber/` (все .gbr файлы)
2. **Drill:** `*.drl` файлы из папки `Gerber/`
3. **BOM:** См. корень проекта `BOM_Master.csv`
4. **Pick&Place:** `pick_and_place.csv`

---

## ✅ Checklist

- [ ] Gerber файлы проверены в viewer
- [ ] Drill файл соответствует отверстиям
- [ ] Silkscreen читаемый
- [ ] Импеданс указан в notes
- [ ] BOM актуальный

---

**Сгенерировано автоматически через MCP Automation**
