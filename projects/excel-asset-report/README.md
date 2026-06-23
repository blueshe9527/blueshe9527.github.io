# Python Excel 資產清冊自動備份與維修報表工具

## 功能
- 讀取 company_assets.xlsx 資產清冊
- 執行前自動建立 backups 資料夾
- 依照日期時間備份原始 Excel 檔
- 篩選狀態為「維修中」的設備
- 輸出 repair_assets.xlsx 維修報表
- 統計維修中設備數量
- 設定報表欄寬與列高
- 顯示警告訊息，提醒追蹤維修進度

## 使用技術
- Python
- openpyxl
- shutil
- os
- datetime
- Excel 資料處理
- 檔案備份

## 學習重點
這個作品模擬 MIS 維運中的 IT 資產管理流程，透過 Python 自動備份原始資料，並將維修中設備整理成報表，減少人工篩選與整理時間。
