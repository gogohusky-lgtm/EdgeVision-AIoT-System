# Queue draining and duplicate enqueue analysis

## Background

During high-stress reliability testing of the Edge AI runtime engine, a batch of 322 images was injected into the ingest directory (captured_frames/), followed by a forced SIGINT (Ctrl+C) to trigger a graceful shutdown.

* The Symptom:

The system suffered from data loss and non-deterministic behavior during termination:

Out of 322 source images, only 315 were processed and recorded in the CSV logs. 7 images were left stranded in the ingestion directory, completely unprocessed.

The system failed to achieve a truly "graceful" shutdown, leaving in-flight tasks truncated.

Through systematic, iterative debugging, the issue was traced down to three independent, cascading runtime flaws detailed below.

---

## Root Cause Analysis & Iterative Resolutions

### Issue 1: In-Flight Task Truncation via Premature Consumer Termination

Diagnosis:

The initial shutdown sequence in frame_to_inference.py relied on polling the queue status:

```
# Legacy Insecure Shutdown Logic
while not FRAME_QUEUE.empty():
    time.sleep(1)
consumer.stop() # Premature termination trigger
```
The Flaw: 

When the FRAME_QUEUE became structurally empty, the main thread immediately invoked consumer.stop(). However, the consumer thread was often still actively executing inference on the last few frames fetched from the queue. Moving straight to thread termination truncated these active in-flight tasks.

### Resolution

Swapped the naive queue-emptiness polling with a deterministic synchronization barrier using queue.join(). This ensures that the main thread blocks until all dequeued frames explicitly signal completion via task_done().

```Python
# Refactored Graceful Shutdown Sequence
producer.stop()
producer.join()

# Explicit block until all active consumer tasks signal task_done()
FRAME_QUEUE.join() 

consumer.stop()
consumer.join()
mqtt.disconnect()
```

### Result (Iteration 1)

Stranded files still remained in the workspace. However, the synchronized logging revealed a new clue: certain files were being picked up and processed multiple times, pointing to a secondary race condition.

---

### Issue 2: Duplicate Enqueuing via File-System Synchronization Lag

Diagnosis:

An asynchronous race condition existed between the high-frequency I/O Producer loop and the compute-heavy Consumer loop:

The Producer scanned the directory (os.listdir) and enqueued a file path.

The Consumer dequeued the path, executed the deep learning inference, and subsequently purged the file via os.remove().

The Race: Because file I/O and model inference take time, the ultra-fast Producer loop rescanned the directory and double-enqueued the same file path before the Consumer had a chance to delete it from the disk.

### Resolution
Introduced an in-memory thread-safe state tracker using a Python set() within the Producer to filter out duplicate files currently in-flight.

```
# Producer tracking state
self.queued_files = set()
```

```
# In Ingestion Loop:
if filepath not in self.queued_files:
    self.frame_queue.put_nowait(filepath)
    self.queued_files.add(filepath)
```

```
# In Consumer (Post-inference & Post-deletion Cleanup):
self.producer.queued_files.remove(filepath)
```
### Result (Iteration 2)
Duplicate inference logs dropped to 0%. However, data loss persisted under massive burst traffic, with files still left behind in the workspace directory.

---

### Issue 3: Silent Frame Dropping under Queue Saturation (Backpressure Failure)

Diagnosis:

The root cause shifted to the Producer's queue insertion policy. To prevent the thread from locking up, the Producer utilized non-blocking ingestion wrapped in a blind catch-all exception block:

```
# Legacy Non-Blocking Drop Policy
try:
    self.frame_queue.put_nowait(filepath)
    self.queued_files.add(filepath)
except Exception:
    pass # Silent failure! Excess frames dropped when queue hit max capacity
```


The Flaw: 

The bounded queue capacity was set to 50. Under a sudden burst of 322 images, the compute-heavy inference loop naturally bottlenecked the consumer. The queue hit full capacity rapidly, causing put_nowait() to throw a queue.Full exception. The Producer caught this and silently skipped the file, resulting in untracked data drops.

### Resolution
Transitioned from a non-blocking "Drop Policy" to a Blocking Backpressure Policy by switching to a standard blocking .put().

```
# Refactored Backpressure Ingestion
# Thread will naturally block and wait if the queue capacity (50) is reached,
# pacing the producer according to the downstream consumer's processing speed.
self.frame_queue.put(filepath) 
self.queued_files.add(filepath)
```

### Results

All 322 pictures were processed completedly and workspace cleaned.

---

## Important Engineering Lessons

### Runtime correctness is more important than concurrency

Introducing threads improved system responsiveness but also introduced race conditions and shared-state issues.

Concurrency does not automatically improve reliability.

Correctness must always come first.

---

### Queue design determines system behavior

A queue is not merely a data structure.

It represents a runtime policy.

Different queue policies lead to different system behaviors:

- Block when full
- Drop oldest
- Drop newest
- Prioritized processing

The correct policy depends on the application requirements.

---

### Robustness emerges from iterative debugging

Most runtime failures were not visible during light testing.

Many issues only appeared under burst traffic and large batch processing.

Stress testing revealed hidden assumptions in:

- Threading
- Queue management
- Shutdown logic

Robust systems are rarely designed perfectly from the beginning.

They evolve through repeated failure analysis and refinement.

