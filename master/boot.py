import time
import os
import machine
import ntptime
import network
import config
import sdcard
from ds3231 import DS3231

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

# Intentar conectar a Wi-Fi
connect_wifi()
time.sleep(2)

spi = machine.SPI(2, baudrate=1000000, polarity=0, phase=0, 
                  sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
cs = machine.Pin(5, machine.Pin.OUT)

try:
    print("⏳ Intentando montar la tarjeta SD...")
    time.sleep(1)  # Retraso antes de inicializar la SD
    
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    print("Tarjeta SD montada exitosamente en /sd.")

    # Verificar contenido de la SD
    print("Contenido de la SD:", os.listdir("/sd"))

except OSError as e:
    print(f"Error OSError al montar la SD: {e}")
except Exception as e:
    print(f"Error inesperado al montar la SD: {e}")

TIMEZONE_OFFSET = -5 * 3600  # -5 horas en segundos

def sync_rtc():
    i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))  # Ajusta los pines según tu ESP32
    ds3231 = DS3231(i2c)
    rtc = machine.RTC()

    if network.WLAN(network.STA_IF).isconnected():
        try:
            print("⏳ Obteniendo hora de internet...")
            ntptime.settime()  # Ajusta la hora del sistema (en UTC)
            utc_time = time.localtime(time.time() + TIMEZONE_OFFSET)  # Ajustar a UTC-5
            
            # Configurar la hora ajustada en el RTC interno y en el DS3231
            rtc.datetime((utc_time[0], utc_time[1], utc_time[2], utc_time[6], utc_time[3], utc_time[4], utc_time[5], 0))
            ds3231.datetime((utc_time[0], utc_time[1], utc_time[2], utc_time[3], utc_time[4], utc_time[5], utc_time[6]))

            print("Hora sincronizada desde NTP:", utc_time)
        except Exception as e:
            print("Error sincronizando RTC desde NTP:", e)
    else:
        try:
            print("🔄 Cargando hora desde el RTC DS3231...")
            rtc_time = ds3231.datetime()
            rtc.datetime((rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[6], rtc_time[3], rtc_time[4], rtc_time[5], 0))
            print("Hora cargada desde el RTC:", time.localtime())
        except Exception as e:
            print("Error obteniendo hora desde RTC DS3231:", e)

# Ejecutar sincronización del RTC
sync_rtc()
print("Ejecutando main.py")
