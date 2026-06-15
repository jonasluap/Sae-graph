# Néonaure - SAÉ Graphes-IHM

## Présentation du projet

Ce projet a été réalisé dans le cadre de la SAÉ Graphes-IHM en BUT Informatique.

L’objectif est de développer une application graphique en Python permettant de jouer au jeu **Néonaure**, une variante du Sudoku basée sur des motifs et des contraintes de voisinage.

L’application utilise **PyQt6** pour l’interface graphique et respecte une architecture **MVC**.

---

## Règles du jeu

Le Néonaure est un jeu de logique sur une grille composée de plusieurs motifs.

Les règles principales sont :

1. Chaque case peut contenir un seul chiffre.
2. Deux cases voisines ne peuvent pas contenir le même chiffre, y compris en diagonale.
3. Un motif composé de `N` cases doit contenir les chiffres de `1` à `N`.
4. Certaines cases sont déjà remplies au départ et ne peuvent pas être modifiées.
5. Les cases remplies par le joueur restent modifiables.

---

## Membres du groupe

* Adel : modèle, chargement et sauvegarde des grilles, résolution, contrôleur principal.
* Henry : composant graphique de la grille, saisie utilisateur, gestion des cases.
* Jonas : fenêtre principale, menus, ergonomie, affichage des motifs et retour visuel des erreurs.

---

## Technologies utilisées

* Python
* PyQt6
* JSON
* Git / GitHub

---

## Architecture du projet

Le projet respecte l’architecture MVC.

### Modèle

Le modèle contient les données et les règles du jeu.

Il gère notamment :

* les cases ;
* les motifs ;
* la grille ;
* les règles de validité ;
* le chargement et la sauvegarde des fichiers JSON ;
* le solveur.

### Vue

La vue correspond à l’interface graphique.

Elle gère notamment :

* la fenêtre principale ;
* le menu principal ;
* l’affichage de la grille ;
* les boutons ;
* le thème sombre / clair ;
* les bordures épaisses des motifs ;
* les cases en erreur.

La vue ne modifie pas directement le modèle. Elle transmet les actions de l’utilisateur au contrôleur.

### Contrôleur

Le contrôleur fait le lien entre le modèle et la vue.

Il reçoit les actions de l’utilisateur, demande au modèle de faire les traitements nécessaires, puis demande à la vue de se mettre à jour.

---

## Fonctionnalités

L’application permet de :

* afficher un menu principal ;
* charger une grille depuis un fichier JSON ;
* afficher une grille adaptée à sa taille réelle ;
* saisir des valeurs dans les cases modifiables ;
* empêcher la saisie de valeurs supérieures à la taille du motif ;
* afficher les cases fixées en gris ;
* afficher les erreurs en rouge ;
* afficher les motifs avec des bordures épaisses ;
* sauvegarder une grille ;
* vérifier une grille ;
* résoudre une grille ;
* réinitialiser une grille ;
* changer entre un mode sombre et un mode clair.

---

## Lancement du projet

Pour lancer l’application, il faut d’abord être à la racine du projet.

Commande :

```bash
python main.py
```

Si plusieurs versions de Python sont installées, il peut être nécessaire d’utiliser :

```bash
python3 main.py
```

ou :

```bash
py main.py
```

---

## Installation des dépendances

Le projet utilise PyQt6.

Pour installer PyQt6 :

```bash
pip install PyQt6
```

---

## Structure du projet

Exemple de structure :

```text
Sae-graph/
│
├── main.py
│
└── src/
    ├── controller/
    │   └── controleur.py
    │
    ├── model/
    │   ├── case.py
    │   ├── grille.py
    │   ├── motif.py
    │   └── solveur.py
    │
    └── view/
        ├── fenetre_principale.py
        └── composant_grille.py
```

---

## Partie réalisée par Jonas

La partie réalisée par Jonas concerne principalement l’interface graphique.

Les éléments réalisés sont :

* création de la fenêtre principale ;
* ajout d’un menu principal ;
* ajout des boutons de navigation ;
* ajout des menus `Fichier`, `Jouer`, `Options` et `Aide` ;
* création d’un thème sombre et d’un thème clair ;
* centrage de la grille dans le plateau de jeu ;
* adaptation de la taille des cases selon la taille de la grille ;
* affichage visuel des motifs avec des bordures épaisses ;
* affichage des erreurs en rouge ;
* blocage visuel des cases fixées ;
* limitation de la saisie selon la taille du motif ;
* connexion de la vue avec le contrôleur.

---

## Gestion des grilles

Les grilles sont chargées depuis des fichiers JSON.

Lorsqu’une grille est chargée :

* les cases existantes sont affichées ;
* les cases fixées sont bloquées ;
* les cases modifiables restent éditables ;
* les motifs sont affichés avec des bordures épaisses ;
* la taille de la grille s’adapte automatiquement au fichier chargé.

---

## Ergonomie

L’interface a été pensée pour être simple à utiliser.

Les choix ergonomiques principaux sont :

* menu principal clair ;
* boutons visibles ;
* grille centrée ;
* cases carrées ;
* couleurs différentes pour les cases fixées et les erreurs ;
* bordures épaisses pour repérer les motifs ;
* messages d’information pour guider l’utilisateur.

---

## Remarques

Certaines fonctionnalités dépendent du modèle et du contrôleur.

Par exemple :

* le chargement réel des fichiers JSON ;
* la sauvegarde ;
* la vérification complète des règles ;
* la résolution automatique.

La vue se contente d’envoyer les actions de l’utilisateur au contrôleur et d’afficher les résultats reçus.
