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


def resoud_tous(probleme: ProblemeTaxi) -> dict[tuple[int, int], SolutionTaxi]:
    """calcule les chemins les plus courts entre tous les couples d'emplacement."""
    resultat = dict()
    for i, depart in enumerate(probleme.emplacements):
        for arrivee in probleme.emplacements[i + 1 :]:
            solution = resoud(probleme=probleme, depart=depart, arrivee=arrivee)
            if solution is not None:
                resultat[(depart, arrivee)] = solution
    return resultat


