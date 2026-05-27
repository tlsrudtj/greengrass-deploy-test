import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt

VERSION = "1.0.0.9"

MQTT_BROKER = "172.17.0.3"
MQTT_PORT = 1883

TOPIC_PUBLISH = "r5/test/status"
TOPIC_SUBSCRIBE = "r5/test/command"

connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        connected = True
        print(f"[MQTT] EMQX 연결 성공")
        client.subscribe(TOPIC_SUBSCRIBE)
        print(f"[MQTT] 구독 시작: {TOPIC_SUBSCRIBE}")
    else:
        print(f"[MQTT] 연결 실패 rc={rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[MQTT] 수신 | topic: {msg.topic} | payload: {payload}")

def on_disconnect(client, userdata, rc):
    global connected
    connected = False
    print(f"[MQTT] 연결 끊김 rc={rc}")

client = mqtt.Client(client_id="r5-app-v8")  # client_id 변경
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()

# 연결 완료까지 대기
timeout = 10
elapsed = 0
while not connected and elapsed < timeout:
    time.sleep(0.1)
    elapsed += 0.1

if not connected:
    print("[MQTT] 연결 타임아웃! EMQX 브로커 확인 필요")
else:
    print("[MQTT] 연결 완료, 발행 시작")

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
    time.sleep(30)