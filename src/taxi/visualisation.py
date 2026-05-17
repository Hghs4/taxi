"""representation sous forme de graphqiue du probleme de taxi."""

import matplotlib.pyplot as plt
import networkx as nx

from taxi.data import ProblemeTaxi
from taxi.resolution import construit_graphe


def affiche_graphe(probleme: ProblemeTaxi):
    graphe = construit_graphe(probleme=probleme)
    positions = nx.spring_layout(graphe, seed=1)

    nx.draw_networkx_nodes(graphe, pos=positions)
    nx.draw_networkx_edges(graphe, pos=positions)
    nx.draw_networkx_labels(graphe, pos=positions)
    nx.draw_networkx_edge_labels(
        graphe,
        pos=positions,
        edge_labels={
            (depart, arrivee): duree
            for depart, arrivee, duree in graphe.edges(data="duree")
        },
    )

    plt.show()