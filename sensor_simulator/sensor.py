import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "mosquitto"
PORT = 1883
TOPIC = "factory/sensor/data"

client = mqtt.Client("SensorSimulator")
client.connect(BROKER, PORT, 60)

print("IoT Sensor Simulator запущено...")

while True:
    # Симуляція нормальних та аномальних показників
    temperature = round(random.uniform(60.0, 95.0), 2)  # Аномалія > 85.0 C
    vibration = round(random.uniform(0.1, 5.0), 2)
    pressure = round(random.uniform(1.0, 2.5), 2)

    payload = {
        "timestamp": time.time(),
        "device_id": "CNC_MACHINE_01",
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure
    }

    client.publish(TOPIC, json.dumps(payload))
    print(f"[SENSOR] Опубліковано: Temp={temperature}°C, Vib={vibration}, Press={pressure}")
    time.sleep(2)