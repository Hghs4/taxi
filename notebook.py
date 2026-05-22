import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import networkx as nx

    from taxi.data import probleme_exemple
    from taxi.resolution import (
        construit_graphe,
        modifie_route,
        resoud,
        resoud_avec_travaux,
        resoud_tous,
    )

    return construit_graphe, mo, modifie_route, nx, plt, probleme_exemple, resoud, resoud_avec_travaux, resoud_tous


@app.cell
def _(mo):
    mo.md("#  Compagnie de Taxi")
    return


@app.cell
def _(mo):
    question = mo.ui.radio(
        options=[
            "Question 1",
            "Question 2",
            "Question 3",
            "Question 4",
        ],
        value="Question 1",
        label="Choisir une question",
        inline=True,
    )

    question
    return (question,)


@app.cell
def _(probleme_exemple):
    probleme = probleme_exemple()
    emplacements = probleme.emplacements
    return emplacements, probleme


@app.cell
def _(emplacements, mo, question):
    if question.value in ["Question 3", "Question 4"]:
        depart = mo.ui.dropdown(options=emplacements, value=1, label="Départ")
        arrivee = mo.ui.dropdown(options=emplacements, value=16, label="Arrivée")
        controles_trajet = mo.hstack([depart, arrivee])
    else:
        depart = None
        arrivee = None
        controles_trajet = mo.md("")

    controles_trajet
    return arrivee, depart


@app.cell
def _(mo, question):
    if question.value == "Question 3":
        duree_9_13 = mo.ui.slider(
            start=1,
            stop=25,
            step=1,
            value=10,
            label="Durée de la route 9-13",
        )
        affichage_slider = duree_9_13
    else:
        duree_9_13 = None
        affichage_slider = mo.md("")

    affichage_slider
    return (duree_9_13,)


@app.cell
def _(
    arrivee,
    depart,
    duree_9_13,
    modifie_route,
    probleme,
    question,
    resoud,
    resoud_avec_travaux,
):
    probleme_affiche = probleme
    solution = None

    if question.value == "Question 1":
        solution = resoud(probleme=probleme, depart=1, arrivee=16)

    elif question.value == "Question 3":
        probleme_affiche = modifie_route(
            probleme=probleme,
            sommet_1=9,
            sommet_2=13,
            nouvelle_duree=duree_9_13.value,
        )
        solution = resoud(
            probleme=probleme_affiche,
            depart=depart.value,
            arrivee=arrivee.value,
        )

    elif question.value == "Question 4":
        solution = resoud_avec_travaux(
            probleme=probleme,
            depart=depart.value,
            arrivee=arrivee.value,
            sommets_en_travaux=[3, 5, 7, 9, 11],
            penalite=1,
        )

    return probleme_affiche, solution


@app.cell
def _(mo, probleme, question, resoud_tous):
    if question.value == "Question 2":
        solutions = resoud_tous(probleme)

        lignes = []
        for (_depart, _arrivee), _solution in solutions.items():
            _chemin = " → ".join(map(str, _solution.chemin))
            lignes.append(
                f"| {_depart} | {_arrivee} | {_chemin} | {_solution.duree_totale} min |"
            )

        tableau = "\n".join(lignes)

        affichage_q2 = mo.md(
            f"""
## Question 2 - Tous les plus courts chemins entre les points de la ville

| Départ | Arrivée | Chemin optimal | Durée |
|---:|---:|---|---:|
{tableau}
"""
        )
    else:
        affichage_q2 = mo.md("")

    affichage_q2
    return


@app.cell
def _(duree_9_13, mo, question, solution):
    if question.value == "Question 2":
        affichage_resultat = mo.md("")

    elif solution is None:
        affichage_resultat = mo.md("Aucun chemin trouvé.")

    else:
        if question.value == "Question 1":
            titre = "Question 1 - Plus court chemin de 1 vers 16"
        elif question.value == "Question 3":
            titre = "Question 3 - Impact de la route 9-13"
        else:
            titre = "Question 4 - Travaux"

        texte = f"""
## {titre}

**Chemin optimal :** {" → ".join(map(str, solution.chemin))}

**Durée totale :** {solution.duree_totale} minutes
"""

        if question.value == "Question 3":
            texte += f"""

**Durée actuelle de la route 9-13 :** {duree_9_13.value} minutes
"""

        if question.value == "Question 4":
            texte += """

**Sommets en travaux :** 3, 5, 7, 9 et 11  
**Pénalité :** +1 minute à chaque passage
"""

        affichage_resultat = mo.md(texte)

    affichage_resultat
    return


@app.cell
def _(construit_graphe, mo, nx, plt, probleme_affiche, question, solution):
    if question.value == "Question 2":
        affichage_graphe = mo.md("")

    else:
        graphe = construit_graphe(probleme_affiche)

        positions = {
            1: (0, 3), 2: (1, 4), 3: (1, 2), 4: (1, 0),
            5: (3, 5), 6: (3, 3), 7: (3, 1),
            8: (5, 5), 9: (5, 3), 10: (5, 1), 11: (5, -1),
            12: (7, 4), 13: (7, 2), 14: (7, 0), 15: (7, -2),
            16: (9, 1),
        }

        fig, ax = plt.subplots(figsize=(12, 7))

        nx.draw_networkx_nodes(
            graphe,
            positions,
            node_size=1200,
            node_color="lightblue",
            edgecolors="black",
            ax=ax,
        )

        nx.draw_networkx_edges(
            graphe,
            positions,
            width=2,
            edge_color="gray",
            ax=ax,
        )

        if question.value == "Question 3":
            nx.draw_networkx_edges(
                graphe,
                positions,
                edgelist=[(9, 13)],
                width=5,
                edge_color="purple",
                ax=ax,
            )

        if question.value == "Question 4":
            nx.draw_networkx_nodes(
                graphe,
                positions,
                nodelist=[3, 5, 7, 9, 11],
                node_size=1400,
                node_color="red",
                edgecolors="black",
                ax=ax,
            )

        if solution is not None:
            chemin_edges = list(zip(solution.chemin[:-1], solution.chemin[1:]))

            nx.draw_networkx_edges(
                graphe,
                positions,
                edgelist=chemin_edges,
                width=5,
                edge_color="orange",
                ax=ax,
            )

            nx.draw_networkx_nodes(
                graphe,
                positions,
                nodelist=solution.chemin,
                node_size=1300,
                node_color="yellow",
                edgecolors="black",
                ax=ax,
            )

        nx.draw_networkx_labels(
            graphe,
            positions,
            font_size=12,
            font_weight="bold",
            ax=ax,
        )

        nx.draw_networkx_edge_labels(
            graphe,
            positions,
            edge_labels={(u, v): d for u, v, d in graphe.edges(data="duree")},
            font_size=10,
            ax=ax,
        )

        ax.set_title(question.value, fontsize=18, pad=20)
        ax.axis("off")

        affichage_graphe = mo.mpl.interactive(fig)

    affichage_graphe
    return


if __name__ == "__main__":
    app.run()