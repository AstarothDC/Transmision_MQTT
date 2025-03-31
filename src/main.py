import time
import random
from mqtt_client import connect_mqtt, send_mqtt_message
import config

# broker MQTT gratuito
mqtt_client = connect_mqtt()

# Simulación de datos
batch_size = 5  

simulated_data = []

while True:
    # Simular datos de 3 electrodos
    data = {
        "electrode1": random.randint(300, 800),
        "electrode2": random.randint(300, 800),
        "electrode3": random.randint(300, 800),
        "timestamp": time.time()
    }
    
    simulated_data.append(data)

    # Imprimir datos
    print(f"Generado: {data}")

    # Enviar datos en lotes
    if len(simulated_data) >= batch_size:
        send_mqtt_message(mqtt_client, config.MQTT_TOPIC, simulated_data)
        simulated_data.clear()  # Limpiar lista 

    time.sleep(2)  
