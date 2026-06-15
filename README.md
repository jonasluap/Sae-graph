# Néonaure

Projet SAÉ Graphes-IHM — BUT Informatique 2025-2026  
IUT du Littoral Côte d'Opale

**Membres du groupe :** Adel Essalhi · Henry · Jonas

---

## Présentation du jeu

Le Néonaure est une variante du Sudoku jouée sur une grille carrée (8×8) ou rectangulaire.  
La grille est divisée en **motifs** (régions irrégulières délimitées par des bordures épaisses), chaque motif de taille N devant contenir exactement les chiffres **1 à N**.

### Règles

1. **Un chiffre par case.**
2. **Adjacence** : deux cases voisines (y compris en diagonale, 8 directions) ne peuvent pas avoir la même valeur.
3. **Motif** : un motif de N cases doit contenir exactement les chiffres 1 à N, sans doublon.

---

## Prérequis

- Python 3.11+
- PyQt6

```bash
pip install PyQt6
```

---

## Lancement

```bash
python main.py
```

---

## Utilisation

1. **Charger une grille** — Menu *Fichier → Charger* ou bouton **Charger** dans l'écran de jeu. Sélectionner un fichier `.json` depuis le dossier `Exemples de grille-20260609/`.
2. **Jouer** — Cliquer sur une case libre et saisir un chiffre. Seules les valeurs valides pour le motif (1 à N) sont acceptées. Les cases en conflit passent en rouge automatiquement.
3. **Vérifier** — Le bouton **Vérifier** indique si la grille est correcte, incomplète ou en erreur.
4. **Résoudre** — Le bouton **Résoudre** lance l'algorithme de backtracking et affiche la solution.
5. **Réinitialiser** — Efface toutes les valeurs saisies et repart de l'état initial.
6. **Sauvegarder** — Enregistre l'état courant de la grille au format JSON.

---

## Architecture MVC

```
src/
├── model/
│   ├── case.py       # Une case : position, valeur, état fixé/libre
│   ├── motif.py      # Un motif : groupe de cases, validation 1..N
│   ├── grille.py     # La grille : chargement JSON, voisinage, validation
│   └── solveur.py    # Algorithme de résolution par backtracking
├── view/
│   ├── fenetre_principale.py   # Fenêtre principale, menus, callbacks
│   └── composant_grille.py     # Grille visuelle, cases colorées par motif
├── controller/
│   └── controleur.py  # Lien entre vue et modèle via callbacks
└── utils/
tests/
├── test_case.py
├── test_motif.py
├── test_grille.py
└── test_controleur.py
```

**Principe :**
- La **vue** ne manipule jamais le modèle directement.
- Le **modèle** ne connaît pas la vue.
- Le **contrôleur** reçoit les actions de la vue, met à jour le modèle et notifie la vue via des callbacks.

---

## Algorithme de résolution

Le solveur utilise un **backtracking récursif** :

1. Trouver la première case vide.
2. Essayer chaque valeur de 1 à N (N = taille du motif de cette case).
3. Vérifier que la valeur ne crée pas de conflit (adjacence + motif).
4. Si valide, placer la valeur et continuer récursivement.
5. Si aucune valeur ne fonctionne, revenir en arrière (*backtrack*).

---

## Format des grilles JSON

```json
{
  "motif1": [[col, ligne, valeur], ...],
  "motif2": [[col, ligne, valeur], ...],
  ...
}
```

- `col` : position horizontale (commence à 0)
- `ligne` : position verticale (commence à 0)
- `valeur` : chiffre pré-rempli, **0 = case vide**

Les dimensions de la grille sont déduites automatiquement (max col + 1, max ligne + 1).

---

## Lancer les tests

```bash
python -m pytest tests/
```
