import time
import random
import os
import machine
from adc_reader import read_adc
from Single_señal import read_adc_sigle
from mqtt_client import connect_mqtt, send_mqtt_message
from storage import save_data  
import config
from ds3231 import DS3231  
from collections import OrderedDict

# Conexión con el broker MQTT
mqtt_client = connect_mqtt()

# Configuración
batch_size = 5  # Cantidad de muestras antes de guardar en SD
mqtt_send_interval = 180  # Enviar por MQTT cada 3 minutos (180 segundos)
simulated_data = []  # Lista para guardar datos antes de escribir en SD
mqtt_data_batch = []  # Lista para acumular datos antes de enviarlos por MQTT
last_mqtt_send_time = time.time()  # Tiempo de la última transmisión por MQTT

# Inicializar I2C para el RTC DS3231
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
rtc_ds3231 = DS3231(i2c)

# Ajuste de zona horaria (UTC-5 para Colombia)
TIMEZONE_OFFSET = -5 * 3600  # -5 horas en segundos

def get_current_time():
    """ Obtiene la hora actual desde el RTC DS3231 en formato timestamp y hora local """
    try:
        year, month, day, _, hour, minute, second, _ = rtc_ds3231.datetime()
        
        # Convertir a timestamp (sin ajuste)
        timestamp_utc = time.mktime((year, month, day, hour, minute, second, 0, 0, 0))
        
        # Ajustar a la zona horaria de Colombia (UTC-5)
        timestamp_local = timestamp_utc + TIMEZONE_OFFSET

        # Formatear manualmente la fecha y hora
        formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            year, month, day, hour, minute, second
        )

        return int(timestamp_local), formatted_time

    except Exception as e:
        print("⚠️ Error obteniendo la hora del RTC:", e)
        timestamp = int(time.time() + TIMEZONE_OFFSET)  # Si falla, usar el tiempo interno ajustado
        return timestamp, "Error obteniendo la hora"

def save_data_to_sd(data_batch):
    """ Guarda un lote de datos en la SD si está montada """
    if "sd" in os.listdir("/"):
        save_data(data_batch)  # Llama directamente a la función en storage.py
    else:
        print("No se puede escribir en la SD porque no está montada.")

while True:
    # Leer señal ECG desde el sensor AD8232
    adc_values = read_adc()
    timestamp, formatted_time = get_current_time()
    data = OrderedDict([
        ("electrode1", adc_values["electrode1"]),
        ("electrode2", adc_values["electrode2"]),
        ("electrode3", adc_values["electrode3"]),
        ("timestamp", (timestamp, formatted_time))
    ])
    
    simulated_data.append(data)
    mqtt_data_batch.append(data)  # También lo añadimos al lote para MQTT
    print(f"Generado: {data}")

    # Guardar en SD cada 5 muestras
    if len(simulated_data) >= batch_size:
        save_data_to_sd(simulated_data)  # Guardamos en la SD si está disponible
        simulated_data.clear()  # Limpiar lista tras almacenamiento

    # Enviar datos por MQTT cada 3 minutos
    if time.time() - last_mqtt_send_time >= mqtt_send_interval:
        if mqtt_data_batch:
            try:
                send_mqtt_message(mqtt_client, config.MQTT_TOPIC, mqtt_data_batch)
                print(f"📡 Datos enviados por MQTT: {len(mqtt_data_batch)} muestras")
            except Exception as e:
                print(f"⚠️ Error al enviar por MQTT: {e}")
            mqtt_data_batch.clear()
            last_mqtt_send_time = time.time()

    time.sleep(1)  # Intervalo de tiempo entre mediciones
 