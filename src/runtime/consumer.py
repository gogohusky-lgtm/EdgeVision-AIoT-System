import os

class FrameConsumer:

    def __init__(
        self,
        frame_queue,
        classifier,
        router,
        mqtt_pub,
        log_callback
    ):

        self.frame_queue = frame_queue
        self.classifier = classifier
        self.router = router
        self.mqtt_pub = mqtt_pub
        self.log_callback = log_callback

    def process_queue(self):

        while not self.frame_queue.empty():

            filepath = self.frame_queue.get()

            print(
                f"\nProcessing: {filepath}"
            )

            result = (
                self.classifier
                .infer_image_path(filepath)
            )

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