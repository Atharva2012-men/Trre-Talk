# Preliminary Wiring Guide

**Important:** This is a starter plan, not a verified wiring diagram for every board/module. Check the exact product labels, data sheets, and ESP32 pinout before powering the circuit.

## Basic sensor connections (example: classic ESP32 DevKit)

| Module | Module pin | ESP32 connection |
|---|---|---|
| Moisture sensor | VCC | Supply voltage supported by that sensor module |
| Moisture sensor | GND | GND |
| Moisture sensor | AO / analog output | GPIO34 (ADC input on many classic ESP32 DevKit boards) |
| pH interface module | VCC | Supply specified by the module |
| pH interface module | GND | GND |
| pH interface module | Analog output | GPIO35 only if its output voltage is safe for the ESP32 ADC |

## Critical voltage warning
ESP32 GPIOs are not 5 V tolerant. Do not connect a sensor output to an ESP32 pin unless you have confirmed the voltage is within the board's allowed input range. Some pH interface boards output voltages that require a suitable divider or conditioning circuit. Never guess—check the module documentation and measure safely.

## Pump (future feature; not included in starter code)
- Do not connect the pump directly to an ESP32 GPIO.
- Use a properly rated transistor/MOSFET driver or suitable relay module, plus any required flyback protection for a DC motor.
- Use a suitable separate supply for the pump.
- Follow the driver module's wiring instructions and keep water away from electronics.
- Add a fuse/current protection and a timeout or maximum-run limit where appropriate.
- Test with supervision and a small amount of water only after the circuit is verified.

## Calibration
- Moisture: record raw readings in representative dry and wet soil, then update `DRY_VALUE` and `WET_VALUE` in `main.py`. Sensor orientation, soil type, and salinity affect readings.
- pH: follow the pH kit manufacturer's instructions and use suitable calibration buffer solutions. Do not assume the example ADC values correspond to real pH values.
- Compare readings with a reliable reference before using them for plant-care decisions.
