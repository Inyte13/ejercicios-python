from generator_graph.directed_graph import create_random_graph_directed
from generator_graph.draw import print_table
from path_menor.bellman_ford import bellman_ford
from path_menor.dijkstra import dijkstra


def main():
  adjacency_weighted, edges_with_weight, start = create_random_graph_directed(
    8, 1, 10, 3
  )
  cost_bellman, previous_bellman, has_cycles = bellman_ford(
    start, edges_with_weight
  )
  print('Bellman Ford')
  print_table(cost_bellman, previous_bellman, has_cycles)

  cost_dijkstra, previous_dijkstra = dijkstra(start, adjacency_weighted)
  print('Dijkstra')
  print_table(cost_dijkstra, previous_dijkstra)


main()
