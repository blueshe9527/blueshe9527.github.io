# Python 多網站連線監控工具

這是一個使用 Python 撰寫的網站連線監控小工具，可以定期檢查多個網站是否正常連線，並顯示檢查時間與 HTTP 狀態碼。

## 功能

- 可監測多個網站
- 每 60 秒自動檢查一次
- 顯示目前檢查時間
- 顯示 HTTP 狀態碼
- 狀態碼為 200 時顯示正常連線
- 狀態碼不是 200 時顯示異常連線
- 使用 try / except 處理連線失敗，避免程式中斷
- 將每次監控結果寫入 monitor.log 紀錄檔
## 使用技術

- Python
- requests
- datetime
- time
- HTTP status code
- exception handling

## 程式概念

這個作品主要練習以下 Python 基礎：

- 使用 list 儲存多個網站網址
- 使用 for 迴圈逐一檢查網站
- 使用 while True 讓程式持續執行
- 使用 requests.get() 向網站發送請求
- 使用 response.status_code 取得網站狀態碼
- 使用 try / except 處理網路連線錯誤
- 使用 time.sleep() 控制檢查間隔

## 執行方式

先安裝 requests：

```bash
pip install requests
```

執行程式：

```bash
python site-monitor.py
```

## 範例輸出

```text
2026年-05月-28日 12點:14分:24秒 https://api.github.com 正常連線 狀態碼 200
2026年-05月-28日 12點:14分:25秒 https://www.google.com 正常連線 狀態碼 200
2026年-05月-28日 12點:14分:26秒 https://www.youtube.com 正常連線 狀態碼 200
```

將監控結果寫入 log 檔
- 網站異常時寄送 Email 或 Telegram 通知
- 加入設定檔管理監控網址
- 記錄每個網站的回應時間
- 製作簡單的網頁儀表板
