import networkx as nx

from taxi.data import ProblemeTaxi, Route
from taxi.resolution import construit_graphe


def test_construction_simple():
    probleme = ProblemeTaxi(
        emplacements=[1, 2],
        routes=[Route(depart=1, arrivee=2, duree=5)],
    )
    calcule = construit_graphe(probleme=probleme)

    attendu = nx.Graph()
    attendu.add_edge(1, 2, duree=5)

    assert nx.utils.graphs_equal(calcule, attendu)