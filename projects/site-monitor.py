# 目標 監測多網站連線時間以及是否正常 假如不正常請顯示出錯誤碼 並以每60秒掃描一次
import requests  # 導入網路請求模組
import time  # 導入時間控制模組
from datetime import datetime  # h從datetime導入datetime模組

URLS = ["https://api.github.com",
        "https://www.google.com",
        "https://www.youtube.com"
        ]
# 監控的網站清單

while True:  # 迴圈
    for URL in URLS:  # 從清單內一筆一筆抓取資料
        now = datetime.now()  # 將現在電腦時間設定為變數now
        current_time = now.strftime("%Y年-%m月-%d日 %H點:%M分:%S秒")  # 將now格式轉成文字格式設定為變數current_time
        try:
            response = requests.get(URL, timeout=5)  # 將請求網站回應資料設定成response(回應)
            status_code = response.status_code  # 將抓取的資料錯誤碼設為變數status_code(狀態碼)

            if status_code == 200:
              message = f"{URL} {current_time} 正常連線 狀態碼 {status_code}\n"

            else:
              message =f"{URL} {current_time} 異常連線 狀態碼 {status_code}\n"

        except requests.exceptions.RequestException as error:  # 如果請求過程發生錯誤，就把錯誤內容存到 error
              message =f"{URL} {current_time} 連線失敗 錯誤原因 {error}\n"  # 印出目前時間、連線失敗與錯誤原因

        print(message)  # 將 message 顯示在畫面上

        with open("monitor.log", "a", encoding="utf-8") as file:  # 開啟 monitor.log，使用追加模式寫入
             file.write(message)  # 將 message 寫入 monitor.log
    time.sleep(60)
