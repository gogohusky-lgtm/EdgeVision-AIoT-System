import os
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

        filepath = self.frame_queue.get()
        if not os.path.exists(filepath):

            print(f"[WARNING] Missing file:"f" {filepath}")
            self.enqueued_files.discard(filepath)  # 從 set 中移除（如果存在）
            self.frame_queue.task_done()

            return
        
        print(f"Queue size: "f"{self.frame_queue.qsize()}")
        print(
            f"\nProcessing: {filepath}"
        )

        try:
            result = (self.classifier.infer_image_path(filepath))
        except Exception as e:
            print(f"[ERROR] Failed ：" f" {filepath}")
            print(e)
            self.enqueued_files.discard(filepath)  # 從 set 中移除（如果存在）
            self.frame_queue.task_done()
            return
        print(
            f"Prediction: "
            f"{result['label']} "
            f"| Latency: "
            f"{result['latency_ms']:.2f} ms"
        )

        self.log_callback(
            filepath,
            result
        )

        self.router.handle_prediction(
            result["label"]
        )

        self.mqtt_pub.publish_prediction(
            result
        )

        try:
            os.remove(filepath)
            print(f"Removed: {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to remove file: {filepath}")
            print(e)

        # 通知 Producer：移除已處理的路徑
        if filepath in self.enqueued_files:
            self.enqueued_files.discard(filepath)

        self.frame_queue.task_done()

    def run(self):

        while self.running or not self.frame_queue.empty():

            if self.frame_queue.empty():

                time.sleep(0.1)

                continue

            self.process_one_frame()

    def stop(self):

        self.running = False