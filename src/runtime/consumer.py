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
        log_callback
    ):

        super().__init__()

        self.frame_queue = frame_queue
        self.classifier = classifier
        self.router = router
        self.mqtt_pub = mqtt_pub
        self.log_callback = log_callback

        self.running = True

    def process_one_frame(self):

        filepath = self.frame_queue.get()
        if not os.path.exists(filepath):

            print(f"[WARNING] Missing file:"f" {filepath}")
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

        os.remove(filepath)

        print(
            f"Removed: {filepath}"
        )

        self.frame_queue.task_done()

    def run(self):

        while self.running:

            if self.frame_queue.empty():

                time.sleep(0.1)

                continue

            self.process_one_frame()

    def stop(self):

        self.running = False