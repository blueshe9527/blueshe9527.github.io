import shutil
import os
from datetime import datetime
source_file = "company_assets.xlsx"
backup_folder = "backups"
os.makedirs(backup_folder, exist_ok=True)
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_filename = f"company_assets_{current_time}.xlsx"
print(backup_filename)
backup_path = os.path.join(backup_folder, backup_filename)
shutil.copy2(source_file, backup_path)
print(f"已備份成功:{backup_path}")
from openpyxl import load_workbook as lw , Workbook as wb
source_workbook = lw(source_file)
source_sheet = source_workbook.active

repair_workbook = wb()
repair_sheet = repair_workbook.active
repair_sheet.title = "維修報表"
repair_sheet.append(["設備編號", "部門", "人員名稱", "機台狀態", "維修日期"])
repair_count = 0
for row in source_sheet.iter_rows(min_row=2, values_only=True):
    equipment_id = row[0]
    department = row[1]
    user = row[2]
    status = row[5]
    repair_date = row[7]
    if status == "維修中":
        repair_count += 1
        repair_sheet.append([equipment_id, department, user, status, repair_date])
        print(f"設備編號 {equipment_id} 維修日期 {repair_date}")
repair_sheet.column_dimensions["A"].width=15
repair_sheet.column_dimensions["B"].width=15
repair_sheet.column_dimensions["C"].width=15
repair_sheet.column_dimensions["D"].width=15
repair_sheet.column_dimensions["E"].width=15

repair_sheet.row_dimensions[1].height=20
repair_sheet.row_dimensions[2].height=20
repair_sheet.row_dimensions[3].height=20
repair_sheet.row_dimensions[4].height=20
repair_sheet.row_dimensions[5].height=20
repair_workbook.save("repair_assets.xlsx")
print("已建立 repair_assets.xlsx")
print(f"維修中 {repair_count} 台 ")
if repair_count > 0:
    print(f"警告：目前有 {repair_count} 台設備維修中，請追蹤處理進度")









