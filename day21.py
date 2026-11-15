import os, shutil

#list all files in a folder
#files= os.listdir("/Users/Dell/Desktop/Machine Learning 2")
#if os.path.exists("day21.py"):
#    print("File Found")

#Create a Folder (no error if it already exists)
#os.makedirs("AI/2026", exist_ok=True)

#copy a file
#shutil.copy("day21.py", "AI/2026/day21.py")

#Move a file
#shutil.move("day21.py", "AI/2026")
#print(files)

SOURCE = r"C:\Users\DELL\Downloads"

CATEGORIES= {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Scripts": [".py", ".js", ".html"],
    "other":[]
}

for filename in os.listdir(SOURCE):
    ext = os.path.splitext(filename)[1].lower()
    dest_folder= "other"
    break
for category, extenstions in CATEGORIES.items():
    if extenstions is not None:
        dest_folder = category
        break




dest= os.path.join(SOURCE, dest_folder)
os.makedirs(dest, exist_ok=True)
shutil.move(os.path.join(SOURCE,filename), os.path.join(dest,filename))

print(f"Moved {filename} -> {dest_folder}/")
