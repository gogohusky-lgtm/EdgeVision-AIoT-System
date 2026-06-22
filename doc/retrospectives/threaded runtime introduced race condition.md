# Problem:

當Queue進一步導入Producer Thread/Consumer Thread後，Frame Scan與Inference Execution開始並行運作。測試：133 images 時出現：
cv2.imread() failed, 回傳：None

cv2.resize(), Assertion failed

導致
Consumer Thread Crash, Root Cause Analysis

即：
[Producer] Scans directory (os.listdir) & enqueues file path.

[Consumer] Processes file ➔ Deletes file (os.remove).

[Producer] Re-scans or double-enqueues the same file before inventory updates(Consumer delete).

[Consumer] Attempts to process ➔ `cv2.imread()` returns None ➔ `cv2.resize()` triggers Assertion Failed ➔ Thread Crashes.



# Solution

新增：os.path.exists(filepath)檢查。

並加入：

try:
    ...
except Exception:
    ...

保護。

例如：

if not os.path.exists(filepath): skip

#　Result

重新測試 133 images，結果：

- No Thread Crash
- No Traceback
- All Images Logged
- Heartbeat Continues
- MQTT Continues

Runtime 能夠持續運作。

# Lessons Learned

Threading 不會自動提升可靠性。反而會引入：Race Condition

以及：Shared Resource Problems

例如：

File existence
Duplicate queue entries
Concurrent access

在實際 Edge Runtime 中：Correctness > Concurrency

通常比單純增加 Thread 更重要。



# 整體 Lessons Learned（最重要）

This refactoring journey reflects the paradigm shift from building an AI Demo to engineering an Edge AIoT System:

|Dimension|Phase 1 (Functional AI)|Phase 2 (Runtime Architecture)|
|------|------|------|
|Primary Focus|Proving the AI Inference works|Optimizing how the system behaves under load|
|Core Metric|Model Accuracy / FPS|System Uptime / Buffer Resilience / Fault Tolerance|
|Mindset|Feature Development|"Runtime Engineering (Buffering, Concurrency, Failure Handling)"|

這也是專案從「AI Demo」逐步演進為「Edge AIoT System」的重要分水嶺。