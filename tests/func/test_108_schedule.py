"""Test: schedule"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import schedule, time
    counter = [0]
    def job():
        counter[0] += 1
    schedule.every(1).seconds.do(job)
    time.sleep(1.1)
    schedule.run_pending()
    assert counter[0] >= 1, f"counter={counter[0]}"
    schedule.clear()

    import threading
    lock = threading.Lock()
    mt = [0]
    stop = threading.Event()
    def mt_job():
        with lock:
            mt[0] += 1
    schedule.every(1).seconds.do(mt_job)
    def worker_loop():
        while not stop.is_set():
            schedule.run_pending()
            time.sleep(0.05)
    worker = threading.Thread(target=worker_loop, daemon=True)
    worker.start()
    time.sleep(1.5)
    stop.set()
    worker.join(timeout=2.0)
    assert not worker.is_alive(), "worker did not exit cleanly"
    assert mt[0] >= 1, f"mt-counter={mt[0]}"
    schedule.clear()

    print("schedule: PASS")
except Exception as e:
    print(f"schedule: FAIL: {e}")
    sys.exit(1)
