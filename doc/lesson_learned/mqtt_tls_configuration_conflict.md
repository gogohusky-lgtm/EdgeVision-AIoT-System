# Problem
邊緣端推論程式嘗試連線本機 MQTT Broker（localhost:1883）時發生中斷，TCP 層級顯示連線成功後隨即被拒絕，錯誤代碼為 Connection failed: rc=5 (Unexpected disconnect)。

# Root Cause
經排查發現：

1. 系統僅監聽 TLS Port 8883
2. 舊有 TLS 設定要求 Client Certificate
3. EdgeVision 使用未加密的 localhost:1883

因此 MQTT CONNECT 封包被 Broker 拒絕。

# Solution
清理衝突配置：移除 /etc/mosquitto/conf.d/ 目錄中舊專案殘留的全域 TLS 限制設定檔（TLS_Enable.conf）。

隔離環境配置：明確劃分 Plain MQTT 監聽配置，避免在同一個連接埠（Port）發生 Listener 重複定義（Duplicate Listener）導致 Broker 服務啟動失敗的問題。

重啟網路服務：重置系統 Mosquitto 服務狀態。

# Result
網路中介軟體（Broker）成功回復標準通訊狀態，邊緣端推論節點與 MQTT Broker 順利達成穩定連線，阻斷完全排除。

# Lessons Learned
當軟體部署到非全新（Non-pristine）的真實硬體環境時，既有的系統全域配置往往會成為隱形的干擾源。理解通訊組件（如 Mosquitto）的多檔案合併與覆蓋行為（Config Layering），是確保邊緣端分散式通訊順暢的基礎硬實力。
