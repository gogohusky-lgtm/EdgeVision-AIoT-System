# Phase 2 — Runtime Hardening Journey

## Objective
將 Phase 1 的貨櫃化 AIoT 管線升級為具備高可用性的生產級 Runtime 守護行程（Daemon）。專注於邊緣端執行期工程（Runtime Engineering），優化系統在高負載下的行為，消除並行異常，確保長時間運作下的資料完整性與系統可用性。

---

# System Architecture & Components
系統採用具備阻斷背壓（Blocking Backpressure）機制的並行架構：
`輸入源 ➔ Producer 執行緒 ➔ 有界佇列 (容量:50) ➔ Consumer 執行緒 ➔ 推論與 MQTT`

* **Producer Thread**：非同步掃描並攝取影像，利用記憶體內 `set()` 邏輯過濾重複排隊，並在佇列飽和時執行阻斷背壓策略。
* **Bounded Queue**：作為執行緒安全的緩衝層，限制極端流量下的記憶體佔用。
* **Consumer Thread**：非同步讀取佇列並執行 TFLite 推論，導入防禦性驗證與隔離異常處理，防止核心崩潰。
* **Resilience Telemetry**：負責 MQTT 自動斷線重連、發送系統心跳（Heartbeat），並輸出 CSV 與視覺化圖表。

---

# Key Engineering Challenges & Solutions

### 1. 瞬時流量阻塞 (Burst Traffic)
* **問題**：大量圖片湧入時，單執行緒同步循環會完全阻塞影像攝取流程。
* **解法**：重構為**生產品-佇列-消費者 (Producer-Queue-Consumer)** 非同步架構，將高頻 I/O 與高耗能推論完全解耦。

### 2. 並行競爭與執行緒崩潰 (Race Condition)
* **問題**：在 133 張圖片壓力測試下，出現 `cv2.imread() failed` 導致 Consumer 崩潰。
* **原因**：Producer 掃描資料夾與排隊的速度，快於 Consumer 推論後刪除檔案的速度，導致同路徑被重複排隊，進而讀取到已刪除的無效檔案。
* **解法**：在 Consumer 讀檔前加入 `os.path.exists()` 防禦性檢查，並在 Producer 內置 `set()` 追蹤在途檔案，完全消除重複排隊。

### 3. 佇列飽和導致隱性丟幀 (Silent Data Loss)
* **問題**：322 張圖片測試中丟失 7 幀，僅成功處理 315 張。
* **原因**：原架構使用非阻塞的 `put_nowait()`。當佇列達到上限（50）時，後續影像觸發異常並被隱性捨棄。
* **解法**：將入隊機制改為阻塞式 `.put()` 建立**阻斷背壓機制**，迫使 Producer 速度匹配 Consumer 的處理能力。

### 4. 停機時在途任務遭截斷 (Shutdown Truncation)
* **問題**：Ctrl+C 關閉系統時，工作區殘留未處理完成的檔案。
* **原因**：停機邏輯僅輪詢佇列是否為空（`FRAME_QUEUE.empty()`），一旦佇列清空便立即終止 Consumer，截斷了正在推論中的在途任務。
* **解法**：引入 `FRAME_QUEUE.join()` 同步屏障，強制主執行緒等待所有 Consumer 宣告 `task_done()` 後才執行銷毀，實現無損安全排空（Queue Draining）。

---

# Key Engineering Lessons

1.  **正確性高於並行度 (Correctness > Concurrency)**：引入多執行緒雖提升了回應速度，但也帶來了共享狀態的風險。在邊緣端 Runtime 中，系統確定性與運作時間（Uptime）永遠高於盲目的並行速度。
2.  **佇列設計即 Runtime 策略**：佇列不只是資料結構，它決定了系統面對過載時的背壓行為（阻斷或捨棄機制），必須依應用情境對延遲與丟幀的容忍度進行設計。
3.  **魯棒性源於壓力測試**：常規測試常會掩蓋架構缺陷。多執行緒同步、背壓邊界與停機邏輯的隱藏假設，只有在極端負載飽和時才會現形。

---

# Outcome
* 實現 100% 資料完整性，通過 322 張爆發流量測試，零丟幀、零執行緒崩潰。
* 成功建立阻斷背壓與安全停機排空機制，工作區殘留檔案降至 0。
* 具備自動網路修復與遙測心跳能力。

專案成功從 **「分散式 AIoT 平台原型展示」** 演進為 **「高韌性、生產級邊緣 AIoT 系統架構」**。