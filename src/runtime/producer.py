import os

class FrameProducer:

    def __init__(self, frame_dir, frame_queue):

        self.frame_dir = frame_dir
        self.frame_queue = frame_queue

    def enqueue_frames(self):

        files = os.listdir(self.frame_dir)

        jpg_files = [
            f for f in files
            if f.endswith(".jpg")
        ]

        for file in jpg_files:

            filepath = os.path.join(
                self.frame_dir,
                file
            )

            if not self.frame_queue.full():

                self.frame_queue.put(
                    filepath
                )

                print(
                    f"[QUEUE] Added: {filepath}"
                )