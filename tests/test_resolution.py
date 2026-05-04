import networkx as nx

from taxi.data import ProblemeTaxi, Route
from taxi.resolution import construit_graphe, resoud


def test_construction_simple():
    probleme = ProblemeTaxi(
        emplacements=[1, 2],
        routes=[Route(depart=1, arrivee=2, duree=5)],
    )
    calcule = construit_graphe(probleme=probleme)

    attendu = nx.Graph()
    attendu.add_edge(1, 2, duree=5)

    assert nx.utils.graphs_equal(calcule, attendu)


def test_resolution_simple():
    probleme = ProblemeTaxi(
        emplacements=[1, 2, 3],
        routes=[
            Route(depart=1, arrivee=2, duree=5),
            Route(depart=2, arrivee=3, duree=2),
            Route(depart=1, arrivee=3, duree=10),
        ],
    )
    resultat = resoud(probleme=probleme, depart=1, arrivee=3)

    assert resultat is not None
    assert resultat.chemin == [1, 2, 3]
    assert resultat.duree_totale == 7


def test_resolution_impossible():
    probleme = ProblemeTaxi(
        emplacements=[1, 2, 3],
        routes=[Route(depart=1, arrivee=2, duree=5)],
    )
    resultat = resoud(probleme=probleme, depart=1, arrivee=3)

    assert resultat is None