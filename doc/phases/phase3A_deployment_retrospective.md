# Phase3A Retrospective — From Simulation to Real Edge Deployment

## Overview

Phase3A 的目標並非開發新的 AI 功能，而是驗證 EdgeVision-AIoT-System 是否能夠真正部署於 Raspberry Pi 5 實體硬體上運行。

在此前的開發階段：

* Phase0 完成單體 AI 推論程式
* Phase1 完成 Containerized AIoT Architecture
* Phase2 完成 Runtime Hardening 與 Queue-Based Architecture

然而：

> 「PC 模擬成功」並不等於「實機部署成功」。

當系統首次部署到 Raspberry Pi 5 時，暴露出大量在 PC 開發環境中從未出現過的整合問題。

---

## Key Challenges Encountered

### 1. TensorFlow → TFLite Runtime Migration

PC 開發環境使用完整 TensorFlow。

實際部署至 Raspberry Pi 5 時發現：

* TensorFlow 體積過大
* 安裝時間過長
* 資源消耗不符合 Edge Device 特性

因此改採：

```python
import tflite_runtime.interpreter as tflite
```

並重新調整 Docker Image 與 Requirements。

---

### 2. MQTT Service Conflict

部署後 MQTT 無法正常連線：

```text
Connection failed: rc=5
Unexpected disconnect
```

初步看似 Broker 問題。

實際追查後發現：

Raspberry Pi 過去曾部署 ESP32 MQTT TLS 專案。

系統中殘留：

```text
/etc/mosquitto/conf.d/TLS_Enable.conf
```

其中：

```text
require_certificate true
```

造成所有未攜帶憑證的 Client 被 Broker 拒絕。

最終移除舊有 TLS 配置後恢復正常。

---

### 3. Linux Service Layer Investigation

本次部署第一次需要深入檢查：

* systemctl
* journalctl
* ss
* Mosquitto Service

例如：

```bash
sudo systemctl status mosquitto
sudo ss -tlnp
```

這些工具在 PC 模擬環境幾乎不曾使用。

實際部署時則成為定位問題的核心手段。

---

### 4. Docker Path Drift

Phase2 Runtime Hardening 完成後：

```text
ai_engine/
```

已重構為：

```text
runtime/
```

但 Docker Compose 與 Dockerfile 仍保留舊路徑。

導致：

```text
unable to prepare context
lstat ... no such file or directory
```

問題本質不是 Docker 故障。

而是：

> 專案架構演進後，部署配置未同步更新。

---

### 5. Docker Volume Mapping Failure

系統運行正常。

Container 內可看到：

```text
/app/monitoring/logs/inference_log.csv
```

但 Host 完全找不到 CSV。

經 docker exec 與 docker inspect 排查後確認：

應用程式實際寫入：

```text
/app/monitoring/logs
```

而 Docker 掛載的是：

```text
/app/src/monitoring/logs
```

造成資料被寫入 Container 私有檔案系統。

此問題凸顯：

> Docker 掛載成功，不代表應用程式真的寫入掛載位置。

---

### 6. Runtime Validation on Real Hardware

完成所有修正後進行壓力測試：

測試條件：

* 322 張圖片一次性投入
* Producer / Consumer Queue 架構
* MQTT Telemetry
* CSV Logging
* Dashboard Update

測試結果：

| Item             | Result |
| ---------------- | ------ |
| Images Input     | 322    |
| Images Processed | 322    |
| CSV Records      | 322    |
| Dropped Frames   | 0      |
| Deadlock         | 0      |
| Crash            | 0      |

系統成功完成全流程處理。

---

## Most Important Lesson

本階段最大的收穫並非 Docker、MQTT 或 Raspberry Pi 本身。

而是理解：

> 真正的部署問題，大多不來自演算法，而來自系統整合。

AI Model 在 PC 上成功推論只是起點。

當系統進入真實硬體環境後，還需要面對：

* 作業系統服務
* 網路中介軟體
* 容器化部署
* 檔案系統映射
* 依賴套件管理
* 環境配置殘留

這些才是 Edge AI 系統能否真正落地運行的關鍵。

---

## Phase3A Outcome

Phase3A 完成後，EdgeVision-AIoT-System 已具備：

* Raspberry Pi 5 Native Deployment
* TFLite Edge Inference
* MQTT Communication
* Docker Compose Orchestration
* Runtime Queue Architecture
* Persistent Telemetry Logging
* Dashboard Visualization

系統正式從「PC 模擬專案」提升為「可於實體邊緣設備部署運行的 AIoT 系統」。

這也是專案從 Software Prototype 邁向 Edge System Engineering 的重要里程碑。
題。