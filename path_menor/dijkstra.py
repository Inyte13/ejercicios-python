import heapq


# Encontrar los mejores caminos desde A - TODOS
def dijkstra(
  start: int, adjacency: dict[int, list[tuple[int, int]]]
) -> tuple[dict[int, float], dict[int, int | None]]:
  cost: dict[int, float] = {}
  previous: dict[int, int | None] = {}
  for vertex in adjacency:
    cost[vertex] = float('inf')
    previous[vertex] = None
  cost[start] = 0

  priority_queue: list[tuple[float, int]] = [(0, start)]
  while priority_queue != []:
    target_cost, vertex = heapq.heappop(priority_queue)
    if target_cost > cost[vertex]:
      continue
    for neighbord, weight in adjacency[vertex]:
      new_cost = target_cost + weight
      if new_cost < cost[neighbord]:
        cost[neighbord] = new_cost
        previous[neighbord] = vertex
        heapq.heappush(priority_queue, (new_cost, neighbord))
  return cost, previous
