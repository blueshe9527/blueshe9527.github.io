# 程式流程：
# 1. 讀取 config.json 設定檔
# 2. 從設定檔取得網址、檢查間隔、timeout、慢速門檻
# 3. 每一輪逐一檢查所有網站
# 4. 取得狀態碼與回應時間
# 5. 判斷正常、異常、回應偏慢或連線失敗
# 6. 將結果印出並寫入 monitor.log
# 7. 每輪結束後輸出統計摘要
import requests
import time
import json
from datetime import datetime

with open("config.json", "r", encoding="utf-8") as file: #打開設定檔
    config = json.load(file)
URLS = config["urls"] #設定檔中拿出網址
INTERVAL = config["interval"] #從設定檔中拿出間隔時間
TIMEOUT = config["timeout"] #從設定檔中拿出超時
SLOW_THRESHOLD = config["slow_threshold"] #從設定檔中拿出速度多少算慢的門檻
normal_count = 0
slow_count = 0
error_count = 0

while True:
    for URL in URLS:
        now = datetime.now()
        current_time = now.strftime("%Y年-%m月-%d號 %H時:%M分:%S秒")
        try:
            response = requests.get( URL, timeout=TIMEOUT)
            status_code = response.status_code
            response_time = round(response.elapsed.total_seconds(), 3)
            if response_time >SLOW_THRESHOLD :
               speed_status = "回應偏慢"
               slow_count += 1
            else:
               speed_status = "回應正常"

            if status_code == 200:
                message = f"{URL} {current_time} 回應時間 {response_time}秒 {speed_status} 正常連線 狀態碼 {status_code}\n"
                normal_count += 1
            else:
                message = f"{URL} {current_time} 回應時間 {response_time}秒 {speed_status} 連線異常 錯誤碼 {status_code}\n"
                error_count += 1

        except requests.exceptions.RequestException as error:
            message = f"{URL} {current_time} 無法連線 錯誤原因 {error}\n"
            error_count += 1
        with open("monitor.log", "a" , encoding="utf-8") as file:
            file.write(message)
            print(message, end="")

    summary = f"目前正常{normal_count} 速度過慢{slow_count} 錯誤{error_count}\n"
    print(summary, end="")
    with open ("monitor.log", "a" , encoding="utf-8") as file:
        file.write(summary)

    time.sleep(INTERVAL)

