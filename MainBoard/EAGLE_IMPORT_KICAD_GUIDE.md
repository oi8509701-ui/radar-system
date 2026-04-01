# 🔄 Импорт Eagle схемы в KiCad

## ❌ Проблема автоматической конвертации

Eagle 7.4.0 хранит информацию о компонентах в сложной структуре:
- **Part** в sheet ссылается на **Device** в library
- **Package** определён в library, не в part
- **Соединения** в connectors с ссылками на part/gate/pin

Автоматическая конвертация **не рекомендуется** для сложных схем.

---

## ✅ РЕШЕНИЕ: Импорт через KiCad GUI

### Шаг 1: Открыть KiCad

```bash
open /Applications/KiCad.app
```

### Шаг 2: Импорт Eagle схемы

1. **File → Import → Non-KiCad Schematic → Eagle**
2. **Выбрать файл:**
   ```
   /Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.sch
   ```
3. **Выбрать файл платы (если есть):**
   ```
   /Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.brd
   ```
4. **Нажать "Import"**

### Шаг 3: Сопоставление библиотек

KiCad предложит сопоставить библиотеки Eagle с библиотеками KiCad:

| Eagle Library | KiCad Equivalent |
|---------------|------------------|
| `My_Library` | Создать новую |
| `eagle-ltspice` | `Device` |
| `pinhead` | `Connector` |
| `inductors` | `Inductor` |
| `supply1` | `Power` |
| `packages` | Создать новую |

### Шаг 4: Проверка импорта

1. **Открыть схему:** File → Open → `RADAR_Main_Board.kicad_sch`
2. **Проверить ERC:** Tools → Electrical Rules Check
3. **Проверить компоненты:** Убедиться что все символы на месте

### Шаг 5: Назначение footprints

1. **Tools → Assign Footprints**
2. **Выбрать footprint для каждого компонента:**
   - FPGA: `BGA256` или `FTG256`
   - MCU: `LQFP144`
   - ADC: `TQFP128`
   - DAC: `LQFP48`
   - И т.д.

### Шаг 6: Сохранить

```
File → Save
```

---

## 📋 Список компонентов для импорта

### Критичные компоненты:

| Ref | Component | Package | KiCad Library |
|-----|-----------|---------|---------------|
| **U1** | XC7A50T/XC7A100T | FTG256 | `FPGA_Xilinx` |
| **U2** | STM32F746ZGT7 | LQFP144 | `MCU_STM32` |
| **U3** | AD9708 | LQFP48 | `AD_DAC` |
| **U4** | AD9484 | TQFP128 | `AD_ADC` |
| **U5** | AD9523-1 | 64-LFCSP | `AD_Clock` |
| **U6,U7** | ADF4382 | 32-LFCSP | `AD_PLL` |
| **U8-U11** | ADAR1000 | LGA40 | `AD_RF` |
| **U12-U27** | ADTR1107 | LGA24 | `AD_RF` |
| **U28,U29** | LTC5552 | 20-DFN | `LTC_Mixer` |
| **J1** | FT601Q | QFP48 | `Interface_USB` |

### Пассивные компоненты:

| Component | Package | Quantity | KiCad Library |
|-----------|---------|----------|---------------|
| Resistors | 0201/0402/0603 | ~100 | `Device` |
| Capacitors | 0201/0402/0603 | ~150 | `Device` |
| Inductors | 0402/0603 | ~20 | `Inductor` |
| Ferrite Beads | 0402/0603 | ~30 | `Device` |

---

## 🔧 Альтернатива: Пересоздание схемы

Если импорт не удался, создайте схему заново:

### 1. Подготовить библиотеки

```bash
# Открыть редактор символов
open /Applications/KiCad.app/Contents/MacOS/symbol-editor
```

### 2. Создать символы для ключевых компонентов

- FPGA XC7A50T (BGA256)
- STM32F746 (LQFP144)
- AD9708 (LQFP48)
- AD9484 (TQFP128)
- ADAR1000 (LGA40)
- ADTR1107 (LGA24)

### 3. Разместить компоненты на схеме

Использовать Eagle схему как参考:
```bash
open /Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.sch
```

### 4. Соединить согласно схеме

---

## 📁 Файлы проекта

| Файл | Формат | Статус |
|------|--------|--------|
| `RADAR_Main_Board.sch` | Eagle 7.4 | ✅ Оригинал |
| `RADAR_Main_Board.brd` | Eagle 7.4 | ✅ Оригинал |
| `RADAR_Main_Board.kicad_sch` | KiCad | ⚠️ Пустой |
| `RADAR_Main_Board.kicad_pcb` | KiCad | ❌ Не создан |

---

## 🎯 Рекомендация

**Используйте импорт через KiCad GUI** — это надёжнее автоматической конвертации.

**Время работы:**
- Импорт: 5-10 минут
- Проверка ERC: 10-15 минут
- Назначение footprints: 30-60 минут
- **Итого:** 1-2 часа

---

## 🔗 Ресурсы

- **KiCad Eagle Import Guide:** https://docs.kicad.org/7.0/en/getting_started_in_kicad/getting_started_in_kicad.html#importing-designs-from-eagle
- **KiCad Libraries:** https://github.com/KiCad/kicad-libraries
- **SnapEDA (footprints):** https://www.snapeda.com/
- **Ultra Librarian:** https://www.ultralibrarian.com/

---

**Статус:** ⚠️ Требуется ручной импорт через KiCad GUI
**Приоритет:** КРИТИЧНО для продолжения проекта
