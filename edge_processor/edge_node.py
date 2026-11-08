import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

BROKER = "mosquitto"
PORT = 1883
TOPIC = "factory/sensor/data"

INFLUX_URL = "http://influxdb:8086"
INFLUX_TOKEN = "my-super-secret-token"
INFLUX_ORG = "factory_org"
INFLUX_BUCKET = "factory_metrics"

# Підключення до InfluxDB
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def process_edge_data(payload):
    temp = payload.get("temperature", 0)
    device_id = payload.get("device_id", "unknown")
    
    # 1. Edge Processing: Real-time Anomaly Detection
    if temp > 85.0:
        print(f"[EDGE ALERT] ⚠️ АНОМАЛІЯ! Критична температура на {device_id}: {temp}°C")
    else:
        print(f"[EDGE OK] Нормальні показники: {temp}°C")

    # 2. Local/Cloud Storage Sync (InfluxDB)
    point = Point("machine_stats") \
        .tag("device_id", device_id) \
        .field("temperature", temp) \
        .field("vibration", payload.get("vibration", 0.0)) \
        .field("pressure", payload.get("pressure", 0.0)) \
        .time(int(payload.get("timestamp")), WritePrecision.S)
    
    write_api.write(bucket=INFLUX_BUCKET, record=point)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        process_edge_data(data)
    except Exception as e:
        print(f"Помилка обробки: {e}")

mqtt_client = mqtt.Client("EdgeProcessor")
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.subscribe(TOPIC)

print("Edge Processor запущено, очікування даних...")
mqtt_client.loop_forever()