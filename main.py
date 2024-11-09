import os
import time
from watchdog.observers import Observer
from file_monitoring import FolderHandler, ImageHandler

main_folder_to_watch = r"C:\path\to\your\images\directory"

observer = Observer()
observer.schedule(FolderHandler(observer), main_folder_to_watch, recursive=False)

# Start monitoring any existing subfolders
for subfolder in os.listdir(main_folder_to_watch):
    subfolder_path = os.path.join(main_folder_to_watch, subfolder)
    if os.path.isdir(subfolder_path):
        observer.schedule(ImageHandler(), subfolder_path, recursive=False)
        print(f"Started monitoring existing folder: {subfolder_path}")

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
