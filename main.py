# Smart Tree Talk - ESP32 MicroPython starter
# IMPORTANT:
# 1. Replace the example Wi-Fi and Blynk values.
# 2. These calibration values are examples only.
# 3. This starter monitors sensors; it does NOT control a pump.
# 4. Check your exact ESP32 board pinout and sensor output voltages.

import network
import time
import machine
try:
    import urequests
except ImportError:
    urequests = None

# Example values only — replace with your own credentials.
WIFI_NAME = "MyHomeWiFi"
WIFI_PASSWORD = "TreeTalk123"
BLYNK_TOKEN = "REPLACE_WITH_YOUR_REAL_BLYNK_TOKEN"

# Example pins for a compatible classic ESP32 DevKit.
# GPIO34 and GPIO35 are ADC inputs on many classic ESP32 boards,
# but pin availability differs on other ESP32 models.
MOISTURE_PIN = 34
PH_PIN = 35

# Example calibration values. Calibrate your actual sensor!
DRY_VALUE = 3200
WET_VALUE = 1400

# Example raw ADC values in pH buffer solutions.
# Replace these with actual calibration readings.
PH7_RAW = 2000
PH4_RAW = 2500

BLYNK_BASE_URL = "https://blynk.cloud/external/api/update"


def make_adc(pin_number):
    adc = machine.ADC(machine.Pin(pin_number))
    adc.atten(machine.ADC.ATTN_11DB)
    adc.width(machine.ADC.WIDTH_12BIT)
    return adc


moisture_sensor = make_adc(MOISTURE_PIN)
ph_sensor = make_adc(PH_PIN)


def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if wifi.isconnected():
        print("Wi-Fi already connected")
        return wifi

    print("Connecting to Wi-Fi...")
    try:
        wifi.connect(WIFI_NAME, WIFI_PASSWORD)
        for _ in range(20):
            if wifi.isconnected():
                print("Wi-Fi connected:", wifi.ifconfig())
                return wifi
            time.sleep(1)
    except Exception as error:
        print("Wi-Fi error:", error)

    print("Wi-Fi connection failed. Check the name/password and 2.4 GHz support.")
    return wifi


def read_moisture():
    raw = moisture_sensor.read()

    if DRY_VALUE == WET_VALUE:
        print("ERROR: moisture calibration values are identical")
        return None

    percent = (DRY_VALUE - raw) * 100 / (DRY_VALUE - WET_VALUE)
    percent = max(0, min(100, percent))
    return round(percent)


def read_ph():
    raw = ph_sensor.read()

    if PH7_RAW == PH4_RAW:
        print("ERROR: pH calibration values are identical")
        return None

    # Simple two-point linear approximation only.
    # Real pH modules may require voltage conversion, temperature
    # compensation, and a calibration procedure from the manufacturer.
    ph_value = 7 + (raw - PH7_RAW) * (4 - 7) / (PH4_RAW - PH7_RAW)
    ph_value = max(0, min(14, ph_value))
    return round(ph_value, 2)


def plant_message(moisture):
    if moisture is None:
        return "Moisture sensor needs checking"
    if moisture < 30:
        return "Soil may be dry; check the plant"
    if moisture > 80:
        return "Soil is very wet; check drainage"
    return "Moisture reading is in the middle range"


def send_to_blynk(pin, value):
    if urequests is None:
        print("Cannot upload: urequests is not installed")
        return

    if not BLYNK_TOKEN or BLYNK_TOKEN == "REPLACE_WITH_YOUR_REAL_BLYNK_TOKEN":
        print("Demo mode: set your real BLYNK_TOKEN to upload readings")
        return

    url = (
        BLYNK_BASE_URL
        + "?token=" + BLYNK_TOKEN
        + "&" + pin + "=" + str(value)
    )

    response = None
    try:
        response = urequests.get(url)
        print("Blynk update", pin, "status:", response.status_code)
    except Exception as error:
        print("Blynk upload error:", error)
    finally:
        if response is not None:
            response.close()


def main():
    wifi = connect_wifi()

    while True:
        try:
            if not wifi.isconnected():
                wifi = connect_wifi()

            if wifi.isconnected():
                moisture = read_moisture()
                ph_value = read_ph()
                message = plant_message(moisture)

                print("\\n--- SMART TREE TALK ---")
                print("Soil moisture:", moisture, "%")
                print("Approximate soil pH:", ph_value)
                print("Tree says:", message)

                if moisture is not None:
                    send_to_blynk("V0", moisture)
                if ph_value is not None:
                    send_to_blynk("V1", ph_value)
                send_to_blynk("V2", message)
            else:
                print("Offline: readings not uploaded")

            time.sleep(10)

        except Exception as error:
            print("Program error:", error)
            time.sleep(5)


main()
