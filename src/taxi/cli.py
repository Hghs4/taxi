"""interface en ligne"""

import typer

from taxi.data import probleme_exemple
from taxi.resolution import (
    etudie_impact_route,
    resoud,
    resoud_avec_travaux,
    resoud_tous,
)

app = typer.Typer()


@app.command()
def question1():
    probleme = probleme_exemple()
    solution = resoud(probleme=probleme, depart=1, arrivee=16)
    typer.echo(solution)


@app.command()
def question2():
    probleme = probleme_exemple()
    solutions = resoud_tous(probleme=probleme)
    for cle, solution in solutions.items():
        typer.echo(f"{cle}: {solution}")


@app.command()
def question3():
    probleme = probleme_exemple()
    resultats = etudie_impact_route(
        probleme=probleme,
        depart=1,
        arrivee=16,
        sommet_1=9,
        sommet_2=13,
        durees=[2, 5, 10, 15, 20],
    )
    for duree, solution in resultats.items():
        typer.echo(f"{duree}: {solution}")


@app.command()
def question4():
    probleme = probleme_exemple()
    solution = resoud_avec_travaux(
        probleme=probleme,
        depart=1,
        arrivee=16,
        sommets_en_travaux=[3, 5, 7, 9, 11],
        penalite=1,
    )
    typer.echo(solution)


if __name__ == "__main__":
    app()