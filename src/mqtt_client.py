from umqtt.simple import MQTTClient
import config
import json

def connect_mqtt():
    """ Establece conexión con el servidor MQTT """
    client = MQTTClient("holter", config.MQTT_BROKER, port=config.MQTT_PORT)
    client.connect()
    print("Conectado a MQTT")
    return client

def send_mqtt_message(client, topic, data):
    """ Publica un JSON en el servidor MQTT """
    json_data = json.dumps(data)  # Convierte a JSON
    client.publish(topic, json_data)
    print(f"Mensaje enviado: {json_data}")
