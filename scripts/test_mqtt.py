from mqtt_client import connect_mqtt, send_mqtt_message

client = connect_mqtt()
send_mqtt_message(client, "holter/test", "Prueba de MQTT")
