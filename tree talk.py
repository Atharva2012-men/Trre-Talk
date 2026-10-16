
import network
import time
import machine
import urequests

# =================================
# SMART TREE TALK - ESP32 PROJECT
# =================================

# Example Wi-Fi details (replace these)
WIFI_NAME = "MyHomeWiFi"
WIFI_PASSWORD = "TreeTalk123"

# Fake Blynk token (replace with your real token)
BLYNK_TOKEN = "1234567890abcdef1234567890abcdef"

# Sensor pins for a compatible ESP32 DevKit
moisture_sensor = machine.ADC(machine.Pin(34))
ph_sensor = machine.ADC(machine.Pin(35))

moisture_sensor.atten(machine.ADC.ATTN_11DB)
ph_sensor.atten(machine.ADC.ATTN_11DB)

moisture_sensor.width(machine.ADC.WIDTH_12BIT)
ph_sensor.width(machine.ADC.WIDTH_12BIT)

# Example calibration values - calibrate your sensors!
DRY_VALUE = 3200
WET_VALUE = 1400

# Example pH calibration readings
PH7_RAW = 2000
PH4_RAW = 2500


# Connect to Wi-Fi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        print("Connecting to Wi-Fi...")
        wifi.connect(WIFI_NAME, WIFI_PASSWORD)

        for attempt in range(20):
            if wifi.isconnected():
                break
            time.sleep(1)

    if wifi.isconnected():
        print("Wi-Fi connected!")
        print(wifi.ifconfig())
    else:
        print("Wi-Fi connection failed!")

    return wifi


# Read soil moisture
def read_moisture():
    raw = moisture_sensor.read()

    if DRY_VALUE == WET_VALUE:
        return 0

    percent = (DRY_VALUE - raw) * 100 / (DRY_VALUE - WET_VALUE)
    percent = max(0, min(100, percent))

    return round(percent)


# Read approximate soil pH
def read_ph():
    raw = ph_sensor.read()

    if PH7_RAW == PH4_RAW:
        return None

    ph = 7 + (raw - PH7_RAW) * (4 - 7) / (PH4_RAW - PH7_RAW)

    return round(max(0, min(14, ph)), 2)


# Send information to Blynk
def send_to_blynk(pin, value):
    url = (
        "https://blynk.cloud/external/api/update"
        "?token=" + BLYNK_TOKEN
        + "&" + pin + "=" + str(value)
    )

    try:
        response = urequests.get(url)
        print("Sent", pin, ":", value,
              "Status:", response.status_code)
        response.close()
    except Exception as error:
        print("Blynk upload error:", error)


# Main program
wifi = connect_wifi()

while True:
    try:
        if not wifi.isconnected():
            wifi = connect_wifi()

        if wifi.isconnected():
            moisture = read_moisture()
            ph = read_ph()

            # Give the plant a message
            if moisture < 30:
                message = "Plant needs water"
            elif moisture > 80:
                message = "Soil is very wet"
            else:
                message = "Moisture looks okay"

            # Display readings in the serial console
            print("\n--- SMART TREE TALK ---")
            print("Soil moisture:", moisture, "%")
            print("Soil pH:", ph)
            print("Tree says:", message)

            # Upload to Blynk virtual pins
            send_to_blynk("V0", moisture)

            if ph is not None:
                send_to_blynk("V1", ph)

            send_to_blynk("V2", message)

        time.sleep(10)

    except Exception as error:
        print("Program error:", error)
        time.sleep(5)


