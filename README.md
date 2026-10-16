# Smart Tree Talk 🌱

## About the Project
Smart Tree Talk is a student hardware project designed to help people understand what a plant may need. An ESP32 reads sensor data and can send it to a mobile dashboard so users can check soil moisture and, after suitable calibration, soil pH. The long-term goal is to make plant care easier through clear messages and optional automatic watering.

## Project Status
**Status: In development.** The circuit, sensor readings, app connection, and watering system must be tested with the actual components before they are described as working.

## Planned Features
- Measure soil moisture.
- Measure soil pH using a compatible pH probe and interface module.
- Display readings on a Blynk IoT dashboard.
- Show simple plant-care messages.
- Add a low-voltage water pump with a suitable driver after testing.
- Explore voice messages and temperature/humidity monitoring in the future.

## Components
- ESP32 development board
- Breadboard and jumper wires
- Soil moisture sensor
- pH probe and compatible interface module
- USB cable and suitable power supply
- Optional low-voltage water pump and suitable driver/relay
- Optional display

See [`components.md`](components.md) for details.

## How It Is Intended to Work
1. Sensors measure soil conditions.
2. The ESP32 reads their electrical signals.
3. Calibration converts raw readings into approximate moisture percentage and pH.
4. The ESP32 sends values to Blynk over Wi-Fi.
5. The dashboard displays the values and a simple message.
6. Automatic watering may be added after the readings and pump circuit are tested.

## Software
- MicroPython on the ESP32
- Thonny IDE (or another compatible editor)
- Blynk IoT for the dashboard
- `urequests` if it is not already available in the firmware

## Getting Started
1. Install MicroPython on a compatible ESP32 board.
2. Open `main.py` in Thonny.
3. Create a Blynk device and configure datastreams:
   - `V0`: moisture percentage (Integer, 0–100)
   - `V1`: pH value (Double, 0–14)
   - `V2`: plant message (String)
4. Enter your own Wi-Fi name, Wi-Fi password, and Blynk token in the code—or preferably load them from a separate local secrets file that is not committed.
5. Check the pinout and voltage limits of your exact board and sensor modules before wiring.
6. Calibrate the sensors using appropriate reference conditions and compare readings with reliable measurements.
7. Test the dashboard and circuit before considering pump automation.

## Safety
- Never connect a pump directly to an ESP32 GPIO pin.
- Use a suitable driver/relay and a properly rated separate supply for the pump.
- Keep water away from exposed electronics.
- Ensure sensor outputs do not exceed the ESP32 input voltage limits.
- Do not rely on example calibration values for real plant-care decisions.
- Do not commit Wi-Fi credentials or authentication tokens to GitHub.

## Repository Contents
- `main.py` — starter MicroPython program
- `components.md` — component checklist
- `wiring.md` — preliminary wiring guide
- `journal.md` — development journal template
- `images/` — place real circuit and dashboard photos here
- `.gitignore` — excludes local secrets and temporary files

## Future Improvements
- Voice messages explaining plant conditions
- Mobile dashboard improvements
- Temperature and humidity sensing
- Safer automatic watering with time limits and dry-run protection
- Better sensor calibration and testing records

## Development Journal
See [`journal.md`](journal.md). Add dated notes, real photos, test results, and problems solved as the project progresses.

## Acknowledgements
This project is a learning exercise combining electronics, MicroPython, sensors, and IoT. Component behavior and readings depend on the exact hardware and calibration.
