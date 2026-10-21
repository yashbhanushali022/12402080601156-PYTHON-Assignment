# Q2 - Optimized Password Audit

import re

b = int(input())

banned_words = []

for _ in range(b):
    banned_words.append(input().strip().lower())

n = int(input())

for index in range(1, n + 1):

    password = input().strip()

    # Length check
    if len(password) < 6 or len(password) > 12:
        print(f"{index}: WEAK_LENGTH")
        continue

    # Character checks
    has_lower = re.search(r"[a-z]", password)
    has_upper = re.search(r"[A-Z]", password)
    has_digit = re.search(r"[0-9]", password)
    has_special = re.search(r"[$#@]", password)

    if not (has_lower and has_upper and has_digit and has_special):
        print(f"{index}: WEAK_PATTERN")
        continue

    # More than 3 same characters continuously
    if re.search(r"(.)\1\1\1", password):
        print(f"{index}: WEAK_PATTERN")
        continue

    # Banned word check
    password_lower = password.lower()

    compromised = False

    for word in banned_words:
        if word in password_lower:
            compromised = True
            break

    if compromised:
        print(f"{index}: COMPROMISED")
    else:
        print(f"{index}: STRONG")