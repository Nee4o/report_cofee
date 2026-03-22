import argparse
import csv
import sys
from statistics import median
from collections import defaultdict
from tabulate import tabulate


def get_median_coffee_report(all_data):
    student_expenses = defaultdict(list)
    for row in all_data:
        name = row.get("student")
        spent_raw = row.get("coffee_spent")

        if name and spent_raw:
            try:
                student_expenses[name].append(float(spent_raw))
            except ValueError:
                continue

    report_data = []
    for student, expenses in student_expenses.items():
        m_val = median(expenses)
        report_data.append([student, m_val])
    report_data.sort(key=lambda x: x[1], reverse=True)
    return report_data, ["student", "median_coffee"]


REPORTS = {"median-coffee": get_median_coffee_report}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    all_rows = []
    for file_path in args.files:
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_rows.append(row)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден")
            return

    if args.report in REPORTS:
        table_data, headers = REPORTS[args.report](all_rows)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
