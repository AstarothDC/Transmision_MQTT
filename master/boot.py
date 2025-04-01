import time
import network
import config

def connect_wifi():
    """ Connect to Wi-Fi."""

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    while not sta_if.isconnected():
        print(f"Conectando a {config.WIFI_SSID}...")
        time.sleep(0.25)

connect_wifi()
print(" Ejecutando main.py ")
