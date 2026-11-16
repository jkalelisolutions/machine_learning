import os,shutil
from datetime import datetime

source = r"C:\Users\DELL\Documents"
archive = r"D:\Users\Dell"

today= datetime.now().strftime('%y-%m') #e.g 2026-11
archive_month= os.path.join(archive,today)
os.makedirs(archive_month, exist_ok=True)

categories = {
    "Images": [".jpeg", ".png", ".gif", ".jpg"],
    "Documents": [".pdf", ".docx", ".xlsx"],
    "Email": [".eml",".txt"],
    "other": []
}

#Creating a destination path for every file
Destination= {
    "Images":"Evidence",
    "Documents": "Contracts",
    "Email": "Correspondence",
    "other":"Other"
}

#List all files in a folder
for file in os.listdir(source):
    source_path= os.path.join(source,file)
    category="other"

    if not os.path.isfile(source_path):
        continue

    #Create a pathway of where the categories(items) will be placed
    ext= os.path.splitext(file)[1].lower()
    for name, extension in categories.items():
        if ext in extension:
            category = Destination[name]

    destination= os.path.join(source, category)
    os.makedirs(destination, exist_ok=True)
    shutil.move(source_path, os.path.join(destination,file))

        
    print(f"Moved {file} to {destination}")
moved = 0
for f in os.listdir(source):
    if f.endswith(".txt"):
        shutil.copy(os.path.join(source,f), archive_month)
        moved +=1
print(f"Backed up {moved} data to {archive_month}")