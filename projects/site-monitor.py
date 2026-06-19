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

import os
import time
import json
import argparse
import requests
from datetime import datetime

def send_line_message(message):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    if not token or not user_id:
        print("LINE_not_configured, skip sending message")
        return False
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization":f"Bearer {token}","Content-Type":"application/json"}
    payload = {"to":user_id,"messages":[{"type":"text","text":message}]}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print("LINE_send_successfully")
            return True
        else:
            print("LINE_send_failed")
            print(response.status_code)
            print(response.text)
            return False
    except requests.exceptions.RequestException as error:
        print("LINE_send_error")
        print(error)
        return False




def parse_args():
    parser = argparse.ArgumentParser(description = "參數控制器")
    parser.add_argument("--once", action="store_true" , help="執行一次")
    parser.add_argument("--interval", type=int , help="間隔幾秒")
    parser.add_argument("--timeout", type=int, help="超時幾秒")
    parser.add_argument("--slow-threshold", type=float, help="慢速臨界點")
    return parser.parse_args()

def get_current_time():
    current_time = datetime.now().strftime('%Y年-%m月-%d日 %H時:%M分:%S秒')
    return current_time

def check_website(url, timeout, slow_threshold):
    try:
        response = requests.get(url, timeout=timeout)
        status_code = response.status_code
        response_time = round(response.elapsed.total_seconds(), 3)
        if response_time > slow_threshold:
            response_speed = "回應偏慢"
        else:
            response_speed = "回應正常"
        if status_code == 200:
            connection_status = "連線正常"
        else:
            connection_status = "異常連線"
        return status_code, response_time, response_speed, connection_status, None
    except requests.exceptions.RequestException as error:
        return None, None, "無法取得速度", "無法連線", error

def normal_message(url, current_time, response_time, response_speed, connection_status, status_code):
    return f"{url} {current_time} 回應時間{response_time}秒 速度狀態{response_speed} 連線狀態{connection_status} 狀態碼{status_code}\n"
def abnormal_message(url, current_time, response_time, response_speed, connection_status, status_code):
    return f"{url} {current_time} 回應時間{response_time}秒 速度狀態{response_speed} 連線狀態{connection_status} 錯誤碼{status_code}\n"
def error_message(url, current_time, error):
    return f"{url} {current_time} 無法連線 錯誤原因 {error}\n"
def create_message(url, current_time, response_time, response_speed, connection_status, status_code, error):
    if error is not None:
        return error_message(url, current_time, error)
    if status_code == 200:
        return normal_message(url, current_time, response_time, response_speed, connection_status, status_code)
    return abnormal_message(url, current_time, response_time, response_speed, connection_status, status_code)

def update_count(normal_count, slow_count, error_count, response_speed, status_code, error):
    if error is not None:
        error_count += 1
    elif status_code != 200:
        error_count +=1
    elif response_speed == "回應偏慢":
        slow_count +=1
    else:
        normal_count += 1
    return normal_count, slow_count, error_count

def config_log():
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
        return config

def write_log(message):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    filename = get_log_filename()
    with open(filename, "a", encoding="utf-8") as file:
        file.write(message)

def get_log_filename():
    today = datetime.today().strftime('%Y年%m月%d日')
    filename = f"logs/qq{today}.log"
    return filename

def alert_if_needed(url, current_time, response_time, response_speed, connection_status, status_code, error):
    if error is not None:
        return f"警告{url} {current_time} 無法連線 錯誤原因 {error}\n"
    if status_code != 200:
            return f"警告{url} {current_time} 回應時間{response_time}秒 連線狀態 {connection_status} 錯誤碼 {status_code}\n"
    if response_speed == "回應偏慢":
            return f"警告{url} {current_time} 回應時間{response_time}秒 連線狀態 {connection_status} 狀態碼 {status_code}\n"
    return ""



args = parse_args()
config = config_log()
URLS = config["urls"]
INTERVAL = args.interval or config["interval"]
TIMEOUT = args.timeout or config["timeout"]
SLOW_THRESHOLD = args.slow_threshold or config["slow_threshold"]
normal_count = 0
slow_count = 0
error_count = 0

while True:
    for url in URLS:
        current_time = get_current_time()
        status_code, response_time, response_speed, connection_status, error = check_website(url, TIMEOUT, SLOW_THRESHOLD)
        message = create_message(url, current_time, response_time, response_speed, connection_status, status_code, error)
        alert_message = alert_if_needed(url, current_time, response_time, response_speed, connection_status, status_code, error)
        normal_count,slow_count,error_count = update_count(normal_count, slow_count, error_count, response_speed, status_code, error)

        if alert_message:
            print(alert_message, end="")
            write_log(alert_message)
            send_line_message("發生錯誤")
        else:
            print(message, end="")
            send_line_message("正常運作中")
            write_log(message)


    summary = f"普通{normal_count} 偏慢{slow_count} 錯誤{error_count}\n"
    print(summary, end="")
    write_log(summary)
    if args.once:
        break
    time.sleep(INTERVAL)
