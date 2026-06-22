# Problem: 

Original Runtime Pipeline Was Tightly Coupled

## 原始架構：

Camera Input
    ↓
Inference
    ↓
Logging
    ↓
Action
    ↓
MQTT
    ↓
File deletion

## 限制：所有工作都在同一條執行流程：即讀檔、推論、輸出順序執行。因此：Frame ingestion 與 inference 完全耦合，大量圖片湧入時容易形成阻塞，無法緩衝 Burst Traffic，不利於後續多 Camera 或多 Source 擴充

# Solution

Introduce Producer-Queue-Consumer Architecture

主要設計變更為：
- 將 Frame Acquisition 與 Inference Processing 解耦（Decouple）。
- Queue 作為 Buffer Layer，避免瞬時流量直接衝擊推論流程：

Producer → Frame Queue (Buffer) → Consumer


架構變為：

Camera Input
      ↓
Producer
      ↓
Frame Queue
      ↓
Consumer
      ↓
Inference
      ↓
Action
      ↓
MQTT
      ↓
File deletion


# Result

成功完成：

- Queue-based Runtime
- Buffered Frame Processing
- Burst Traffic Handling

實測：

Single image, 20 images batch, 133 images batch 皆可正常排隊處理。

# Lessons Learned

Queue 不只是資料結構。在 Runtime Architecture 中：
Queue = Decoupling Mechanism

主要目的不是加速，而是：Improve System Robustness