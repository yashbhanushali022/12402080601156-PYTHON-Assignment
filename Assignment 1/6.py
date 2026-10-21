# Q6 - Python Module Dependency Resolver

import heapq

n, e = map(int, input().split())

modules = []

for _ in range(n):
    modules.append(input().strip())

graph = {module: [] for module in modules}
indegree = {module: 0 for module in modules}

edges = set()

for _ in range(e):

    a, b = input().split()

    # a imports b
    # Therefore b must be loaded before a

    if (a, b) not in edges:

        edges.add((a, b))

        graph[b].append(a)
        indegree[a] += 1


# Lexicographically smallest module first
heap = []

for module in modules:

    if indegree[module] == 0:
        heapq.heappush(heap, module)


order = []

while heap:

    current = heapq.heappop(heap)

    order.append(current)

    for next_module in graph[current]:

        indegree[next_module] -= 1

        if indegree[next_module] == 0:
            heapq.heappush(heap, next_module)


if len(order) == n:

    print(*order)

else:

    print("CYCLE")

    # Find one cycle using DFS

    state = {module: 0 for module in modules}
    path = []
    position = {}

    cycle = []

    def find_cycle(node):

        global cycle

        state[node] = 1
        position[node] = len(path)
        path.append(node)

        for neighbor in graph[node]:

            if state[neighbor] == 0:

                if find_cycle(neighbor):
                    return True

            elif state[neighbor] == 1:

                start = position[neighbor]
                cycle.extend(path[start:])
                cycle.append(neighbor)

                return True

        path.pop()
        position.pop(node, None)
        state[node] = 2

        return False


    for module in sorted(modules):

        if state[module] == 0:

            if find_cycle(module):
                break

    if cycle:
        print(*cycle)