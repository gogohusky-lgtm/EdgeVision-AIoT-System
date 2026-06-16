from pathlib import Path
import time
import threading

class FrameConsumer(threading.Thread):

    def __init__(
        self,
        frame_queue,
        classifier,
        router,
        mqtt_pub,
        log_callback,
        enqueued_files   # 新增：共享的 set
    ):
        super().__init__()
        self.frame_queue = frame_queue
        self.classifier = classifier
        self.router = router
        self.mqtt_pub = mqtt_pub
        self.log_callback = log_callback
        self.enqueued_files = enqueued_files  # 保存引用
        self.running = True

    def process_one_frame(self):
        filepath = Path(self.frame_queue.get())

        if not filepath.exists():
            print(f"[WARNING] Missing file: {filepath}")
            self.enqueued_files.discard(str(filepath))
            self.frame_queue.task_done()
            return

        print(f"Queue size: {self.frame_queue.qsize()}")
        print(f"\nProcessing: {filepath}")

        try:
            result = self.classifier.infer_image_path(str(filepath))
        except Exception as e:
            print(f"[ERROR] Failed: {filepath}")
            print(e)
            self.enqueued_files.discard(str(filepath))
            self.frame_queue.task_done()
            return

        print(f"Prediction: {result['label']} | Latency: {result['latency_ms']:.2f} ms")

        self.log_callback(str(filepath), result)
        self.router.handle_prediction(result["label"])
        self.mqtt_pub.publish_prediction(result)

        try:
            filepath.unlink()
            print(f"Removed: {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to remove file: {filepath}")
            print(e)

        self.enqueued_files.discard(str(filepath))
        self.frame_queue.task_done()

    def run(self):
        while self.running or not self.frame_queue.empty():
            if self.frame_queue.empty():
                time.sleep(0.1)
                continue
            self.process_one_frame()

    def stop(self):
        self.running = False
