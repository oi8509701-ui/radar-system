# 🔄 Конвертация Eagle → KiCad

## 📊 Статус конвертации

**Дата:** 2026-03-30
**Исходный файл:** `MainBoard/RADAR_Main_Board.sch` (Eagle 7.4.0)
**Результат:** `MainBoard/RADAR_Main_Board_Converted.kicad_sch`

---

## ✅ Что сконвертировано:

| Элемент | Eagle | KiCad | Статус |
|---------|-------|-------|--------|
| **Библиотеки** | 18 | 18 | ✅ Конвертировано |
| **Листы** | 4 | 4 | ✅ Конвертировано |
| **Компоненты** | ~100+ | 0 | ⚠️ Требуется доработка |
| **Соединения** | ~200+ | 0 | ⚠️ Требуется доработка |

---

## ⚠️ Проблемы конвертации:

### 1. **Структура Eagle файлов**
Eagle 7.4.0 использует сложную вложенную структуру:
```
<eagle>
  <drawing>
    <schematic>
      <libraries> → 18 библиотек
      <sheets>
        <sheet>
          <parts> → компоненты
          <connectors> → соединения
```

### 2. **Библиотеки компонентов**
Eagle библиотеки не совместимы с KiCad напрямую:
- **Eagle:** `.lbr` файлы
- **KiCad:** `.kicad_sym` символы

**Требуется:**
- Заменить библиотеки Eagle на аналоги KiCad
- Или создать новые символы в KiCad

### 3. **Посадочные места (Footprints)**
- **Eagle:** Встроены в библиотеки
- **KiCad:** Отдельные `.kicad_mod` файлы

**Требуется:**
- Сопоставить посадочные места Eagle с KiCad
- Обновить имена footprints

---

## 📋 Список компонентов (из BOM):

### FPGA:
```
U1: XC7A50T-2FTG256I / XC7A100T-2FTG256I
Footprint: FTG256 (BGA)
```

### MCU:
```
U2: STM32F746ZGT7
Footprint: LQFP144
```

### ADC/DAC:
```
U3: AD9708 → LQFP48
U4: AD9484 → TQFP128
```

### Clock/Synth:
```
U5: AD9523-1 → 64-LFCSP
U6: ADF4382ABCCZ → 32-LFCSP (TX LO)
U7: ADF4382ABCCZ → 32-LFCSP (RX LO)
```

### Beamforming:
```
U8-U11: ADAR1000 → LGA40 (4 шт)
U12-U27: ADTR1107 → LGA24 (16 шт)
```

### Mixer:
```
U28-U29: LTC5552IUDB#TRMPBF → 20-DFN (2 шт)
```

### USB:
```
J1: FT601Q → QFP48
```

### Power:
```
Различные LDO, DC/DC, MOSFET
```

---

## 🔧 Рекомендации по завершению конвертации:

### Вариант 1: Ручная конвертация в KiCad

1. **Открыть KiCad**
   ```bash
   open /Applications/KiCad.app
   ```

2. **Импорт Eagle проекта:**
   - File → Import → Non-KiCad Schematic → Eagle
   - Выбрать `RADAR_Main_Board.sch`
   - Выбрать библиотеки для сопоставления

3. **Проверка ERC:**
   - Tools → Electrical Rules Check
   - Исправить ошибки соединений

4. **Назначение footprints:**
   - Tools → Assign Footprints
   - Сопоставить каждый компонент с footprint KiCad

5. **Сохранить как KiCad:**
   - File → Save As → `RADAR_Main_Board.kicad_sch`

---

### Вариант 2: Использование скрипта конвертации

**Скрипт:** `kicad-mcp-server/eagle2kicad_converter.py`

**Запуск:**
```bash
cd kicad-mcp-server
python eagle2kicad_converter.py
```

**Результат:** `RADAR_Main_Board_Converted.kicad_sch`

**Доработка:**
- Открыть в KiCad
- Заменить символы на правильные из библиотек KiCad
- Проверить соединения
- Назначить footprints

---

### Вариант 3: Пересоздание схемы в KiCad

**Наиболее надёжный вариант для сложной схемы**

1. **Открыть Eagle схему для справки:**
   ```bash
   open MainBoard/RADAR_Main_Board.sch
   ```

2. **Создать новую схему в KiCad:**
   ```bash
   open MainBoard/RADAR_Main_Board.kicad_sch
   ```

3. **Перенести компоненты вручную:**
   - FPGA, MCU, ADC, DAC
   - Clock distribution
   - RF тракты
   - Power distribution

4. **Соединить согласно Eagle схеме**

---

## 📁 Файлы:

| Файл | Описание | Статус |
|------|----------|--------|
| `RADAR_Main_Board.sch` | Eagle схема (оригинал) | ✅ 51K строк |
| `RADAR_Main_Board.brd` | Eagle PCB (оригинал) | ✅ 33K строк |
| `RADAR_Main_Board.kicad_sch` | KiCad схема (пустая) | ⚠️ Каркас |
| `RADAR_Main_Board_Converted.kicad_sch` | KiCad (конверт) | ⚠️ Требует доработки |
| `RADAR_Main_Board.kicad_pcb` | KiCad PCB | ❌ Не создана |

---

## 🎯 Следующие шаги:

1. **Выбрать вариант конвертации** (1, 2 или 3)
2. **Выполнить конвертацию**
3. **Проверить ERC**
4. **Назначить footprints**
5. **Создать PCB в KiCad**

---

## 🔗 Полезные ссылки:

- **KiCad Eagle Import:** https://docs.kicad.org/7.0/en/getting_started_in_kicad/getting_started_in_kicad.html#importing-designs-from-eagle
- **KiCad Libraries:** https://github.com/KiCad/kicad-libraries
- **SnapEDA Footprints:** https://www.snapeda.com/

---

**Статус:** ⚠️ Требуется ручная доработка
**Приоритет:** Высокий (критично для продолжения проекта)
