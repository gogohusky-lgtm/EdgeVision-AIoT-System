# Problem
容器啟動後，檢查 Container 內部確實已在 /app/monitoring/logs/inference_log.csv 生成了推論遙測日誌，然而在宿主機（Host）對應的掛載目錄下卻完全看不到該 CSV 檔案，導致邊緣端的持久化觀測日誌缺失。

# Root Cause

Docker 容器內實際寫入位置：/app/monitoring/logs

而 Docker Compose 綁定掛載（Bind Mount）的位置為：/app/src/monitoring/logs

兩者不一致。

因此 CSV 實際生成於容器內部，但未落在與宿主機同步的掛載目錄。

# Solution
調整 docker-compose.yml 中的 Volume Mapping，使 Host 與 Container 共享的目錄與 logger.py 實際寫入位置一致。

修正後：

Host:
src/monitoring/logs

對映於

Container:
/app/monitoring/logs

# Lessons Learned
「Docker 掛載成功」並不等同於「應用程式成功寫入掛載路徑」。在分散式與容器化架構中，必須全面使用絕對路徑計算來對抗執行環境變更帶來的路徑飄移。排查此類問題時，結合 docker inspect 與 docker exec -it 進行內部實地檢查是最有效的除錯手段。


原因：

logger.py 內使用相對位置：monitoring/logs，
但 docker-compose bind mount映射：/app/src/monitoring/logs
兩邊不是同一路徑。

造成：

Container內生成

Host看不到

以為Logging失敗

實際上沒失敗

只是寫到另一個目錄。

修正：

統一路徑。

Lesson

Docker volume mount success
≠

Application writes to mounted path

必須確認：docker inspect

與

docker exec

實際檢查。