import networkx as nx
from heuristic_gcp import *


def parse_line(line): 
    if line.startswith(TYPE_COMMENT):
        return TYPE_COMMENT, None
    elif line.startswith(TYPE_PROBLEM_LINE):
        _, _, num_nodes, num_edges = line.split(' ')
        return TYPE_PROBLEM_LINE, (int(num_nodes), int(num_edges))
    elif line.startswith(TYPE_EDGE_DESCRIPTOR):
        _, node1, node2 = line.split(' ')
        return TYPE_EDGE_DESCRIPTOR, (int(node1), int(node2))
    else:
        raise ValueError(f"Unable to parse '{line}'")


def from_file(filename): #Contruit la matrice d'adjacence à partir des fichiers fournis
        matrice = None
        with open(filename) as f:
            problem_set = False
            for line in f.readlines():
                line_type, val = parse_line(line.strip())
                if line_type == TYPE_COMMENT:
                    continue
                elif line_type == TYPE_PROBLEM_LINE and not problem_set:
                    num_nodes, num_edges = val
                    matrice = [ [0 for _ in range(num_nodes)] for _ in range(num_nodes) ]
                    problem_set = True
                elif line_type == TYPE_EDGE_DESCRIPTOR:
                    if not problem_set:
                        raise RuntimeError("Edge descriptor found before problem line")
                    node1, node2 = val
                    matrice[node1-1][node2-1] = 1
                    matrice[node2-1][node1-1] = 1
        return matrice

def defineGraph(filename):

    """
    graph = nx.Graph()
    add_nodes_from([1, 2, 3, 4])
    add_edges_from([
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 3),
        (2, 4),
        (3, 1),
        (3, 2),
        (3, 4),
        (4, 1),
        (4, 2),
        (4, 3)
    ])
    """
    graph = nx.from_numpy_matrix(np.array(from_file(filename)))
    return graph

matrice = [] #Contient la matrice d'adjacence

SUBPLOT_NUM = 211
TYPE_COMMENT = "c"
TYPE_PROBLEM_LINE = "p"
TYPE_EDGE_DESCRIPTOR = "e"


dataset = input("Entrer le nom du dataset: ")
graph = defineGraph(dataset)
print(graph)
start = time.time()
coloring, nb_colors = GraphColoring(graph)
end = time.time()
print("Temps d'execution = ", (end-start)*1000," milliseconds")
print(coloring)
print("Le nombre de couleurs utilisé est = ", nb_colors)
#nx.draw_networkx(graph,node_color=coloring, with_labels=True)
nx.draw_circular(graph, font_weight="bold", node_color = coloring, with_labels=True, vmin=0, vmax=max(coloring))
plt.show()