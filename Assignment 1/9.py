# Q9 - Threaded Job Scheduler

import threading
import heapq


w, n = map(int, input().split())

jobs = []

for arrival_order in range(n):

    arrival, job_id, priority, duration, resources = input().split()

    job = {
        "arrival": int(arrival),
        "id": job_id,
        "priority": int(priority),
        "duration": int(duration),
        "resources": int(resources),
        "order": arrival_order
    }

    jobs.append(job)


# Higher priority first
# Earlier arrival first when priority is equal
jobs.sort(
    key=lambda job: (
        job["arrival"],
        -job["priority"],
        job["order"]
    )
)


worker_available = [0] * w

results = []

lock = threading.Lock()


def execute_job(job, worker_id, start_time):

    finish_time = start_time + job["duration"]

    with lock:

        results.append({
            "id": job["id"],
            "worker": worker_id,
            "start": start_time,
            "finish": finish_time,
            "waiting": start_time - job["arrival"]
        })


# Simulate scheduling
threads = []

for job in jobs:

    # Select worker that becomes available first
    worker_index = min(
        range(w),
        key=lambda x: worker_available[x]
    )

    start_time = max(
        job["arrival"],
        worker_available[worker_index]
    )

    worker_available[worker_index] = (
        start_time + job["duration"]
    )

    thread = threading.Thread(
        target=execute_job,
        args=(
            job,
            worker_index + 1,
            start_time
        )
    )

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()


# Sort report by job ID
results.sort(key=lambda x: x["id"])

for result in results:

    print(
        result["id"],
        f"W{result['worker']}",
        result["start"],
        result["finish"]
    )


average_wait = (
    sum(result["waiting"] for result in results)
    / len(results)
)

print(f"AVG_WAIT {average_wait:.2f}")