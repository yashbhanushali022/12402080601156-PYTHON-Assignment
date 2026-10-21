MOD = 1000000007

NEGATIVE_INFINITY = -10**30


n, m = map(
    int,
    input().split()
)


matrix = []

for _ in range(n):

    row = input().split()

    matrix.append(row)


# Best score for current row
score = [
    NEGATIVE_INFINITY
] * m


# Number of ways to achieve best score
ways = [0] * m


for i in range(n):

    new_score = [
        NEGATIVE_INFINITY
    ] * m

    new_ways = [0] * m


    for j in range(m):

        if matrix[i][j] == "X":
            continue


        value = int(
            matrix[i][j]
        )


        # Starting cell
        if i == 0 and j == 0:

            new_score[j] = value

            new_ways[j] = 1

            continue


        candidates = []


        # From above
        if (
            i > 0
            and score[j] != NEGATIVE_INFINITY
        ):

            candidates.append(
                (
                    score[j],
                    ways[j]
                )
            )


        # From left
        if (
            j > 0
            and new_score[j - 1]
                != NEGATIVE_INFINITY
        ):

            candidates.append(
                (
                    new_score[j - 1],
                    new_ways[j - 1]
                )
            )


        # From diagonal
        if (
            i > 0
            and j > 0
            and score[j - 1]
                != NEGATIVE_INFINITY
        ):

            candidates.append(
                (
                    score[j - 1],
                    ways[j - 1]
                )
            )


        if candidates:

            best_score = max(
                score_value
                for score_value, _ in candidates
            )


            count = 0

            for score_value, path_count in candidates:

                if score_value == best_score:

                    count += path_count


            count %= MOD


            new_score[j] = (
                best_score + value
            )

            new_ways[j] = count


    score = new_score
    ways = new_ways


if score[m - 1] == NEGATIVE_INFINITY:

    print("IMPOSSIBLE")

else:

    print(
        score[m - 1],
        ways[m - 1]
    )