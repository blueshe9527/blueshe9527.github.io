# import 模組
# 取得現在時間
# 讀取 config工具
# 寫入 log工具
# 檢查網站工具
# 正常訊息工具
# 異常訊息工具
# 錯誤訊息工具
# 建立訊息分辨工具
# 更新統計工具
# 主程式
import requests
import json
import time
from datetime import datetime


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%Y年-%m月-%d日 %H時:%M分:%S秒")
    return current_time


def check_website(URL, TIMEOUT, SLOW_THRESHOLD):
    try:
        response = requests.get(URL, timeout=TIMEOUT)
        response_time = round(response.elapsed.total_seconds(), 3)
        status_code = response.status_code
        if response_time > SLOW_THRESHOLD:
            response_status = "回應偏慢"

        else:
            response_status = "回應正常"

        return status_code, response_time, response_status, None
    except requests.exceptions.RequestException as error:
        response_status = "無法連線"
        return None, None, response_status, error

def normal_message(URL, current_time, response_time, response_status, status_code):
    return f"{URL} {current_time} 回應時間 {response_time} 秒 {response_status} 正常連線 狀態碼 {status_code}\n"

def abnormal_message(URL, current_time, response_time, response_status, status_code):
    return f"{URL} {current_time} 回應時間 {response_time} 秒 {response_status} 異常連線 錯誤碼 {status_code}\n"

def error_message(URL, current_time, error):
    return f"{URL} {current_time} 無法連線 錯誤原因 {error}\n"

def create_message(URL, current_time, response_time, response_status, status_code, error):
    if error is not None:
        message = error_message(URL, current_time, error)
        return message
    elif status_code == 200:
        message = normal_message(URL, current_time, response_time, response_status, status_code)
        return message
    else :
        message = abnormal_message(URL, current_time, response_time, response_status, status_code)
        return message

def load_config():
    with open("config.json", "r", encoding ="utf-8") as file:
        config = json.load(file)
        return config

def write_log(message):
    with open("monitor.log", "a", encoding ="utf-8") as file:
        file.write(message)

def update_count(normal_count, slow_count, error_count, response_status, status_code, error):
    if error is not None:
        error_count += 1
    else:
        if response_status == "回應偏慢":
            slow_count += 1
        if status_code == 200:
            normal_count += 1
        else:
            error_count += 1
    return normal_count, slow_count, error_count

def alert_if_needed(URL, response_status, error): #警告 如果 需要 = 如果需要警告
    if error is not None:
        return f"警告 {URL} 連線失敗\n"
    if response_status == "回應偏慢":
        return f"警告 {URL} 回應偏慢\n"
    return ""

config = load_config()
URLS = config["urls"]
TIMEOUT = config["timeout"]
SLOW_THRESHOLD = config["slow_threshold"]
INTERVAL = config["interval"]

normal_count = 0
slow_count = 0
error_count = 0

while True:
    for URL in URLS:
        current_time = get_current_time()
        status_code, response_time, response_status, error = check_website(URL, TIMEOUT, SLOW_THRESHOLD)
        message = create_message(URL, current_time, response_time, response_status, status_code, error)
        normal_count, slow_count, error_count = update_count(normal_count, slow_count, error_count, response_status, status_code, error)

        print(message, end="")
        write_log(message)

        alert_message = alert_if_needed(URL, response_status, error)
        if alert_message != "":
            write_log(alert_message)
            print(alert_message, end="")
            write_log(alert_message)

    summary = f"正常{normal_count} 偏慢{slow_count} 錯誤{error_count}\n"
    print(summary, end="")

    write_log(summary)
    time.sleep(INTERVAL)

