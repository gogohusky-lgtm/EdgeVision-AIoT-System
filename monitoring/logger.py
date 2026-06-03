import os
import csv

LOG_DIR = "monitoring/logs"

LOG_FILE = os.path.join(
    LOG_DIR,
    "inference_log.csv"
)


def initialize_log():

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            mode="w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "image",
                "label",
                "latency_ms"
            ])

        print(
            f"Created log file: {LOG_FILE}"
        )


def log_inference(
    image_path,
    result
):

    with open(
        LOG_FILE,
        mode="a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            result.get(
                "timestamp",
                ""
            ),

            image_path,

            result.get(
                "label",
                ""
            ),

            result.get(
                "latency_ms",
                0
            )
        ])

    print(
        f"Logged result to: {LOG_FILE}"
    )