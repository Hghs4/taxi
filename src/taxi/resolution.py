"""Fonctions de visualisation du graphe de taxi."""

import networkx as nx

from taxi.data import ProblemeTaxi


def construit_graphe(probleme: ProblemeTaxi) -> nx.Graph:
    resultat = nx.Graph()
    for route in probleme.routes:
        resultat.add_edge(route.depart, route.arrivee, duree=route.duree)
    return resultat