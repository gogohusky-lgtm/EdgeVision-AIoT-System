# Problem
在 PC 開發階段，系統依賴完整的 TensorFlow 框架進行模型載入與驗證，但將此架構直接移至邊緣端裝置（Raspberry Pi 5）時，遭遇完整的 TensorFlow 封包過於龐大、安裝耗時且非必要地消耗過多記憶體與硬碟空間的問題。


# Root Cause
完整的 TensorFlow 框架包含大量模型訓練與通用計算組件，而在邊緣端節點上，系統僅需要進行輕量化模型推論（Inference-only），部署完整框架不符合邊緣運算（Edge Computing）資源精簡的原則。
相較於完整 TensorFlow：

- 更小的 Container Image
- 更快的 Build Time
- 更低記憶體占用
- 更符合 Edge Inference-only Workload

因此選擇 tflite-runtime 作為推論後端。

# Solution
推論引擎輕量化：將推論核心代碼從 import tensorflow as tf 調整為僅導入專為邊緣端設計的 import tflite_runtime.interpreter as tflite。

所以PC原來的:
import tensorflow as tf

self.interpreter = tf.lite.Interpreter(model_path=model_path)

到RPI5要改成：
import tflite_runtime.interpreter as tflite

self.interpreter = tflite.Interpreter(model_path=model_path)


依賴環境重構：更新 requirements_ai.txt，移除完整 TensorFlow 依賴，精準鎖定邊緣端運行所需的輕量化版本組件：

Plaintext
numpy==1.26.4
opencv-python-headless==4.8.1.78
tflite-runtime==2.14.0
paho-mqtt==2.1.0
Result
成功在 Raspberry Pi 5 運行的 Docker 容器內，以極低的資源開銷正確載入 TFLite 推論引擎，完全免除完整 TensorFlow 框架帶來的非必要開銷。

# Lessons Learned
在邊緣端部署 AI 模型時，環境與架構的精簡度直接影響系統的敏捷性。轉用 tflite-runtime 不僅縮短了容器鏡像（Container Image）的構建時間，也為受限的內嵌式硬體保留了更多寶貴的記憶體運算空間。
