def bellman_ford(
  start: int, edges: dict[tuple[int, int], int]
) -> tuple[dict[int, float], dict[int, int | None], bool]:
  cost: dict[int, float] = {}
  previous: dict[int, int | None] = {}
  for vertex_a, vertex_b in edges:
    cost[vertex_a] = float('inf')
    cost[vertex_b] = float('inf')
    previous[vertex_a] = None
    previous[vertex_b] = None
  cost[start] = 0

  vertex_count = len(cost)
  for _ in range(vertex_count):
    updated = False
    for (vertex_a, vertex_b), weight in edges.items():
      new_cost = cost[vertex_a] + weight
      if new_cost < cost[vertex_b]:
        cost[vertex_b] = new_cost
        previous[vertex_b] = vertex_a
        updated = True
    if not updated:
      return cost, previous, False

  return cost, previous, True
