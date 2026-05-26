import time
from datetime import datetime

VERSION = "1.0.0.3"

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"그린그라스 배포 테스트 {now} VER{VERSION}")
    time.sleep(3)
