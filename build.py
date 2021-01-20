import openpyxl
import shutil
import sys
import os

# Input validation
if len(sys.argv)<2:
    print("Usage: python build.py <excel file>")
    exit(1)

# Set up build folder
shutil.rmtree("build",ignore_errors=True)
os.makedirs("build")
shutil.copyfile("src/jquery-3.5.1.min.js","build/jquery-3.5.1.min.js")
shutil.copyfile("src/index.html","build/index.html")
shutil.copyfile("src/style.css","build/style.css")
shutil.copyfile("src/script.js","build/script.js")
shutil.copytree("res","build/res")

# Read Excel sheet
wb=openpyxl.load_workbook(sys.argv[1])
for row in wb.active.values:
    for value in row:
        print(value)
