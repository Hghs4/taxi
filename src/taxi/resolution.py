"""resolution du problème de trajet de taxi."""

import networkx as nx

from taxi.data import ProblemeTaxi, SolutionTaxi


def construit_graphe(probleme: ProblemeTaxi) -> nx.Graph:
    resultat = nx.Graph()
    for route in probleme.routes:
        resultat.add_edge(route.depart, route.arrivee, duree=route.duree)
    return resultat


def resoud(probleme: ProblemeTaxi, depart: int, arrivee: int) -> SolutionTaxi | None:
    graphe = construit_graphe(probleme=probleme)
    try:
        chemin = nx.shortest_path(
            G=graphe,
            source=depart,
            target=arrivee,
            weight="duree",
        )
        duree_totale = nx.shortest_path_length(
            G=graphe,
            source=depart,
            target=arrivee,
            weight="duree",
        )
    except nx.NetworkXException:
        return None

    return SolutionTaxi(
        chemin=chemin,
        duree_totale=duree_totale,
    )