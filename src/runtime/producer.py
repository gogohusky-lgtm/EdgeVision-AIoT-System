from pathlib import Path
import threading
import time

class FrameProducer(threading.Thread):

    def __init__(self, frame_dir, frame_queue, polling_interval=1):
        super().__init__()
        self.frame_dir = Path(frame_dir)
        self.frame_queue = frame_queue
        self.polling_interval = polling_interval
        self.running = True
        self.queued_files = set()

    def enqueue_frames(self):
        jpg_files = [f for f in self.frame_dir.iterdir() if f.suffix == ".jpg"]

        for filepath in jpg_files:
            filepath_str = str(filepath)
            if filepath_str in self.queued_files:
                continue  # 避免重複放入 queue

            try:
                self.frame_queue.put(filepath_str)
                self.queued_files.add(filepath_str)
            except:
                print("[---Queue Full---]")
                pass

    def run(self):
        while self.running:
            self.enqueue_frames()
            time.sleep(self.polling_interval)

    def stop(self):
        self.running = False
