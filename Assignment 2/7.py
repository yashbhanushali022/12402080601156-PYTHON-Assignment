import json
from collections import defaultdict


def read_records(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            try:

                yield json.loads(line)

            except json.JSONDecodeError:

                yield None


file_path = input(
    "Enter JSONL file path: "
).strip()


statistics = defaultdict(
    lambda: {
        "count": 0,
        "min": None,
        "max": None,
        "sum": 0.0,
        "corrupted": 0
    }
)


try:

    for record in read_records(
        file_path
    ):

        if record is None:

            statistics["UNKNOWN"][
                "corrupted"
            ] += 1

            continue


        device = record.get(
            "device_id",
            "UNKNOWN"
        )


        try:

            temperature = float(
                record["temperature_c"]
            )

            humidity = float(
                record["humidity"]
            )

        except (
            KeyError,
            ValueError,
            TypeError
        ):

            statistics[device][
                "corrupted"
            ] += 1

            continue


        data = statistics[device]

        data["count"] += 1

        data["sum"] += temperature


        if data["min"] is None:

            data["min"] = temperature

        else:

            data["min"] = min(
                data["min"],
                temperature
            )


        if data["max"] is None:

            data["max"] = temperature

        else:

            data["max"] = max(
                data["max"],
                temperature
            )


    for device in sorted(statistics):

        data = statistics[device]

        if data["count"] == 0:

            print(
                f"{device} "
                f"count=0 "
                f"min=N/A "
                f"max=N/A "
                f"avg=N/A "
                f"corrupted={data['corrupted']}"
            )

        else:

            average = (
                data["sum"]
                / data["count"]
            )

            print(
                f"{device} "
                f"count={data['count']} "
                f"min={data['min']:g} "
                f"max={data['max']:g} "
                f"avg={average:.2f} "
                f"corrupted={data['corrupted']}"
            )


except FileNotFoundError:

    print("ERROR: File not found.")

except OSError as e:

    print("ERROR:", e)