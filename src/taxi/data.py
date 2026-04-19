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