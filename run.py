import os
import csv

output_folder = "Source/out"
os.makedirs(output_folder, exist_ok=True)

report_folder = "report"
os.makedirs(report_folder, exist_ok=True)

output_file_path = os.path.join(output_folder, "merged_file.csv")

error_reports = []
all_data = []

for file_name in os.listdir("Source"):
    if file_name.endswith('.csv'):
        file_path = os.path.join("Source", file_name)

        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                data = list(reader)

            all_data.extend(row for row in data if "GTIN;SN;BN;XD" not in row)

        except Exception as e:
            error_reports.append(f"Error processing file {file_name}: {str(e)}")

if error_reports:
    report_path = os.path.join(report_folder, "error_report.txt")
    with open(report_path, 'w') as report_file:
        report_file.write("\n".join(error_reports))
else:
    with open(output_file_path, 'w', newline='', encoding='utf-8-sig') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(all_data)

    print(f"Merged all files successfully. The output file is available at: {output_file_path}")

    gtin_from_merged_file = all_data[0][0][:14]
    gtin_folder = os.path.join(output_folder, gtin_from_merged_file)
    os.makedirs(gtin_folder, exist_ok=True)

    gtin_merged_file_path = os.path.join(gtin_folder, "merged_file.csv")
    os.rename(output_file_path, gtin_merged_file_path)

    chunk_size = 90000
    for i in range(0, len(all_data), chunk_size):
        chunk = all_data[i:i + chunk_size]
        chunk.insert(0, ["GTIN;SN;BN;XD"])
        chunk_file_path = os.path.join(gtin_folder, f"chunk_{i // chunk_size + 1}.csv")
        with open(chunk_file_path, 'w', newline='', encoding='utf-8-sig') as chunk_file:
            writer = csv.writer(chunk_file)
            writer.writerows(chunk)

            print(f"Created small file: {chunk_file_path}")

    print(f"Successfully split the output file into smaller files.")