"""Description.

tests pour le module data.py
"""

import pytest
from pydantic import ValidationError

from taxi.data import ProblemeTaxi, Route, SolutionTaxi, probleme_exemple


def test_route_boucle():
    with pytest.raises(ValidationError):
        Route(depart=1, arrivee=1, duree=5)


def test_probleme_emplacements_distincts():
    with pytest.raises(ValidationError):
        ProblemeTaxi(
            emplacements=[1, 2, 2],
            routes=[],
        )


def test_probleme_routes_valides_depart():
    with pytest.raises(ValidationError):
        ProblemeTaxi(
            emplacements=[1, 2, 3],
            routes=[Route(depart=4, arrivee=2, duree=5)],
        )


def test_probleme_routes_valides_arrivee():
    with pytest.raises(ValidationError):
        ProblemeTaxi(
            emplacements=[1, 2, 3],
            routes=[Route(depart=1, arrivee=4, duree=5)],
        )


def test_probleme_routes_sans_doublon():
    with pytest.raises(ValidationError):
        ProblemeTaxi(
            emplacements=[1, 2, 3],
            routes=[
                Route(depart=1, arrivee=2, duree=5),
                Route(depart=2, arrivee=1, duree=7),
            ],
        )


def test_solution_taxi():
    solution = SolutionTaxi(chemin=[1, 4, 10], duree_totale=5)
    assert solution.chemin == [1, 4, 10]
    assert solution.duree_totale == 5


def test_probleme_exemple():
    probleme = probleme_exemple()
    assert len(probleme.emplacements) == 16
    assert len(probleme.routes) == 29