"""Description.

description du problème de trajets dans la ville.
"""

from pydantic import BaseModel, PositiveInt, model_validator
from typing_extensions import Self


class Route(BaseModel):
    depart: PositiveInt
    arrivee: PositiveInt
    duree: PositiveInt

    @model_validator(mode="after")
    def verifie_boucle(self) -> Self:
        """on regarde si la route relie deux sommets distincts."""
        if self.depart == self.arrivee:
            msg = "Une route doit relier deux emplacements distincts"
            raise ValueError(msg)
        return self


class ProblemeTaxi(BaseModel):
    emplacements: list[PositiveInt]
    routes: list[Route]

    @model_validator(mode="after")
    def verifie_emplacements_distincts(self) -> Self:
        if len(set(self.emplacements)) != len(self.emplacements):
            msg = "Les emplacements doivent être distincts"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def verifie_routes_valides(self) -> Self:
        emplacements_valides = set(self.emplacements)
        for route in self.routes:
            if route.depart not in emplacements_valides:
                msg = "Le départ d'une route doit être un emplacement valide"
                raise ValueError(msg)
            if route.arrivee not in emplacements_valides:
                msg = "L'arrivée d'une route doit être un emplacement valide"
                raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def verifie_absence_doublons(self) -> Self:
        """montre si une route n'est pas présente deux fois."""
        deja_vues = set()
        for route in self.routes:
            cle = tuple(sorted((route.depart, route.arrivee)))
            if cle in deja_vues:
                msg = "Deux routes ne peuvent pas relier les mêmes emplacements"
                raise ValueError(msg)
            deja_vues.add(cle)
        return self


class SolutionTaxi(BaseModel):
    chemin: list[PositiveInt]
    duree_totale: PositiveInt


def probleme_exemple() -> ProblemeTaxi:
    """la fonction construit le probleme de l'énoncé."""
    return ProblemeTaxi(
        emplacements=list(range(1, 17)),
        routes=[
            Route(depart=1, arrivee=2, duree=5),
            Route(depart=1, arrivee=3, duree=9),
            Route(depart=1, arrivee=4, duree=4),
            Route(depart=2, arrivee=5, duree=3),
            Route(depart=2, arrivee=6, duree=2),
            Route(depart=3, arrivee=4, duree=4),
            Route(depart=3, arrivee=6, duree=1),
            Route(depart=4, arrivee=7, duree=7),
            Route(depart=5, arrivee=8, duree=4),
            Route(depart=5, arrivee=9, duree=2),
            Route(depart=5, arrivee=10, duree=9),
            Route(depart=6, arrivee=7, duree=3),
            Route(depart=6, arrivee=10, duree=9),
            Route(depart=6, arrivee=11, duree=6),
            Route(depart=7, arrivee=11, duree=8),
            Route(depart=7, arrivee=15, duree=5),
            Route(depart=8, arrivee=12, duree=5),
            Route(depart=9, arrivee=8, duree=3),
            Route(depart=9, arrivee=13, duree=10),
            Route(depart=10, arrivee=9, duree=6),
            Route(depart=10, arrivee=13, duree=5),
            Route(depart=10, arrivee=14, duree=1),
            Route(depart=11, arrivee=14, duree=2),
            Route(depart=12, arrivee=16, duree=9),
            Route(depart=13, arrivee=12, duree=4),
            Route(depart=13, arrivee=14, duree=3),
            Route(depart=14, arrivee=16, duree=4),
            Route(depart=15, arrivee=14, duree=4),
            Route(depart=15, arrivee=16, duree=3),
        ],
    )