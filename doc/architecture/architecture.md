EdgeVision-AIoT-System/
│
├── docker-compose.yml
│
├── deployment/
│     │
│     ├─── ai_engine/
│     │        ├── Dockerfile_ai_node
│     │        ├── models/pet_classifier_fp16.tflite 
│     │        └── requirements_ai_node.txt 
│     │ 
│     ├─── dashboard_node/
│     │        ├── Dockerfile_dashboard_node
│     │        ├── requirement_dashboard_node.py 
│     │        └── dashboard_subscriber.py
│     │ 
│     └─── mosquitto/
│              └── mosquitto.conf
│
├── docs/
│
├── architecture/
│
└── src/
      │
      ├── inference_core.py
      │
      ├── action_layer/
      │     ├── gpio_controller.py
      │     └── action_router.py
      │
      ├── camera_input/
      │     ├── captured_frames/      
      │     └── webcam_capture.py
      │
      ├── monitoring/
      │     ├── dashboard/dashboard_latest.png   
      │     ├── logs/inference_log.csv 
      │     └── logger.py
      │
      ├── communication/
      │     ├── mqtt_subscriber.py 
      │     └── mqtt_publisher.py
      │      
      └── runtime/
            ├── frame_to_inference.py
            ├── frame_queue.py
            ├── producer.py
            └── consumer.py



EdgeVision-AIoT-System/
│
├── docker-compose.yml
│
├── deployment/
│     │
│     ├─── ai_node/
│     │        ├── Dockerfile
│     │        └── requirements.txt 
│     │ 
│     ├─── dashboard_node/
│     │        ├── Dockerfile
│     │        └── requirements.txt 
│     │ 
│     └─── mosquitto/
│              └── mosquitto.conf
│
├── docs/
│
├── architecture/
│
└── src/
      │
      ├── inference_core.py
      │
      ├── models/
      │     └── pet_classifier_fp16.tflite
      │
      ├── dashboard/
      │     └── dashboard_subscriber.py
      │
      ├── action_layer/
      │     ├── gpio_controller.py
      │     └── action_router.py
      │
      ├── camera_input/
      │     ├── captured_frames/      
      │     └── webcam_capture.py
      │
      ├── monitoring/
      │     ├── dashboard/
      │     │    └── dashboard_latest.png   
      │     ├── logs/
      │     │    └── inference_log.csv
      │     └── logger.py
      │
      ├── communication/
      │     ├── mqtt_subscriber.py 
      │     └── mqtt_publisher.py
      │      
      └── runtime/
            ├── frame_to_inference.py
            ├── frame_queue.py
            ├── producer.py
            └── consumer.py