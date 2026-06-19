# Python 自動化作品說明

這個資料夾收錄我在學習 Python、MIS 維運與自動化過程中完成的練習作品。

## 作品一：薪資報表自動產生工具

### 功能
- 讀取 employees.csv 員工資料
- 計算每位員工薪資
- 將正常資料輸出到 salary_report.csv
- 將錯誤資料輸出到 error_report.csv
- 產生 summary_report.txt 統計正常資料、錯誤資料與總薪資

### 使用技術
- Python
- csv.DictReader / csv.DictWriter
- try / except 錯誤處理
- 檔案讀寫
- 資料驗證

### 學習重點
這個作品讓我練習將原始資料轉換成可閱讀的報表，並處理工時或時薪格式錯誤、負數等異常資料。

---

## 作品二：多網站連線監控工具

### 功能
- 讀取 config.example.json 設定網站清單
- 檢查多個網站是否正常連線
- 顯示 HTTP 狀態碼
- 記錄網站回應時間
- 判斷網站是否回應偏慢
- 將檢查結果寫入 log 檔
- 支援 LINE 通知
- 支援參數控制，例如 interval、timeout、slow-threshold

### 使用技術
- Python
- requests
- json
- argparse
- os 環境變數
- datetime
- log 紀錄
- LINE Messaging API

### 學習重點
這個作品讓我練習網站狀態檢查、錯誤處理、設定檔讀取、log 紀錄與 API 通知，和 MIS 日常監控、問題回報流程有關。
