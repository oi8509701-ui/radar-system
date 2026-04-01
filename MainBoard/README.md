# Main Board — Основная плата AERIS-10

## Назначение
Основная плата обработки сигналов радара AERIS-10

## Ключевые компоненты
- **FPGA:** Xilinx Artix-7 (XC7A50T/XC7A100T)
- **MCU:** STM32F746ZGT7 (ARM Cortex-M7)
- **ADC:** AD9484 (500 MSPS, 8-bit)
- **DAC:** AD9708 (125 MSPS, 8-bit)
- **Clock:** AD9523-1
- **PLL:** 2× ADF4382ABCCZ (10.5 GHz)
- **Beamforming:** 4× ADAR1000 (16 каналов)
- **Front-end:** 16× ADTR1107
- **Mixer:** 2× LTC5552

## Функции
- Генерация LFM chirp через DAC
- Приём и оцифровка IF сигнала через ADC
- I/Q down-conversion в FPGA
- Beamforming (электронное управление лучом)
- Обработка: FFT, pulse compression, Doppler, CFAR
- USB 3.0 интерфейс (FT601)
- Управление всеми подсистемами через STM32

## Характеристики
| Параметр | Значение |
|----------|----------|
| Частота | 10.5 ГГц |
| Каналов | 16 |
| FPGA | Artix-7 50T/100T |
| ADC | 500 MSPS |
| DAC | 125 MSPS |
