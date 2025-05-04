import os
import subprocess
import time
import datetime
import shutil
import platform

RETENTION_PERIOD_WEEKS = 4
SCRIPT_NAME = "media_manager.py"
README_NAME = "README.md"
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), SCRIPT_NAME)
README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), README_NAME)

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=PHOTO_FOLDER)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command '{' '.join(command)}': {stderr.decode()}")
        return False
    return True

def commit_and_push():
    if run_command(["git", "add", "."]):
        if run_command(["git", "commit", "-m", f"Automated commit - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]):
            if run_command(["git", "push", "origin", "main"]):
                print("Successfully committed and pushed changes to GitHub.")
                return True
    return False

def delete_old_folders():
    cutoff_date = datetime.datetime.now() - datetime.timedelta(weeks=RETENTION_PERIOD_WEEKS)
    for item in os.listdir(PHOTO_FOLDER):
        item_path = os.path.join(PHOTO_FOLDER, item)
        if os.path.isdir(item_path) and item != SCRIPT_NAME:  # Exclude the script itself
            try:
                # Get the modification time of the folder
                modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
                if modified_time < cutoff_date:
                    print(f"Deleting old folder: {item_path}")
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"Error processing folder {item_path}: {e}")
        elif os.path.isfile(item_path) and item == README_NAME:
            print(f"Keeping {README_NAME}") # Explicitly mention that README is kept

if __name__ == "__main__":
    system = platform.system()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    PHOTO_FOLDER = os.path.join(desktop_path, "CKR_ARCHIVE")

    # Create the archive folder if it doesn't exist
    if not os.path.exists(PHOTO_FOLDER):
        try:
            os.makedirs(PHOTO_FOLDER)
            print(f"Created folder: {PHOTO_FOLDER}")
        except OSError as e:
            print(f"Error creating folder {PHOTO_FOLDER}: {e}")
            exit()

    commit_and_push()
    delete_old_folders()

    print("Script execution completed.")
