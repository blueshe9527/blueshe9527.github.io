import requests
import time
from datetime import datetime

URLS = [
    "https://api.github.com",
    "https://www.google.com",
    "https://www.youtube.com"
]
while True:
    for URL in URLS:
        now = datetime.now()
        current_time = now.strftime("%Y年-%m月-%d號 %H時:%M分:%S秒")
        try:
            response = requests.get( URL, timeout=5)
            status_code = response.status_code
            response_time = round(response.elapsed.total_seconds(),3)
            if status_code == 200:
                message = f"{URL}{current_time} 回應時間 {response_time} 正常連線 狀態碼 {status_code}\n"
            else:
                message = f"{URL}{current_time} 回應時間 {response_time} 連線異常 錯誤碼 {status_code}\n"
        except requests.exceptions.RequestException as error:
            message = f"{URL}{current_time}無法連線 錯誤原因 {error}\n"
        print(message)
        with open("monitor.log", "a" ,encoding="utf-8" ) as file:
            file.write(message)
    time.sleep(60)

