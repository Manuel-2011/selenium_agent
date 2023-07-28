import paho.mqtt.client as mqtt
import os

CHANNEL = os.getenv("BROKER_CHANNEL")
BROKER_URL = os.getenv("BROKER_URL")

class Publisher:
  def __init__(self):
    self.client = mqtt.Client()

  def send_message(self, message):
    # Connect to the MQTT broker
    self.client.connect(BROKER_URL)  # Replace 'broker_address' with the actual broker's IP/URL
    self.client.publish(CHANNEL, message)
    self.client.disconnect()
