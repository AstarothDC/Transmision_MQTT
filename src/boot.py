
import network
import time
import config

def connect_wifi():
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True)  # Activar WiFi
    if not wlan.isconnected():
        print(f"Conectando a {config.WIFI_SSID}...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        
        timeout = 10  # 10 intentos
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print("Conectado a WiFi:", wlan.ifconfig())
    else:
        print("No se pudo conectar.")

connect_wifi()
print(" Ejecutando main.py ")
