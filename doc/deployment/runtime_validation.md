# Phase 1 運作狀態驗證與確定性指標 (Runtime Verification)

## 驗證目的
本文件旨在建立一套標準的測試方法，用以驗證單機多容器環境下，AI推論節點、MQTT Broker 與監控儀表板節點之間的數據閉環（Data Loop）是否運作正常。

## 步驟一：基礎設施狀態確認 (Orchestration Check)

執行以下指令確認所有微服務容器的運行狀態：

```bash
docker compose ps
```

預期輸出指標：

mqtt_broker   - 狀態：Up - 埠口：0.0.0.0:1883->1883/tcp

ai_node       - 狀態：Up

dashboard_node - 狀態：Up

## 步驟二：日誌流與數據通訊驗證 (Dataflow & Log Verification)

透過觀察邊緣 AI 節點的容器輸出，確定圖片消費與通訊鏈路的狀態：


docker compose logs -f ai_node

關鍵正確性特徵 (Correctness Patterns)：

1. 影像消耗確認：日誌需週期性顯示 Removed: camera_input/captured_frames/frame_X.jpg，證明 Folder Polling 與記憶體釋放正常。

2. 硬體模擬層確認：顯示 [SIM GPIO] cats 或 dogs，代表在無實體 GPIO 環境下，硬體抽象層成功切換至開發模擬模式（Development Mode）。

3. 通訊發送確認：日誌輸出 Published MQTT: {"timestamp": ..., "label": ..., "latency_ms": ...}，確認 JSON 序列化與 Mosquitto 網路連線正常。

## 步驟三：持久化層與可視化驗證 (Persistence & Visualization)

1. CSV 日誌查核：
檢查主機端相對路徑 ./monitoring/logs/inference_log.csv。預期確認：

- 標頭檔欄位為：timestamp, image, label, latency_ms。

- 新增的推論數據正常追加（Append）且未發生編碼衝突。

2. 前端監控看板查核：

確認系統根目錄下週期性更新 dashboard_latest.png 圖片，其趨勢圖需能正確動態繪製最新 30 筆推論延遲波動（Latency Curve），證明 Matplotlib 異步渲染執行緒未發生死鎖（Deadlock）。

