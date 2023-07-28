import paho.mqtt.client as mqtt
import os

CHANNEL = os.getenv("BROKER_CHANNEL")
BROKER_URL = os.getenv("BROKER_URL")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to a topic where you want to receive messages
    client.subscribe(CHANNEL)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print("Received message: " + str(msg.payload.decode()))

class Suscriber:
  def __init__(self):
    # Create an MQTT client instance
    self.client = mqtt.Client()

    # Set the callback functions
    self.client.on_connect = on_connect
    self.client.on_message = on_message

    # Connect to the MQTT broker
    self.client.connect(BROKER_URL)  # Replace 'broker_address' with the actual broker's IP/URL

    # Start the MQTT loop to maintain the connection and process incoming messages
    self.client.loop_forever()
