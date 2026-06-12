import json
from src.model.case import Case
from src.model.motif import Motif


class Grille:
    """Modèle principal du jeu Néonaure.

    Contient toutes les cases organisées en motifs.
    Les dimensions sont déduites du fichier JSON (max col + 1, max ligne + 1).
    """

    def __init__(self):
        self.nb_colonnes = 0
        self.nb_lignes = 0
        self.motifs = []          # liste de Motif
        self._cases = {}          # dictionnaire (col, ligne) -> Case pour accès O(1)

    # ------------------------------------------------------------------
    # Chargement / sauvegarde
    # ------------------------------------------------------------------

    def charger_json(self, chemin: str) -> None:
        """Lit un fichier JSON et construit la grille.

        Format attendu : {"motifX": [[col, ligne, valeur], ...], ...}
        valeur == 0 signifie case vide (stockée comme None).
        Les dimensions sont déduites du max col et max ligne trouvés.
        """
        with open(chemin, "r", encoding="utf-8") as f:
            donnees = json.load(f)

        self.motifs = []
        self._cases = {}
        max_col = 0
        max_ligne = 0

        for nom_motif, liste_cases in donnees.items():
            cases_du_motif = []

            for col, ligne, valeur in liste_cases:
                # Suivre les dimensions maximales
                if col > max_col:
                    max_col = col
                if ligne > max_ligne:
                    max_ligne = ligne

                # valeur 0 dans le JSON = case vide
                valeur_reelle = None if valeur == 0 else valeur
                est_fixee = valeur != 0

                case = Case(col, ligne, valeur_reelle, est_fixee)
                cases_du_motif.append(case)

                # Enregistrer dans le dictionnaire pour get_case()
                self._cases[(col, ligne)] = case

            self.motifs.append(Motif(nom_motif, cases_du_motif))

        # +1 car les indices commencent à 0
        self.nb_colonnes = max_col + 1
        self.nb_lignes = max_ligne + 1

    def sauvegarder_json(self, chemin: str) -> None:
        """Sérialise l'état courant de la grille au même format JSON."""
        donnees = {}

        for motif in self.motifs:
            liste_cases = []
            for case in motif.cases:
                # None -> 0 pour respecter le format d'origine
                valeur = case.valeur if case.valeur is not None else 0
                liste_cases.append([case.col, case.ligne, valeur])
            donnees[motif.nom] = liste_cases

        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Accès aux cases
    # ------------------------------------------------------------------

    def get_case(self, col: int, ligne: int) -> Case | None:
        """Retourne la Case à la position (col, ligne), ou None si hors grille."""
        return self._cases.get((col, ligne))

    def get_voisins(self, col: int, ligne: int) -> list:
        """Retourne les cases adjacentes dans les 8 directions (graphe roi).

        Les cases hors grille ou inexistantes sont ignorées.
        """
        voisins = []
        for dc in [-1, 0, 1]:
            for dl in [-1, 0, 1]:
                if dc == 0 and dl == 0:
                    continue  # la case elle-même
                case = self.get_case(col + dc, ligne + dl)
                if case is not None:
                    voisins.append(case)
        return voisins

    def get_motif_de(self, case: Case) -> Motif | None:
        """Retourne le motif auquel appartient la case donnée."""
        for motif in self.motifs:
            if case in motif.cases:
                return motif
        return None

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def est_valide(self) -> bool:
        """Vérifie toutes les contraintes sur l'état courant (grille partielle ou complète).

        Contrainte 1 — adjacence : deux cases voisines ne peuvent pas avoir la même valeur.
        Contrainte 2 — motifs : pas de doublon dans un motif.
        Les cases vides (None) sont ignorées dans les deux vérifications.
        """
        # Contrainte 1 : adjacence (graphe roi, 8 directions)
        for case in self._cases.values():
            if case.valeur is None:
                continue
            for voisin in self.get_voisins(case.col, case.ligne):
                if voisin.valeur == case.valeur:
                    return False

        # Contrainte 2 : pas de doublon dans chaque motif
        for motif in self.motifs:
            if not motif.est_valide():
                return False

        return True

    def est_complete(self) -> bool:
        """Toutes les cases sont remplies ET toutes les contraintes sont respectées."""
        toutes_remplies = all(c.valeur is not None for c in self._cases.values())
        return toutes_remplies and self.est_valide()

    # ------------------------------------------------------------------
    # Utilitaires
    # ------------------------------------------------------------------

    def __repr__(self):
        return f"Grille({self.nb_colonnes}x{self.nb_lignes}, {len(self.motifs)} motifs)"
