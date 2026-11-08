#  Smart Factory Monitoring System (IoT Edge + Cloud Integration)

Розподілена IoT-система моніторингу промислового обладнання на базі **Edge Computing** та **Cloud Integration** з використанням **Docker containers**.

Проєкт реалізовано в рамках Практичної роботи 9.2 (Частина 2) з дисципліни *«Технології IoT та SMART-технології»*.

---

##  Архітектура системи

Система побудована за мікросервісною архітектурою та складається з 5 контейнеризованих компонентів:

```text
[ IoT Sensor Simulator ] 
           │ (MQTT: factory/sensor/data)
           ▼
   [ MQTT Broker ]
           │
           ▼
  [ Edge Processor ] ──────────────► [ Critical Alerts (Console Log) ]
           │ (Real-time Anomaly Check: Temp > 85°C)
           ▼
     [ InfluxDB ] (Time-series Storage)
           │
           ▼
      [ Grafana ] (Cloud Analytics & Visualization)
