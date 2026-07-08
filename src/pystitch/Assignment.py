from typing import Sequence


# This project doesn't run flake8 yet, but inkstitch's does and this function
# trips C901 there. The branching is inherent to the shortest-augmenting-path
# formulation of the algorithm, not something worth splitting up just to
# satisfy the linter.
def minimal_assignment(cost: Sequence[Sequence[float]]) -> list[int]:  # noqa: C901
    """Solves the assignment problem: given cost[row][column] with
    len(rows) <= len(columns), returns for each row a distinct column such
    that the total cost is minimal (Hungarian algorithm).
    See: https://en.wikipedia.org/wiki/Hungarian_algorithm

    Good visualization: https://www.youtube.com/watch?v=cQ5MsiGaDY8
    but note we are storing an extra matrix (row_potential x column_potential)
    instead of constantly mutating every value in the cost matrix.
    """
    rows = len(cost)
    columns = len(cost[0])
    infinity = float("inf")
    # Potentials and matching, 1-indexed with column 0 as scratch space.
    row_potential: list[float] = [0] * (rows + 1)
    column_potential: list[float] = [0] * (columns + 1)
    match = [0] * (columns + 1)  # match[column] = row assigned to it
    path = [0] * (columns + 1)
    for row in range(1, rows + 1):
        match[0] = row
        j0 = 0
        min_value = [infinity] * (columns + 1)
        used = [False] * (columns + 1)
        while True:
            used[j0] = True
            i0 = match[j0]
            delta = infinity
            j1 = 0
            for j in range(1, columns + 1):
                if used[j]:
                    continue
                current = cost[i0 - 1][j - 1] - row_potential[i0] - column_potential[j]
                if current < min_value[j]:
                    min_value[j] = current
                    path[j] = j0
                if min_value[j] < delta:
                    delta = min_value[j]
                    j1 = j
            for j in range(0, columns + 1):
                if used[j]:
                    row_potential[match[j]] += delta
                    column_potential[j] -= delta
                else:
                    min_value[j] -= delta
            j0 = j1
            if match[j0] == 0:
                break
        while j0 != 0:
            j1 = path[j0]
            match[j0] = match[j1]
            j0 = j1
    assignment = [0] * rows
    for j in range(1, columns + 1):
        if match[j] != 0:
            assignment[match[j] - 1] = j - 1
    return assignment
