# Projet Taxi : Recherche de plus courts chemins

## Description

Ce projet modélise un réseau routier utilisé par une compagnie de taxi.  

L’objectif est de déterminer les plus courts chemins entre différents sommets d’un graphe pondéré représentant les routes et leurs durées de trajet.

Le projet contient :
- la modélisation des données,
- la construction du graphe,
- les algorithmes de résolution,
- des tests unitaires,
- un dashboard interactif réalisé avec Marimo.

---

## Technologies utilisées

- Python 3.13
- uv
- networkx
- matplotlib
- marimo
- pytest

---

## Structure du projet

```text
taxi/
│
├── src/
│   └── taxi/
│       ├── __init__.py
│       ├── cli.py
│       ├── data.py
│       ├── resolution.py
│       └── visualisation.py
│
├── tests/
│   ├── test_data.py
│   └── test_resolution.py
│
├── notebook.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Hghs4/taxi.git
cd taxi
```

### 2. Installer les dépendances

```bash
uv sync
```

---

## Lancer les tests

```bash
PYTHONPATH=src uv run pytest
```

---

## Lancer le dashboard

```bash
PYTHONPATH=src uv run marimo run notebook.py
```

Puis ouvrir le lien affiché dans le terminal.

---

## Fonctionnalités du dashboard

Le dashboard permet :

- d’afficher le réseau routier,
- de visualiser le plus court chemin,
- de modifier les sommets de départ et d’arrivée,
- d’étudier l’impact de la route 9-13,
- de simuler des travaux sur certaines routes,
- d’afficher tous les plus courts chemins.

---

## Questions traitées

### Question 1
Recherche du plus court chemin entre deux sommets.

### Question 2
Calcul de tous les plus courts chemins du graphe.

### Question 3
Étude de l’impact de la route 9-13 sur les trajets.

### Question 4
Simulation de travaux avec pénalités de durée.

---

## Auteurs

Projet réalisé par :

- Hugo
- Vikrant