import os
import pandas as pd
import matplotlib.pyplot as plt


def get_grade(mark):

    if mark >= 90:
        return "A+"

    elif mark >= 80:
        return "A"

    elif mark >= 70:
        return "B"

    elif mark >= 60:
        return "C"

    elif mark >= 50:
        return "D"

    else:
        return "F"


csv_path = input(
    "Enter marks CSV path: "
).strip()


output_folder = input(
    "Enter output folder: "
).strip()


os.makedirs(
    output_folder,
    exist_ok=True
)


try:

    # Read CSV
    data = pd.read_csv(
        csv_path
    )


    # Required columns
    if (
        "enrollment" not in data.columns
        or
        "name" not in data.columns
    ):

        raise ValueError(
            "CSV must contain enrollment and name columns."
        )


    # Find subject columns
    subjects = [
        column
        for column in data.columns
        if column not in [
            "enrollment",
            "name"
        ]
    ]


    # Convert marks to numeric
    for subject in subjects:

        data[subject] = pd.to_numeric(
            data[subject],
            errors="coerce"
        )


        # Invalid marks
        data.loc[
            (data[subject] < 0)
            |
            (data[subject] > 100),
            subject
        ] = pd.NA


        # Fill missing marks with average
        average = data[
            subject
        ].mean()


        data[subject] = data[
            subject
        ].fillna(average)


    # -------------------------
    # Cleaned CSV
    # -------------------------

    cleaned_file = os.path.join(
        output_folder,
        "cleaned_marks.csv"
    )

    data.to_csv(
        cleaned_file,
        index=False
    )


    # -------------------------
    # Subject Statistics
    # -------------------------

    summary = pd.DataFrame({

        "subject": subjects,

        "average": [
            data[subject].mean()
            for subject in subjects
        ],

        "minimum": [
            data[subject].min()
            for subject in subjects
        ],

        "maximum": [
            data[subject].max()
            for subject in subjects
        ]
    })


    summary_file = os.path.join(
        output_folder,
        "summary.csv"
    )


    summary.to_csv(
        summary_file,
        index=False
    )


    # -------------------------
    # Grade Distribution
    # -------------------------

    all_marks = (
        data[subjects]
        .stack()
    )


    grades = all_marks.apply(
        get_grade
    )


    grades.value_counts().sort_index().plot(
        kind="bar",
        title="Grade Distribution"
    )


    plt.xlabel("Grade")

    plt.ylabel(
        "Number of Students"
    )

    plt.tight_layout()


    grade_chart = os.path.join(
        output_folder,
        "grade_distribution.png"
    )


    plt.savefig(
        grade_chart
    )

    plt.close()


    # -------------------------
    # Subject Average
    # -------------------------

    summary.plot(
        x="subject",
        y="average",
        kind="bar",
        legend=False,
        title="Subject-wise Average"
    )


    plt.ylabel(
        "Average Marks"
    )

    plt.tight_layout()


    average_chart = os.path.join(
        output_folder,
        "subject_average.png"
    )


    plt.savefig(
        average_chart
    )

    plt.close()


    # -------------------------
    # Top Performers
    # -------------------------

    data["total"] = data[
        subjects
    ].sum(axis=1)


    top_students = data.nlargest(
        10,
        "total"
    )


    plt.bar(
        top_students["name"].astype(str),
        top_students["total"]
    )


    plt.title(
        "Top Performers"
    )

    plt.xlabel(
        "Student"
    )

    plt.ylabel(
        "Total Marks"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    plt.tight_layout()


    top_chart = os.path.join(
        output_folder,
        "top_performers.png"
    )


    plt.savefig(
        top_chart
    )

    plt.close()


    print("\nFiles created:")

    print(
        "cleaned_marks.csv"
    )

    print(
        "summary.csv"
    )

    print(
        "grade_distribution.png"
    )

    print(
        "subject_average.png"
    )

    print(
        "top_performers.png"
    )


except FileNotFoundError:

    print(
        "ERROR: CSV file not found."
    )


except Exception as e:

    print(
        "ERROR:",
        e
    )