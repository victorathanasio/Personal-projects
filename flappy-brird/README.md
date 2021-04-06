# ReadMe coding weeks: Projet des coding weeks 2020-2021 de Flappy BRirds 

## Description

Afin de mettre en pratique les connaissances acquises pendant la première semaine de coding weeks, le projet suivant a été proposé. L'équipe, donc, a recréé en utilisant la package pygame du Python le jeu Flappy Bird, qui a été devenu très célèbre en 2013. 

## Progress
- [x] Setting up Github (**Thales**)
- [x] Sprint 0 ( **L'équipe** )
- [x] Sprint 1 - Fonctionnalité 1 : Créer l'environnement (**Thales**)
- [x] Sprint 1 - Fonctionnalité 2 : Créer la classe Bird (**Yuichi et Thales**)
- [x] Sprint 1 - Fonctionnalité 3 : Créer la classe Ground (**Rafael**)
- [x] Sprint 1 - Fonctionnalité 4 : Créer la classe Pipe (**Victor**)
- [x] Sprint 2 - Fonctionnalité 5 : Créer le design du jeu (**Thales et Victor**)
- [x] Sprint 2 - Fonctionnalité 6 : Créer les animations du oiseau (**Thales et Rafael**)
- [x] Sprint 2 - Fonctionnalité 7 : Ajouter les sons du jeu (**Thales et Victor**)
- [x] Sprint 2 - Fonctionnalité 8 : Ajouter le score du jeu (**Yuichi**)
- [x] Sprint 2 - Fonctionnalité 9 : Developper un menu pour le jeu (**Victor**)
- [x] Sprint 3 - Fonctionnalité 10 : Developper un AI pour jouer (**Thales et Victor**)
- [ ] Sprint 3 - Fonctionnalité 11 : Ajouter de publicité
- [x] Sprint 3 - Fonctionnalité 12 : Ajouter différents difficultées (**Yuichi**)
- [x] Sprint 3 - Fonctionnalité 13 : Ajouter autres themes (**Yuichi**)
- [x] Sprint 3 - Fonctionnalité 14 : Créer le menu de fin de jeu (**Rafael**) 


## Visuals

En plus du MVP et le mode original, il a aussi quelques adaptations qui ont eté implementées pour faire le jeu plus intéressant.

### Themes

#### 1- MVP
![alt text](https://i.imgur.com/kNvjL4i.png)

#### 2- Original

![alt text](https://i.imgur.com/O2V6EB4.png)

#### 3- France

![alt text](https://i.imgur.com/PxRcDZu.png)


#### 4- Brésil

![alt text](https://i.imgur.com/QBwLaZO.png)

#### 5- CS

![alt text](https://i.imgur.com/wwuRwdm.png)

#### 6- Neymar

![alt text](https://i.imgur.com/o2qLlIz.png)


### Modes de jeu
Il y a 5 modes de difficulté dans le jeu: Easy, Normal, Hard, Very Hard, Insane et 'Meme'.

Prise en compte de la difficulté "Normale" comme difficulté par default, les différences de chaque difficulté sont:

Easy : Les tubes sont légèrement plus grands et plus espacés.

Hard : Les tubes se déplacent verticalement, en maintenant une taille d'ouverture fixe.

Very Hard : Les tubes se déplacent verticalement avec des différences de vitesse entre les tubes supérieur et inférieur (la taille de l'ouverture est variable).

Insane : Les tubes se déplacent comment Very Hard, mais ils sont plus rapprochés.

"Meme" : Mode de jeu impossible. Les tubes sont très proches et le jeu tourne à une vitesse 2x plus rapide.

#### Examples du mouvement des tubes
Easy:\
![Easy](https://i.ibb.co/HryYTpH/ezgif-com-gif-maker-7.gif)

Normal:\
![Normal](https://i.ibb.co/xJdpZ92/ezgif-com-gif-maker-6.gif)

Hard:\
![Hard](https://i.ibb.co/FJYsVGk/ezgif-com-gif-maker.gif)

Very Hard:\
![Very Hard](https://i.ibb.co/3BTLHTc/ezgif-com-gif-maker-1.gif)

Insane:\
![Insane](https://i.ibb.co/CM2KRh8/ezgif-com-gif-maker-4.gif)

Meme:\
![Meme](https://i.ibb.co/6nL9w8g/ezgif-com-gif-maker-5.gif)


## Installation
* Python 3.8
* pygame 2.0.0
* pygame-menu 3.3.0
* neat-python 0.92

```bash
pip install -r requirements.txt
```

## Usage

### Pour jouer il faut:

1- Exécutez le fichier main.py \
2- Choisissez la difficulté et le thème et le mode de jeu (Regular, AI ou train AI).\

### Comment Jouer:

1- Utilisez le click gauche pour faire l'oiseau sauter\
2- Passez entre les tubes pour marquer les points \
3- Vous perdez si l'oiseau touche le sol ou un tube\

### Comment entraîner et tester l'IA:

1 - Sélectionnez Train AI dans le menu et cliquez sur PLAY.\
2 - Une fois l'exécution du jeu terminée, le meilleur modèle est enregistré dans AI_models / as winner_ [theme] _ [difficulté]\
3 - Pour tester l'IA entraînée, renommez le fichier en winner.pkl\
Facultatif: Il est possible d'éditer les critères d'arrêt et AI avec le fichier NEAT_config.txt\

## Authors & contributions
* Thales Augusto Souto Rodriguez: Étudiant brésilien en double dîplome. J'étude la génie informátique à l'Université de São Paulo.

* Yuichi Tokumoto: Étudiant brésilien en double dîplome. J'étude la génie industriel à l'Université de São Paulo.

* Rafael Seigi Pinheiro Terashima : Étudiant brésilien en double dîplome. J'étude la génie de procèdes à l'Université de São Paulo.

* Victor Alexandre Candido Athanasio: Étudiant brésilien en double dîplome. J'étude la génie mécatronique à l'Université de São Paulo.


## Testing

Les tests ont été effectués à l'aide de pytest et, au lieu de recevoir des commandes utilisateur, les tests utilisent l'IA déjà entraînée.

![Testing](https://i.ibb.co/bXrSbvX/ezgif-com-gif-maker-3.gif)
![coverage](https://i.imgur.com/qA8WENk.png)

## License
Copyright (c) <2020> <Flappy Brird team>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Presentation

Le lien pour l'enregistrement de le video:

[Coding Weeks - CentraleSupélec - Group17 - defense](https://www.youtube.com/watch?v=2d4sDXg-uuk&feature=youtu.be&ab_channel=VictorAthanasio)

