import csv
with open("employees.csv", "r", encoding="utf-8") as input_file:
    reader = csv.DictReader(input_file)
    salary_fieldnames = reader.fieldnames + ["salary"]
    error_fieldnames = reader.fieldnames + ["error"]

    with open("salary_report.csv", "w", encoding="utf-8", newline="") as salary_file, \
         open("error_report.csv", "w", encoding="utf-8", newline="") as error_file:
         salary_writer = csv.DictWriter(salary_file, fieldnames=salary_fieldnames)
         error_writer = csv.DictWriter(error_file, fieldnames=error_fieldnames)
         salary_writer.writeheader()
         error_writer.writeheader()
         normal_count = 0
         error_count = 0
         total_salary = 0
         for row in reader:
             try:
                name = row["name"]
                hours = int(row["hours"])
                hourly_wage = int(row["hourly_wage"])
                if hours < 0 :
                    raise ValueError ("工時不能小於0")
                if hourly_wage < 0 :
                    raise ValueError ("時薪不能小於0")

                salary = hours * hourly_wage
                row["salary"] = salary
                salary_writer.writerow(row)
                normal_count += 1
                total_salary += salary
                print(f"姓名 {name} 工時 {hours} 小時 時薪 {hourly_wage} 元 薪資 {salary} 元")

             except ValueError as error:
                row["error"] = str(error)
                error_writer.writerow(row)
                error_count += 1
                print(f"錯誤資料{row}")
                print(f"錯誤原因{error}")
         with open("summary_report.txt", "w", encoding="utf-8") as summary_file:
             summary_file.write("處理完成\n")
             summary_file.write(f"正常資料筆數: {normal_count}\n")
             summary_file.write(f"錯誤資料筆數: {error_count}\n")
             summary_file.write(f"總薪資: {total_salary}\n")

















