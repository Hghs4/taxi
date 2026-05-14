"""resolution du problème de trajet de taxi."""

import networkx as nx

from taxi.data import ProblemeTaxi, SolutionTaxi, Route


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


def modifie_route(
    probleme: ProblemeTaxi,
    sommet_1: int,
    sommet_2: int,
    nouvelle_duree: int,
) -> ProblemeTaxi:
    """Renvoie un nouveau problème avec une durée modifiée pour une route."""
    nouvelles_routes = []
    for route in probleme.routes:
        if {route.depart, route.arrivee} == {sommet_1, sommet_2}:
            nouvelles_routes.append(
                Route(
                    depart=route.depart,
                    arrivee=route.arrivee,
                    duree=nouvelle_duree,
                )
            )
        else:
            nouvelles_routes.append(route)
    return ProblemeTaxi(
        emplacements=probleme.emplacements,
        routes=nouvelles_routes,
    )


def etudie_impact_route(
    probleme: ProblemeTaxi,
    depart: int,
    arrivee: int,
    sommet_1: int,
    sommet_2: int,
    durees: list[int],
) -> dict[int, SolutionTaxi | None]:
    """impact de plusieurs durées possibles pour une route."""
    resultat = dict()
    for duree in durees:
        probleme_modifie = modifie_route(
            probleme=probleme,
            sommet_1=sommet_1,
            sommet_2=sommet_2,
            nouvelle_duree=duree,
        )
        resultat[duree] = resoud(
            probleme=probleme_modifie,
            depart=depart,
            arrivee=arrivee,
        )
    return resultat


def resoud_avec_travaux(
    probleme: ProblemeTaxi,
    depart: int,
    arrivee: int,
    sommets_en_travaux: list[int],
    penalite: int,
) -> SolutionTaxi | None:
    """resout le problème avec une pénalité de passage sur certains sommets."""
    graphe = nx.DiGraph()

    for sommet in probleme.emplacements:
        graphe.add_edge(
            (sommet, "entree"),
            (sommet, "sortie"),
            duree=penalite if sommet in sommets_en_travaux else 0,
        )

    for route in probleme.routes:
        graphe.add_edge(
            (route.depart, "sortie"),
            (route.arrivee, "entree"),
            duree=route.duree,
        )
        graphe.add_edge(
            (route.arrivee, "sortie"),
            (route.depart, "entree"),
            duree=route.duree,
        )

    try:
        chemin_etendu = nx.shortest_path(
            G=graphe,
            source=(depart, "sortie"),
            target=(arrivee, "entree"),
            weight="duree",
        )
        duree_totale = nx.shortest_path_length(
            G=graphe,
            source=(depart, "sortie"),
            target=(arrivee, "entree"),
            weight="duree",
        )
    except nx.NetworkXException:
        return None

    chemin = [sommet for sommet, position in chemin_etendu if position == "entree"]
    chemin.insert(0, depart)

    return SolutionTaxi(
        chemin=chemin,
        duree_totale=duree_totale,
    )