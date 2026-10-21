# Q7 - Interactive Formula Validator

class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


variables = {}


def get_value(value):

    # Variable
    if value.isidentifier():

        if value not in variables:
            raise UnknownVariableError(
                f"Unknown variable: {value}"
            )

        return variables[value]

    # Number
    try:
        return float(value)

    except ValueError:
        raise InvalidFormatError(
            "Invalid operand"
        )


while True:

    line = input().strip()

    if line.lower() == "quit":
        break

    try:

        # Assignment
        if "=" in line:

            parts = line.split("=")

            if len(parts) != 2:
                raise InvalidFormatError(
                    "Invalid assignment"
                )

            name = parts[0].strip()
            value = parts[1].strip()

            if not name.isidentifier():
                raise InvalidFormatError(
                    "Invalid variable name"
                )

            variables[name] = get_value(value)

            continue

        parts = line.split()

        if len(parts) != 3:
            raise InvalidFormatError(
                "Expected: operand operator operand"
            )

        left = get_value(parts[0])
        operator = parts[1]
        right = get_value(parts[2])

        if operator not in ["+", "-", "*", "/", "%"]:
            raise UnsupportedOperatorError(
                "Unsupported operator"
            )

        if operator in ["/", "%"] and right == 0:
            raise DivisionByZeroError(
                "Division by zero"
            )

        if operator == "+":
            result = left + right

        elif operator == "-":
            result = left - right

        elif operator == "*":
            result = left * right

        elif operator == "/":
            result = left / right

        elif operator == "%":
            result = left % right

        if result.is_integer():
            print(int(result))
        else:
            print(result)

    except (
        InvalidFormatError,
        UnknownVariableError,
        DivisionByZeroError,
        UnsupportedOperatorError
    ) as error:

        print(type(error).__name__)