# Contexte SAÉ Graphes-IHM — Instructions pour Claude Code

## Qui je suis

Je m'appelle Adel. Je travaille en groupe de 3 (Adel, Henry, Jonas) sur une SAÉ universitaire (IUT Littoral Côte d'Opale, BUT Informatique, 2025-2026). Ce fichier contient tout ce dont tu as besoin pour m'aider à coder ma partie du projet.

---

## Le jeu : Néonaure

C'est une variante du Sudoku. La grille (carrée 64 cases ou rectangulaire) doit être remplie avec des chiffres selon 3 règles :

1. **Un chiffre par case**
2. **Chaque chiffre doit être entouré de chiffres différents, y compris en diagonale** (contrainte d'adjacence 8 directions)
3. **Un motif de N cases (délimité par des bordures épaisses) doit contenir tous les chiffres de 1 à N**

Les motifs sont des groupes de cases irréguliers (comme les régions dans Killer Sudoku), pas des lignes/colonnes classiques.

---

## Format JSON des grilles (format réel fourni par les profs)

```json
{
  "motif1": [[col, ligne, valeur], [col, ligne, valeur], ...],
  "motif2": [[col, ligne, valeur], ...],
  ...
}
```

**Chaque case est un tableau `[col, ligne, valeur]`** :
- `col` = position horizontale (x), commence à 0
- `ligne` = position verticale (y), commence à 0
- `valeur` = chiffre pré-rempli, **0 signifie case vide**

**Les dimensions ne sont pas explicites dans le JSON**, il faut les déduire en cherchant le max de col et le max de ligne parmi toutes les cases.

Exemple réel (grille1.json) :
```json
{
  "motif1": [[0,0,0], [1,0,0], [0,1,0], [1,1,3], [2,1,0]],
  "motif2": [[2,0,5], [3,0,0], [4,0,0], [4,1,0], [5,0,0]],
  "motif11": [[7,1,0], [7,2,0]],
  "motif14": [[6,3,0]],
  "motif15": [[5,5,0]]
}
```

Les motifs peuvent avoir des tailles différentes (1 case, 2 cases, 5 cases...).
N pour un motif = nombre de cases dans ce motif, donc un motif de 5 cases doit contenir 1,2,3,4,5.

Les grilles peuvent être rectangulaires (ex : grille9.json fait 5 colonnes x 13 lignes).

---

## Architecture imposée : MVC

L'architecture **Model-View-Controller** est obligatoire :
- Le modèle ne gère pas la vue
- La vue ne manipule pas les données directement
- Le contrôleur fait le lien

### Classes du modèle :

**`Case`** (faite par Henry)
- Position (col, ligne)
- Valeur (int ou None si vide)
- Est-elle fixée (donnée de départ non modifiable) ?

**`Motif`** (fait par Henry)
- Liste de cases
- N = nombre de cases
- Validation : contient-il exactement les chiffres 1 à N sans doublon ?

**`Grille`** (ma responsabilité)
- Dimensions (nb_colonnes, nb_lignes)
- Liste de motifs
- Méthodes : charger JSON, sauvegarder JSON, valider, voisins d'une case

---

## Ma partie (Adel)

### 1. Classe `Grille` — branche `feature/modele-grille`

Fichier : `src/model/grille.py`

```python
class Grille:
    def __init__(self):
        self.nb_colonnes = 0
        self.nb_lignes = 0
        self.motifs = []  # liste de Motif

    def charger_json(self, chemin: str) -> None:
        """Lit un fichier JSON et construit la grille.
        Format : {"motif1": [[col, ligne, valeur], ...], ...}
        valeur == 0 => case vide (None)
        Les dimensions sont déduites du max col et max ligne trouvés.
        """

    def sauvegarder_json(self, chemin: str) -> None:
        """Sérialise l'état courant de la grille au même format JSON."""

    def get_case(self, col: int, ligne: int):
        """Retourne la Case à la position (col, ligne), ou None si hors grille."""

    def get_voisins(self, col: int, ligne: int) -> list:
        """Retourne les cases adjacentes (8 directions), en ignorant les bords."""

    def est_valide(self) -> bool:
        """Vérifie toutes les contraintes : adjacence + motifs."""

    def est_complete(self) -> bool:
        """Toutes les cases sont remplies ET est_valide() == True."""
```

### 2. Chargement/sauvegarde JSON — branche `feature/json-io`

Fichier : `src/utils/json_handler.py`

Peut être une fonction standalone ou intégrée directement dans `Grille.charger_json`. Responsabilités :
- Parser le JSON
- Instancier les objets `Case` et `Motif`
- Déduire les dimensions (max_col+1, max_ligne+1)
- Convertir valeur 0 → None pour les cases vides
- Marquer comme `fixee=True` les cases avec valeur != 0

### 3. Algorithme de résolution — branche `feature/algo-resolution`

Fichier : `src/model/solveur.py`

Algorithme : **backtracking récursif**.

```python
def resoudre(grille) -> bool:
    """
    Remplit la grille par backtracking.
    Retourne True si une solution est trouvée, False sinon.
    Modifie la grille en place.
    """
    case = trouver_case_vide(grille)
    if case is None:
        return True  # toutes les cases remplies = solution trouvée

    motif = grille.get_motif_de(case)
    valeurs_possibles = range(1, len(motif.cases) + 1)

    for val in valeurs_possibles:
        if peut_placer(grille, case, val):
            case.valeur = val
            if resoudre(grille):
                return True
            case.valeur = None  # backtrack

    return False

def peut_placer(grille, case, val) -> bool:
    """
    Vérifie :
    1. val n'est pas déjà dans les 8 voisins
    2. val n'est pas déjà dans le motif de cette case
    """
```

Optimisation optionnelle (si temps) : choisir la case avec le moins de valeurs possibles en premier (heuristique MRV).

### 4. Contrôleur MVC — branche `feature/controleur-mvc`

Fichier : `src/controller/controleur.py`

Responsabilités :
- Recevoir les actions de la vue (clic case, saisie chiffre, bouton Résoudre, Charger, Sauvegarder)
- Appeler les méthodes du modèle
- Notifier la vue des changements (callbacks)
- Ne jamais toucher aux widgets directement

---

## Ce que font Henry et Jonas

**Henry** : `Case`, `Motif`, composant IHM grille, tests unitaires
Branches : `feature/modele-case`, `feature/modele-motif`, `feature/ihm-grille`, `feature/tests-modele`

**Jonas** : fenêtre principale + menu, visuel motifs (bordures épaisses), cases rouges si erreur, README
Branches : `feature/ihm-fenetre`, `feature/ihm-motifs-visuel`, `feature/ihm-erreurs`, `feature/readme-doc`

---

## Stack technique

- Langage : **Python**
- IHM : **Tkinter** (à confirmer avec le prof)
- Format données : **JSON** (format décrit ci-dessus)
- Git : branche `main` protégée, PR obligatoire pour merger

---

## Règles Git

- Travailler sur sa branche, jamais directement sur `main`
- Commit après chaque sous-partie fonctionnelle
- Format messages : `feat: ...` / `fix: ...` / `refactor: ...`
- Pull Request + relecture avant merge dans `main`

---

## Barème (priorités)

Note globale (20 pts) :
- Fonctionnalités : **9 pts** ← priorité absolue
- Ergonomie IHM : 5 pts
- Algorithme de résolution : **3 pts** ← responsabilité directe d'Adel
- Qualité code : 3 pts

Note individuelle (20 pts) :
- Commits fréquents et avec du contenu : **6 pts**
- Tâches réalisées : 10 pts

---

## Ordre d'implémentation recommandé

1. `Grille.charger_json` + déduction des dimensions → débloque tout
2. `Grille.get_voisins` + `Grille.est_valide`
3. `Solveur.resoudre` (backtracking)
4. `Grille.sauvegarder_json`
5. `Controleur` en parallèle avec Jonas sur la vue

---

## Instructions pour toi (Claude Code)

- Respecte strictement l'architecture MVC
- Ajoute des docstrings sur chaque méthode
- Si tu as besoin d'une classe que Henry doit produire (`Case`, `Motif`), crée un stub temporaire avec l'interface minimale et signale-le
- Propose des tests unitaires simples avec les fichiers JSON fournis (grille1.json à grille9.json dans le dossier `grilles/`)
- Signale toute dépendance entre les branches avant de coder
