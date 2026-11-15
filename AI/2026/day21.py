import os, shutil

#list all files in a folder
files= os.listdir("/Users/Dell/Desktop/Machine Learning 2")
if os.path.exists("day21.py"):
    print("File Found")

#Create a Folder (no error if it already exists)
os.makedirs("AI/2026", exist_ok=True)

#copy a file
shutil.copy("day21.py", "AI/2026/day21.py")

#Move a file
shutil.move("day21.py", "AI/2026")
print(files)