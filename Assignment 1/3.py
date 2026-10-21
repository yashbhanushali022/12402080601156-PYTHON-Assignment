# Q3 - Recursive Expression Engine

import re

v = int(input())

expressions = {}

for _ in range(v):
    line = input()

    name, expression = line.split("=", 1)

    name = name.strip()
    expression = expression.strip()

    expressions[name] = expression

main_expression = input().strip()

memo = {}
visiting = set()


def tokenize(expression):
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[()+\-*]", expression)


def evaluate_variable(name):

    if name in memo:
        return memo[name]

    if name in visiting:
        raise ValueError("CYCLE")

    if name not in expressions:
        raise ValueError("INVALID")

    visiting.add(name)

    try:
        value = evaluate_expression(expressions[name])
        memo[name] = value
    finally:
        visiting.remove(name)

    return value


def evaluate_expression(expression):

    tokens = tokenize(expression)

    if not tokens:
        raise ValueError("INVALID")

    position = [0]

    def parse_expression():

        value = parse_term()

        while position[0] < len(tokens):

            operator = tokens[position[0]]

            if operator not in ["+", "-"]:
                break

            position[0] += 1
            right = parse_term()

            if operator == "+":
                value += right
            else:
                value -= right

        return value

    def parse_term():

        value = parse_factor()

        while position[0] < len(tokens):

            operator = tokens[position[0]]

            if operator != "*":
                break

            position[0] += 1

            right = parse_factor()
            value *= right

        return value

    def parse_factor():

        if position[0] >= len(tokens):
            raise ValueError("INVALID")

        token = tokens[position[0]]

        if token == "(":

            position[0] += 1

            value = parse_expression()

            if position[0] >= len(tokens):
                raise ValueError("INVALID")

            if tokens[position[0]] != ")":
                raise ValueError("INVALID")

            position[0] += 1

            return value

        if token.isdigit():

            position[0] += 1
            return int(token)

        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", token):

            position[0] += 1
            return evaluate_variable(token)

        raise ValueError("INVALID")

    result = parse_expression()

    if position[0] != len(tokens):
        raise ValueError("INVALID")

    return result


try:
    answer = evaluate_expression(main_expression)
    print(answer)

except ValueError as error:

    if str(error) == "CYCLE":
        print("CYCLE")
    else:
        print("INVALID")