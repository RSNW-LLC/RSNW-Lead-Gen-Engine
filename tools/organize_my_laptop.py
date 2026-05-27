import os
import shutil

# The folder you want to clean up (Change this to your Downloads path if needed)
TARGET_FOLDER = os.path.expanduser("~/Downloads")

# Define where different file types should go
DESTINATIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".doc", ".pptx"],
    "Data_and_Sheets": [".csv", ".xlsx", ".json", ".sql", ".db"],
    "Scripts_and_Code": [".py", ".sh", ".js", ".html", ".css"],
    "Apps_and_Zips": [".zip", ".tar.gz", ".deb", ".exe", ".msi"]
}

def organize():
    print(f"[*] Cleaning up: {TARGET_FOLDER}")
    
    if not os.path.exists(TARGET_FOLDER):
        print("[X] Folder not found!")
        return

    for filename in os.listdir(TARGET_FOLDER):
        filepath = os.path.join(TARGET_FOLDER, filename)
        
        # Skip if it's a folder
        if os.path.isdir(filepath):
            continue
            
        # Get file extension
        file_ext = os.path.splitext(filename)[1].lower()
        
        moved = False
        for folder, extensions in DESTINATIONS.items():
            if file_ext in extensions:
                dest_dir = os.path.join(TARGET_FOLDER, folder)
                
                # Create folder if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                # Move the file
                shutil.move(filepath, os.path.join(dest_dir, filename))
                print(f" [->] Moved {filename} to {folder}/")
                moved = True
                break
        
    print("[✓] Cleanup complete. Your folder is now 'neat and neat'!")

if __name__ == "__main__":
    organize()
