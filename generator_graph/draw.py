import numpy
from matplotlib import pyplot
from matplotlib.collections import LineCollection
from numpy.typing import NDArray


def to_graph(
  points: NDArray[numpy.float64],
  weighted_edges: dict[tuple[int, int], int],
  start: int,
  directed: bool,
) -> None:
  _, ax = pyplot.subplots()

  if directed:
    for vertex_a, vertex_b in weighted_edges:
      ax.annotate(
        '',
        xy=points[vertex_b],
        xytext=points[vertex_a],
        arrowprops={
          'arrowstyle': '-|>',
          'color': 'gray',
          'linewidth': 1.5,
          'shrinkA': 12,
          'shrinkB': 12,
        },
        zorder=1,
      )
  else:
    segments = []
    for vertex_a, vertex_b in weighted_edges:
      segments.append((points[vertex_a], points[vertex_b]))
    ax.add_collection(
      LineCollection(segments, colors='gray', linewidths=1.5, zorder=1)
    )

  for (vertex_a, vertex_b), weight in weighted_edges.items():
    middle_x = (points[vertex_a][0] + points[vertex_b][0]) / 2
    middle_y = (points[vertex_a][1] + points[vertex_b][1]) / 2
    ax.text(
      middle_x,
      middle_y,
      str(weight),
      ha='center',
      va='center',
      fontsize=8,
      zorder=2,
      bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1},
    )

  colors = []
  for vertex in range(len(points)):
    if vertex == start:
      colors.append('lightgreen')
    else:
      colors.append('white')

  ax.scatter(
    points[:, 0],
    points[:, 1],
    s=500,
    facecolors=colors,
    edgecolors='black',
    zorder=3,
  )
  for vertex, (x, y) in enumerate(points):
    ax.text(x, y, str(vertex), ha='center', va='center', zorder=4)

  ax.set_aspect('equal')
  ax.axis('off')
  pyplot.savefig(f'{"directed" if directed else "undirected"}.png')


def print_table(
  cost: dict[int, float],
  previous: dict[int, int | None],
  has_cycles: bool | None = None,
) -> None:
  if has_cycles is not None:
    print('Hay ciclo negativo' if has_cycles else 'Sin ciclo negativo')
  print(f'{"vertice":>8} | {"costo":>8} | {"previo":>6}')
  print('-' * 28)
  for vertex in sorted(cost):
    print(f'{vertex:>8} | {cost[vertex]:>8} | {previous[vertex]!s:>6}')
  print('-' * 28)
  print(f'{"total":>8} | {sum(cost.values()):>8}')
