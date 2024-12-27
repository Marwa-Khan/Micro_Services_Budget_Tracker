import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = ["notifications"]

client = mqtt.Client()

def connect_mqtt():
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

def publish_message(topic, message):
    client.publish(topic, message)
