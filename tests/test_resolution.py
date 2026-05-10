import networkx as nx

from taxi.data import ProblemeTaxi, Route, probleme_exemple
from taxi.resolution import (
    construit_graphe,
    resoud,
    resoud_tous,
    modifie_route,
    etudie_impact_route,
)

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


def test_resolution_sujet():
    probleme = probleme_exemple()
    resultat = resoud(probleme=probleme, depart=1, arrivee=16)

    assert resultat is not None
    assert resultat.chemin == [1, 2, 6, 7, 15, 16]
    assert resultat.duree_totale == 18


def test_resolution_tous():
    probleme = ProblemeTaxi(
        emplacements=[1, 2, 3],
        routes=[
            Route(depart=1, arrivee=2, duree=5),
            Route(depart=2, arrivee=3, duree=2),
            Route(depart=1, arrivee=3, duree=10),
        ],
    )
    resultat = resoud_tous(probleme=probleme)

    assert resultat[(1, 2)].chemin == [1, 2]
    assert resultat[(1, 2)].duree_totale == 5
    assert resultat[(1, 3)].chemin == [1, 2, 3]
    assert resultat[(1, 3)].duree_totale == 7
    assert resultat[(2, 3)].chemin == [2, 3]
    assert resultat[(2, 3)].duree_totale == 2


def test_modifie_route():
    probleme = ProblemeTaxi(
        emplacements=[1, 2, 3],
        routes=[
            Route(depart=1, arrivee=2, duree=5),
            Route(depart=2, arrivee=3, duree=2),
        ],
    )
    modifie = modifie_route(
        probleme=probleme,
        sommet_1=1,
        sommet_2=2,
        nouvelle_duree=8,
    )

    resultat = resoud(probleme=modifie, depart=1, arrivee=3)

    assert resultat is not None
    assert resultat.chemin == [1, 2, 3]
    assert resultat.duree_totale == 10


def test_impact_route():
    probleme = ProblemeTaxi(
        emplacements=[1, 2, 3],
        routes=[
            Route(depart=1, arrivee=2, duree=5),
            Route(depart=2, arrivee=3, duree=2),
            Route(depart=1, arrivee=3, duree=10),
        ],
    )
    resultat = etudie_impact_route(
        probleme=probleme,
        depart=1,
        arrivee=3,
        sommet_1=2,
        sommet_2=3,
        durees=[1, 10],
    )

    assert resultat[1] is not None
    assert resultat[1].chemin == [1, 2, 3]
    assert resultat[1].duree_totale == 6

    assert resultat[10] is not None
    assert resultat[10].chemin == [1, 3]
    assert resultat[10].duree_totale == 10