from src.model.grille import Grille
from src.model.solveur import resoudre


class Controleur:
    """Fait le lien entre le modèle (Grille) et la vue (PyQt6).

    La vue appelle les méthodes du contrôleur.
    Le contrôleur met à jour le modèle et notifie la vue via des callbacks.
    Le modèle ne connaît pas la vue.
    """

    def __init__(self):
        self.grille = None
        # Callbacks enregistrés par la vue
        self._on_grille_chargee = None
        self._on_grille_modifiee = None
        self._on_solution_trouvee = None
        self._on_erreur = None

    # ------------------------------------------------------------------
    # Enregistrement des callbacks (la vue branche ses fonctions ici)
    # ------------------------------------------------------------------

    def on_grille_chargee(self, callback):
        """La vue fournit une fonction à appeler quand une grille est chargée."""
        self._on_grille_chargee = callback

    def on_grille_modifiee(self, callback):
        """La vue fournit une fonction à appeler quand une case change de valeur."""
        self._on_grille_modifiee = callback

    def on_solution_trouvee(self, callback):
        """La vue fournit une fonction à appeler quand la résolution se termine."""
        self._on_solution_trouvee = callback

    def on_erreur(self, callback):
        """La vue fournit une fonction à appeler en cas d'erreur (fichier manquant, etc.)."""
        self._on_erreur = callback

    # ------------------------------------------------------------------
    # Actions déclenchées par la vue
    # ------------------------------------------------------------------

    def charger_grille(self, chemin: str) -> None:
        """Charge une grille depuis un fichier JSON et notifie la vue."""
        try:
            self.grille = Grille()
            self.grille.charger_json(chemin)
            if self._on_grille_chargee:
                self._on_grille_chargee(self.grille)
        except Exception as e:
            if self._on_erreur:
                self._on_erreur(str(e))

    def sauvegarder_grille(self, chemin: str) -> None:
        """Sauvegarde l'état courant de la grille dans un fichier JSON."""
        if self.grille is None:
            return
        try:
            self.grille.sauvegarder_json(chemin)
        except Exception as e:
            if self._on_erreur:
                self._on_erreur(str(e))

    def saisir_valeur(self, col: int, ligne: int, valeur: int | None) -> None:
        """Le joueur saisit une valeur dans une case.

        Refuse la modification si la case est fixée (valeur de départ).
        Notifie la vue avec la validité courante de la grille.
        """
        if self.grille is None:
            return

        case = self.grille.get_case(col, ligne)
        if case is None or case.fixee:
            return

        case.valeur = valeur

        if self._on_grille_modifiee:
            self._on_grille_modifiee(col, ligne, valeur, self.grille.est_valide())

    def resoudre_grille(self) -> None:
        """Lance le solveur et notifie la vue du résultat."""
        if self.grille is None:
            return

        # Réinitialiser les cases non fixées avant de résoudre
        for case in self.grille._cases.values():
            if not case.fixee:
                case.valeur = None

        succes = resoudre(self.grille)

        if self._on_solution_trouvee:
            self._on_solution_trouvee(succes, self.grille)
