# Allowed columns
COLUMNS = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",

    "course.id": "c.course_id",
    "course.name": "c.course_name"
}


def build_query(
    columns,
    filters,
    order_column,
    direction,
    limit
):

    # Validate columns
    for column in columns:

        if column not in COLUMNS:
            raise ValueError(
                "Invalid column: " + column
            )

    # Validate order column
    if order_column not in COLUMNS:
        raise ValueError(
            "Invalid order column"
        )

    # Validate direction
    direction = direction.upper()

    if direction not in ["ASC", "DESC"]:
        raise ValueError(
            "Invalid sort direction"
        )

    # Validate limit
    if limit < 1 or limit > 1000:
        raise ValueError(
            "LIMIT must be between 1 and 1000"
        )

    selected_columns = ", ".join(
        COLUMNS[column]
        for column in columns
    )

    query = f"""
SELECT {selected_columns}
FROM Student s
JOIN CourseRegistration r
    ON s.student_id = r.student_id
JOIN Course c
    ON r.course_id = c.course_id
"""

    parameters = []

    conditions = []

    for column, operator, value in filters:

        if column not in COLUMNS:
            raise ValueError(
                "Invalid filter column"
            )

        if operator not in [
            "=", ">", "<", ">=", "<=", "LIKE"
        ]:
            raise ValueError(
                "Invalid operator"
            )

        conditions.append(
            COLUMNS[column] +
            " " +
            operator +
            " %s"
        )

        parameters.append(value)

    if conditions:

        query += " WHERE "

        query += " AND ".join(conditions)

    query += (
        " ORDER BY "
        + COLUMNS[order_column]
        + " "
        + direction
    )

    query += " LIMIT %s"

    parameters.append(limit)

    return query, parameters


try:

    columns = input(
        "Columns separated by comma: "
    ).split(",")

    columns = [
        column.strip()
        for column in columns
    ]

    number_of_filters = int(
        input("Number of filters: ")
    )

    filters = []

    for i in range(number_of_filters):

        print(
            "Enter filter:",
            "column operator value"
        )

        parts = input().split(
            maxsplit=2
        )

        if len(parts) != 3:
            raise ValueError(
                "Invalid filter format"
            )

        column = parts[0]
        operator = parts[1]
        value = parts[2]

        filters.append(
            (column, operator, value)
        )

    order_column = input(
        "Order column: "
    ).strip()

    direction = input(
        "Sort direction: "
    ).strip()

    limit = int(
        input("Limit: ")
    )

    query, parameters = build_query(
        columns,
        filters,
        order_column,
        direction,
        limit
    )

    print("\nSQL_OK")
    print(query.strip())
    print("Parameters:", parameters)

except ValueError as e:

    print("ERROR:", e)