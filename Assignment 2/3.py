import csv
import mysql.connector


try:

    host = input("Host [localhost]: ").strip()
    if host == "":
        host = "localhost"

    user = input("Username [root]: ").strip()
    if user == "":
        user = "root"

    password = input("Password: ")

    database = input("Database name: ").strip()

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()

    # Student table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INT PRIMARY KEY,
            name VARCHAR(100),
            spi DECIMAL(3,1)
        )
    """)

    # Course table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Course (
            course_id VARCHAR(20) PRIMARY KEY,
            course_name VARCHAR(100)
        )
    """)

    # Registration table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id INT,
            course_id VARCHAR(20),
            PRIMARY KEY(student_id, course_id),
            FOREIGN KEY(student_id)
                REFERENCES Student(student_id),
            FOREIGN KEY(course_id)
                REFERENCES Course(course_id)
        )
    """)

    connection.commit()

    student_file = input("Student CSV file: ").strip()

    with open(student_file, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            cursor.execute("""
                INSERT INTO Student
                (student_id, name, spi)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                spi = VALUES(spi)
            """, (
                int(row["student_id"]),
                row["name"],
                float(row["spi"])
            ))

    registration_file = input(
        "Registration CSV file: "
    ).strip()

    with open(
        registration_file,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            cursor.execute("""
                INSERT IGNORE INTO CourseRegistration
                (student_id, course_id)
                VALUES (%s, %s)
            """, (
                int(row["student_id"]),
                row["course_id"]
            ))

    connection.commit()

    course_id = input("Course ID: ").strip()

    spi_threshold = float(
        input("SPI threshold: ")
    )

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            s.spi,
            r.course_id
        FROM Student s
        JOIN CourseRegistration r
            ON s.student_id = r.student_id
        WHERE r.course_id = %s
          AND s.spi > %s
        ORDER BY
            s.spi DESC,
            s.student_id ASC
    """, (
        course_id,
        spi_threshold
    ))

    rows = cursor.fetchall()

    for row in rows:
        print(*row)

    cursor.close()
    connection.close()

except mysql.connector.Error as e:

    print("Database Error:", e)

except (ValueError, FileNotFoundError) as e:

    print("Error:", e)