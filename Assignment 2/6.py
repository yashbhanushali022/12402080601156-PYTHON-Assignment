from collections import defaultdict, deque
import re


X, T = map(
    int,
    input().split()
)

n = int(input())

failures = defaultdict(deque)

suspicious = {}


pattern = re.compile(
    r"^(\d{2}):(\d{2})\s+"
    r"(\S+)\s+"
    r"(\S+)\s+"
    r"(FAIL|SUCCESS)$"
)


def convert_time(hour, minute):

    return (
        int(hour) * 60
        + int(minute)
    )


for _ in range(n):

    line = input().strip()

    match = pattern.match(line)

    if not match:
        continue

    hour, minute, user, ip, status = (
        match.groups()
    )

    current_time = convert_time(
        hour,
        minute
    )

    queue = failures[user]


    if status == "FAIL":

        queue.append(
            (current_time, ip)
        )

        while (
            queue
            and current_time - queue[0][0] > T
        ):
            queue.popleft()


    else:

        while (
            queue
            and current_time - queue[0][0] > T
        ):
            queue.popleft()

        if len(queue) >= X:

            different_ip = any(
                failed_ip != ip
                for _, failed_ip in queue
            )

            if different_ip:

                if user not in suspicious:

                    suspicious[user] = (
                        f"{hour}:{minute}"
                    )


for user in sorted(suspicious):

    print(
        user,
        suspicious[user]
    )