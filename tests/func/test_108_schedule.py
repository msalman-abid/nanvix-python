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
    print("schedule: PASS")
except Exception as e:
    print(f"schedule: FAIL: {e}")
    sys.exit(1)
