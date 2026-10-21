# Q1 - Campus Merit Analyzer

n, k, m = map(int, input().split())

students = []
semester_students = {}

for _ in range(n):
    data = input().split()

    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])
    marks = list(map(int, data[4:]))

    student = {
        "enrollment": enrollment,
        "name": name,
        "semester": semester,
        "cpi": cpi,
        "marks": marks
    }

    students.append(student)

    if semester not in semester_students:
        semester_students[semester] = []

    semester_students[semester].append(student)

# Semester-wise top K
for semester in sorted(semester_students):

    group = semester_students[semester]

    group.sort(
        key=lambda s: (
            -s["cpi"],
            -sum(s["marks"]) / m,
            s["enrollment"]
        )
    )

    print(
        f"Semester {semester}:",
        *[s["enrollment"] for s in group[:k]]
    )

# Subject-wise toppers
for subject in range(m):

    highest = -1
    toppers = []

    for student in students:

        mark = student["marks"][subject]

        if mark > highest:
            highest = mark
            toppers = [student["enrollment"]]

        elif mark == highest:
            toppers.append(student["enrollment"])

    print(f"S{subject + 1}:", *toppers)