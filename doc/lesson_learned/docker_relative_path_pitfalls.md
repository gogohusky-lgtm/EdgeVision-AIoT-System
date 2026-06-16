# Problem
在完成 Runtime Hardening（Phase2）後，專案目錄結構經歷重構，
frame_to_inference.py 由原本的 ai_engine/ 搬移至 runtime/。

部署至 Raspberry Pi 5 並執行：docker-compose build 時出現：

lstat .../src/runtime/Dockerfile:
no such file or directory

導致容器無法建構。

# Root Cause
專案程式碼結構雖已演進，但 Docker Compose 設定檔與 Dockerfile 內部的相對路徑（如 COPY 指令範圍及 context 邊界）仍指向舊版目錄，導致 Docker 守護行程在指定的 Build Context 中找不到對應的檔案。

# Solution
重新校準 Docker Compose 構建上下文（Build Context），將其定錨於專案根目錄，並精確定義 Dockerfile 與磁碟卷（Volumes）的映射關係：

```
YAML
build:
  context: .
  dockerfile: ai_node/Dockerfile
volumes:
  - ./src:/app/src
```

確保 Host 端的 EdgeVision-AIoT-System/src 正確且安全地對齊 Container 內的 /app/src 目錄。

# Result
Docker Compose 構建流程完全回復正常，能正確將更新後的專案代碼封裝入邊緣節點容器中。

# Lessons Learned
容器配置必須與專案軟體架構同步演進。在進行重大程式碼重構時，第一時間需將外部的編排配置（Orchestration Config）納入修改範疇，避免開發環境與部署環境產生路徑脫節。
