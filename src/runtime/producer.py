import os
import threading
import time

class FrameProducer(threading.Thread):

    def __init__(
        self,
        frame_dir,
        frame_queue,
        polling_interval=1
    ):

        super().__init__()

        self.frame_dir = frame_dir
        self.frame_queue = frame_queue
        self.polling_interval = polling_interval

        self.running = True
        
        self.queued_files = set()

    def enqueue_frames(self):

        files = os.listdir(self.frame_dir)

        jpg_files = [f for f in files if f.endswith(".jpg")]

        for file in jpg_files:

            filepath = os.path.join(self.frame_dir,file)
            
            # 檢查是否已經 enqueue 過
            if filepath in self.queued_files:
                continue  # 跳過，避免重複放入 queue

            try:

                self.frame_queue.put(
                    filepath
                )
                # 成功放入 queue 後，記錄到 set
                self.queued_files.add(filepath)
            except:
                print("[---Queue Full---]")
                pass

    def run(self):

        while self.running:

            self.enqueue_frames()

            time.sleep(
                self.polling_interval
            )

    def stop(self):

        self.running = False