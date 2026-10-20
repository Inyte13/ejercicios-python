import random
from typing import Literal

from generator_graph.draw import to_graph
from generator_graph.undirected_graph import (
  assign_weights,
  build_unweighted_adjacency,
  build_weighted_adjacency,
  create_planar_edges,
  create_points,
  delete_edges,
  edges_from_adjacency,
  normalize,
)


def _dfs(
  adjacency: dict[int, list[int]], start: int
) -> tuple[dict[int, list[int]], list[tuple[int, int]]]:
  visited = {start}
  stack = [start]
  dfs: dict[int, list[int]] = {start: []}
  order: list[tuple[int, int]] = []

  while stack != []:
    target = stack[-1]
    unvisited: list[int] = []
    for neighbor in adjacency[target]:
      if neighbor not in visited:
        unvisited.append(neighbor)
    if unvisited != []:
      next = random.choice(unvisited)
      visited.add(next)
      dfs[next] = []
      dfs[target].append(next)
      order.append((target, next))
      stack.append(next)
    else:
      stack.pop()
  return dfs, order


def _directing_edges(
  edges: set[tuple[int, int]], order: list[tuple[int, int]]
) -> set[tuple[int, int]]:
  order_normalize: set[tuple[int, int]] = set()
  set_order = set(order)
  for vertex_a, vertex_b in order:
    order_normalize.add(normalize(vertex_a, vertex_b))
  for vertex_a, vertex_b in edges - order_normalize:
    if random.random() < 0.5:
      set_order.add((vertex_a, vertex_b))
    else:
      set_order.add((vertex_b, vertex_a))
  return set_order


def create_random_graph_directed(
  vertex_count: int, min_weight: int, max_weight: int,
  density: Literal[1, 2, 3]
) -> tuple[dict[int, list[tuple[int, int]]], dict[tuple[int, int], int], int]:
  points = create_points(vertex_count)
  edges = create_planar_edges(points)
  adjacency_unweighted = build_unweighted_adjacency(edges)
  vertices = list(adjacency_unweighted.keys())
  start = random.choice(vertices)
  dfs_edges, order = _dfs(adjacency_unweighted, start)
  finally_edges = delete_edges(edges, edges_from_adjacency(dfs_edges), density)
  order_edges = _directing_edges(finally_edges, order)
  edges_with_weight = assign_weights(order_edges, min_weight, max_weight)
  adjacency_weighted = build_weighted_adjacency(edges_with_weight, True)
  to_graph(points, edges_with_weight, start, True)
  return adjacency_weighted, edges_with_weight, start


