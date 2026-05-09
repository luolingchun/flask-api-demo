import time


def job_test(a: int, b: int, job_id: str):
    print(f"test job {job_id}...")
    time.sleep(30)
    return a + b
