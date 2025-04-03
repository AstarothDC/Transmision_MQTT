from simple import MQTTClient
import config
import json
import time

def connect_mqtt():
    """ Intenta conectar con el servidor MQTT y maneja errores. """
    client = MQTTClient("holter", config.MQTT_BROKER, port=config.MQTT_PORT)

    try:
        client.connect()
        print("Conectado a MQTT")
        return client
    except Exception as e:
        print(f"Error al conectar MQTT: {e}")
        return None

def send_mqtt_message(client, topic, data, qos=0, retain=False):
    """ Publica un mensaje en formato JSON en el servidor MQTT. """
    if client is None:
        print("No hay conexión MQTT. Intentando reconectar...")
        client = connect_mqtt()
        if client is None:
            return

    try:
        json_data = json.dumps(data)
        client.publish(topic, json_data, qos=qos, retain=retain)
        print(f"Mensaje enviado a {topic}: {json_data}")
    except Exception as e:
        print(f"Error enviando mensaje MQTT: {e}")

def reconnect_mqtt(client):
    """ Reintenta conectar en caso de desconexión """
    while client is None:
        print("Intentando reconectar...")
        client = connect_mqtt()
        if client:
            print("Reconectado con éxito")
            return client
        time.sleep(5)  # Espera antes de reintentar
