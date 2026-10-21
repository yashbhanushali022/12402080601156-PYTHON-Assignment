# Q8 - Compressed Log Index

import os
import re
import pickle
import zipfile


def build_index(folder, zip_name):

    index = {}

    total_files = 0
    total_lines = 0

    for filename in os.listdir(folder):

        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        total_files += 1

        with open(path, "r", encoding="utf-8",
                  errors="ignore") as file:

            for line_number, line in enumerate(file, 1):

                total_lines += 1

                # Convert text into normalized words
                words = re.findall(
                    r"[A-Za-z0-9_]+",
                    line.lower()
                )

                for word in words:

                    if word not in index:
                        index[word] = []

                    index[word].append(
                        (filename, line_number)
                    )

    pickle_file = "log_index.pkl"

    with open(pickle_file, "wb") as file:
        pickle.dump(index, file)

    # Create ZIP file
    with zipfile.ZipFile(
        zip_name,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        archive.write(
            pickle_file,
            arcname=pickle_file
        )

        for filename in os.listdir(folder):

            path = os.path.join(folder, filename)

            if os.path.isfile(path):
                archive.write(
                    path,
                    arcname=os.path.join(
                        "logs",
                        filename
                    )
                )

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search_index(pickle_path, queries):

    with open(pickle_path, "rb") as file:
        index = pickle.load(file)

    for token in queries:

        token = token.lower()

        print(token + ":")

        if token not in index:
            print("No matches")
            continue

        for filename, line_number in index[token]:
            print(
                f"{filename}:{line_number}"
            )


mode = input().strip().upper()

if mode == "BUILD":

    folder, zip_name = input().split()

    build_index(folder, zip_name)

elif mode == "SEARCH":

    pickle_path = input().strip()

    q = int(input())

    queries = []

    for _ in range(q):
        queries.append(input().strip())

    search_index(
        pickle_path,
        queries
    )

else:

    print("INVALID MODE")