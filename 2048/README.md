# Projet des coding weeks 2020-2021 de PT-BR Team

## Description
Pour se familiariser avec des différents packages des Python et avec des méthodologies de Clean Code, TDD et MVP, ce projet a été créé. Le but c'était de créer le jeu mobile 2048 dans l'ambiance du Python.

### This is the 2048 game project of the first week of the CS Coding Weeks.

## Members
* Thales Augusto Souto Rodriguez: Étudiant brésilien en double dîplome. J'étude la génie informátique à l'Université de São Paulo.

* Yuichi Tokumoto: Étudiant brésilien en double dîplome. J'étude la génie industriel à l'Université de São Paulo.


* Rafael Seigi Pinheiro Terashima : Étudiant brésilien en double dîplome. J'étude la génie de procèdes à l'Université de São Paulo.

* Victor Alexandre Candido Athanasio: Étudiant brésilien en double dîplome. J'étude la génie mécatronique à l'Université de São Paulo.


## Installation
* Python 3.8
* NumPy 1.13.3 (seulement pour le optimized.py)
* Pandas 1.0.1


## Progress
- [x] Setting up Github
- [x] Sprint 0
- [x] Sprint 1 - Fonctionnalité 1 : Représenter la grille de jeu
- [x] Sprint 1 - Fonctionnalité 2 : Afficher la grille de jeu
- [x] Sprint 2 - Fonctionnalité 3 : Faire jouer le joueur
- [x] Sprint 3 - Fonctionnalité 4 : Gestion des déplacements
- [x] Sprint 3 - Fonctionnalité 5 : Tester la fin du jeu.
- [x] Sprint 4 - Fonctionnalité 6 : Mettre en orchestre le jeu
- [x] Conclusion du objectif 1
- [x] Objectif 2


## Usage

Pour jouer la version MVP (textuelle , il faut:
1) Executer le fichier main.py avec un argument "textual"
2) Choisir le taille e le theme comme indique
3) La grille du joue será creé et vous pouvez commencer a faire les mouvements

Example de la version MVP:
```bash
Entrez le thème (0 (Default), 1 (Chemistry), 2 (Alphabet):0

Entrez la taille de la grille (minimum 3):4
 === === === ===
|   |   |   | 2 |
 === === === ===
| 2 |   |   |   |
 === === === ===
|   |   |   |   |
 === === === ===
|   |   |   |   |
 === === === ===

Entrez votre commande (a (gauche), d (droite), w (haut), s (bas)):
```
Pour jouer la version finale, il faut:
1) Ouvrir et executer le fichier main.py ( sans aucun argument)  il lancera le jeux avec les régales normales
2) On peut choisissez le theme, la taille et les autres opitions dans les menus au dessus (File, Grid_size et Theme)
3) Jouez 


## Detailed updates


Nous avons bien terminé les fonctions de la fonctionnalité 1 et elles fonctionnent comme prévu. Certaines des fonctions comme create_grid ont un paramètre d'entrée default pour convenir à plusieurs tests simultanément.<br/>
```bash
def create_grid(n=4):
    grid = []
    for i in range(n):
        grid.append([' ' for j in range(n)])
    return grid
```

Pour la fonctionnalité 2, nous avons légèrement modifié le style de create_grid_with_size_theme () pour centrer le texte et paraître un peu plus beau.<br/>
```bash
 ==== ==== ==== ====
|    |    |    | H  |
 ==== ==== ==== ====
|    |    |    |    |
 ==== ==== ==== ====
|    |    |    |    |
 ==== ==== ==== ====
| He |    |    |    |
 ==== ==== ==== ====
 ```


Vous trouverez ci-dessous une image de la façon dont le monkeypatch pour la fonctionnalité 3 a été implémenté, afin de tester des inputs prédéfinies.<br/>
```
def test_read_theme_grid(monkeypatch):
    responses = iter(['d', 'g','0', '1', '2','no','yess','11', '0','1','no'])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert read_theme_grid() == "0"
    ...
```
En parallèle au development du MVP, on a aussi developpé un code qui utilise d'autres packages pour construire le jeu (more_optimized.py). Avec cette autre code, on a pu adapter l'interface graphique du jeu pour construire les fonctionnalités qui on été demandé dans l'Objectif 2.<br/>

![gif project ](https://s8.gifyu.com/images/UsageExample.gif)<br/>
