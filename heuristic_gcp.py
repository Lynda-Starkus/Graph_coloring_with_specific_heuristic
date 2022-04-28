"""
Heuristique spécifique pour le problème de coloration des graphes par le max stable
"""
from collections import defaultdict, deque
import itertools
import random

import networkx as nx
from networkx.utils import arbitrary_element
from networkx.utils import py_random_state
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import colors

colors_option = []
for color_name in colors.CSS4_COLORS:
    colors_option.append(color_name)
random.shuffle(colors_option)

#Extraire le plus grand stable de G

"""
    Retourne un max stable sous-graphe de G, en choisissant à chaque itération de la boucle 
    while le sommet de degré minimal
"""
def _maximal_independent_set(G):
    result = set()
    #Initiailiser le graph restant à G
    remaining = set(G)
    #Pour tout noeud dans le graph restant
    while remaining:
        #Choisir le noeud avec le degré min (pour éviter la suppression de beaucoup de noeuds)
        G = G.subgraph(remaining)
        v = min(remaining, key=G.degree)

        #Ajouter le noeud v au stable 
        result.add(v)
        #Enlever le noeud v du Graph ainsi que ses voisins 
        remaining -= set(G[v]) | {v}
    return result

"""
    Cet fonction permet d'appeler la procédure d'extraction du max-indep-set (stable maximal) 
    et soustrait l'ensemble du graphe de base, 
"""
def strategy_independent_set(G, colors):
    remaining_nodes = set(G)
    while len(remaining_nodes) > 0:
        nodes = _maximal_independent_set(G.subgraph(remaining_nodes))
        remaining_nodes -= nodes
        yield from nodes
    return nodes

def GraphColoring(G):
    colored_graph = G
    if len(G) == 0:
        return {}
    colors = {}
    nodes = strategy_independent_set(G, colors)
    for u in nodes:
        # Ensemble des voisins du noeud courant 
        neighbour_colors = {colors[v] for v in G[u] if v in colors}
        # Trouver la première couleur non utilisé
        for color in itertools.count():
            if color not in neighbour_colors:
                break
        # Donner la couleur au noeud courant 
        colors[u] = color

    color_map = []
    for node in colored_graph:
        color_map.append(colors_option[colors[node]])

    colors_used = set(color_map)
    return color_map, len(colors_used)


