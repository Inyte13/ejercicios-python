import random
from typing import Literal

import numpy
from generator_graph.draw import to_graph
from numpy.typing import NDArray
from scipy.spatial import Delaunay

MIN_DISTANCE = 0.2


def create_points(vertex_count: int) -> NDArray[numpy.float64]:
  points: list[NDArray[numpy.float64]] = []
  while len(points) < vertex_count:
    candidate = numpy.random.random(2)
    if all(
      numpy.linalg.norm(candidate - point) >= MIN_DISTANCE for point in points
    ):
      points.append(candidate)
  return numpy.array(points)


def normalize(vertex_a: int, vertex_b: int) -> tuple[int, int]:
  return (min(vertex_a, vertex_b), max(vertex_a, vertex_b))


def create_planar_edges(
  points: NDArray[numpy.float64],
) -> set[tuple[int, int]]:
  triangles = Delaunay(points).simplices.tolist()
  edges: set[tuple[int, int]] = set()
  for first_vertex, second_vertex, third_vertex in triangles:
    sides = (
      (first_vertex, second_vertex),
      (second_vertex, third_vertex),
      (first_vertex, third_vertex),
    )
    for vertex_a, vertex_b in sides:
      edges.add(normalize(vertex_a, vertex_b))
  return edges


def build_unweighted_adjacency(
  edges: set[tuple[int, int]],
) -> dict[int, list[int]]:
  adjacency: dict[int, list[int]] = {}
  for vertex_a, vertex_b in edges:
    if vertex_a not in adjacency:
      adjacency[vertex_a] = []
    if vertex_b not in adjacency:
      adjacency[vertex_b] = []
    adjacency[vertex_a].append(vertex_b)
    adjacency[vertex_b].append(vertex_a)
  return adjacency


def _dfs(adjacency: dict[int, list[int]]) -> dict[int, list[int]]:
  vertices = list(adjacency.keys())
  start = random.choice(vertices)
  visited = {start}
  stack = [start]
  dfs: dict[int, list[int]] = {start: []}
  while stack != []:
    target = stack[-1]
    unvisited: list[int] = []
    for neighbor in adjacency[target]:
      if neighbor not in visited:
        unvisited.append(neighbor)
    if unvisited != []:
      next = random.choice(unvisited)
      visited.add(next)
      dfs[next] = [target]
      dfs[target].append(next)
      stack.append(next)
    else:
      stack.pop()
  return dfs


def edges_from_adjacency(
  adjacency: dict[int, list[int]],
) -> set[tuple[int, int]]:
  edges: set[tuple[int, int]] = set()
  for vertex, neighbors in adjacency.items():
    for neighbor in neighbors:
      edges.add((min(vertex, neighbor), max(vertex, neighbor)))
  return edges


RATIOS = {1: 0.15, 2: 0.70, 3: 0.85}


def delete_edges(
  total_edges: set[tuple[int, int]],
  dfs_edges: set[tuple[int, int]],
  density: Literal[1, 2, 3],
) -> set[tuple[int, int]]:
  edges = list(total_edges - dfs_edges)
  remaining = round(len(edges) * RATIOS[density])
  finally_edges = random.sample(edges, remaining)
  return dfs_edges.union(finally_edges)


def assign_weights(
  edges: set[tuple[int, int]], min_weight: int, max_weight: int
) -> dict[tuple[int, int], int]:
  edges_with_weight: dict[tuple[int, int], int] = {}
  for edge in edges:
    edges_with_weight[edge] = random.randint(min_weight, max_weight)
  return edges_with_weight


def build_weighted_adjacency(
  edges: dict[tuple[int, int], int], directed: bool
) -> dict[int, list[tuple[int, int]]]:
  adjacency: dict[int, list[tuple[int, int]]] = {}
  for (vertex_a, vertex_b), weight in edges.items():
    if vertex_a not in adjacency:
      adjacency[vertex_a] = []
    if vertex_b not in adjacency:
      adjacency[vertex_b] = []
    adjacency[vertex_a].append((vertex_b, weight))
    if not directed:
      adjacency[vertex_b].append((vertex_a, weight))
  return adjacency


def create_random_graph_undirected(
  vertex_count: int,
  min_weight: int,
  max_weight: int,
) -> tuple[dict[int, list[tuple[int, int]]], dict[tuple[int, int], int], int]:
  points = create_points(vertex_count)
  edges = create_planar_edges(points)
  adjacency_unweighted = build_unweighted_adjacency(edges)
  dfs_edges = _dfs(adjacency_unweighted)
  finally_edges = delete_edges(edges, edges_from_adjacency(dfs_edges), 2)
  edges_with_weight = assign_weights(finally_edges, min_weight, max_weight)
  adjacency_weighted = build_weighted_adjacency(edges_with_weight, False)
  vertices = list(adjacency_unweighted.keys())
  start = random.choice(vertices)
  to_graph(points, edges_with_weight, start, False)
  return adjacency_weighted, edges_with_weight, start
