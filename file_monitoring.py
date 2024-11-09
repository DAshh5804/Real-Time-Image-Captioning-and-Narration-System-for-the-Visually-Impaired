import os
import time
import threading
from watchdog.events import FileSystemEventHandler
from tkinter import Tk, Label
from image_caption_and_narration import generate_caption, get_translated_message, speak_gtts

def show_overlay(text):
    root = Tk()
    
    screen_width = root.winfo_screenwidth()
    window_width = 300
    x_position = int((screen_width - window_width) / 2)
    root.geometry(f"{window_width}x100+{x_position}+10")  
    
    root.overrideredirect(1)  
    root.wm_attributes("-topmost", 1)  
    
    Label(root, text=text, font=("Helvetica", 12), wraplength=280).pack(pady=20)

    def close_after_delay():
        root.destroy()

    root.after(8000, close_after_delay)  
    root.mainloop()

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            max_retries = 5
            retry_delay = 1 
            for attempt in range(max_retries):
                try:
                    if os.path.exists(event.src_path):
                        caption = generate_caption(event.src_path)
                        message = get_translated_message(caption)

                        narration_thread = threading.Thread(target=speak_gtts, args=(message,))
                        narration_thread.start()

                        show_overlay(message)
                        break
                    else:
                        raise FileNotFoundError(f"File not found: {event.src_path}")
                except FileNotFoundError as e:
                    print(f"Attempt {attempt + 1}/{max_retries} - Error processing image: {e}")
                    time.sleep(retry_delay)
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break

class FolderHandler(FileSystemEventHandler):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer

    def on_created(self, event):
        if event.is_directory:
            self.observer.schedule(ImageHandler(), event.src_path, recursive=False)
            print(f"Started monitoring new folder: {event.src_path}")
