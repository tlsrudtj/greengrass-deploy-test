import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt

VERSION = "1.0.1.10"

MQTT_BROKER = "172.17.0.1"  # Docker bridge 게이트웨이 (호스트)
MQTT_PORT = 1883

TOPIC_PUBLISH = "status/order_manager/robot_manager"
TOPIC_SUBSCRIBE = "event/robot_manager/submit_task"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] EMQX 연결 성공")
        client.subscribe(TOPIC_SUBSCRIBE)
        print(f"[MQTT] 구독 시작: {TOPIC_SUBSCRIBE}")
    else:
        print(f"[MQTT] 연결 실패 rc={rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[MQTT] 수신 | topic: {msg.topic} | payload: {payload}")

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] 연결 끊김 rc={rc}")

client = mqtt.Client(client_id="r5-app-container")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = json.dumps({
        "version": VERSION,
        "timestamp": now,
        "status": "running",
        "manager_id": "AZ.RM1"
    })
    client.publish(TOPIC_PUBLISH, payload)
    print(f"[MQTT] 발행 | topic: {TOPIC_PUBLISH} | {payload}")
    time.sleep(3)