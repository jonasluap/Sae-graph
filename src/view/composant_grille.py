# src/view/composant_grille.py

from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator, QFont


class CaseWidget(QLineEdit):
    """
    Widget représentant une case individuelle à l'écran.

    Hérite de QLineEdit afin de permettre la saisie directe des valeurs
    par l'utilisateur.

    Jonas pourra personnaliser son apparence (bordures, couleurs, etc.)
    via les feuilles de style Qt (QSS).
    """

    def __init__(self, ligne: int, colonne: int):
        super().__init__()

        # Coordonnées de la case dans la grille
        self.ligne = ligne
        self.colonne = colonne

        # Centre le texte dans la case
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Limite la saisie à deux caractères
        # (permet des motifs jusqu'à une taille de 99)
        self.setMaxLength(2)

        # Autorise uniquement les entiers entre 1 et 99
        self.setValidator(QIntValidator(1, 99))

        # Le widget s'agrandit automatiquement avec la fenêtre
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Style visuel de base
        # Jonas pourra remplacer ce style pour afficher les motifs
        self.setStyleSheet(
            "border: 1px solid gray; background-color: white;"
        )

        # Police utilisée pour l'affichage des valeurs
        font = QFont("Arial", 16)
        self.setFont(font)


class ComposantGrille(QWidget):
    """
    Composant graphique principal affichant la grille du jeu.

    Cette classe appartient à la couche Vue (MVC).
    Elle n'accède jamais directement au modèle et communique
    uniquement via des signaux Qt envoyés au contrôleur.
    """

    # Signal émis lorsqu'un utilisateur modifie une case.
    # Paramètres :
    # - colonne
    # - ligne
    # - nouvelle valeur
    #
    # Une valeur de 0 représente une case vidée.
    saisie_utilisateur = pyqtSignal(int, int, int)

    def __init__(self, rows: int = 8, cols: int = 8, parent=None):
        super().__init__(parent)

        # Dimensions de la grille affichée
        self.rows = rows
        self.cols = cols

        # Permet de retrouver rapidement un widget à partir
        # de ses coordonnées (ligne, colonne)
        self.widgets_cases = {}

        self._init_ui()

    def _init_ui(self):
        """
        Initialise l'interface graphique du composant.
        """

        # Layout utilisé pour positionner les cases
        self.layout = QGridLayout()

        # Aucun espace entre les cases.
        # Les séparations visuelles seront gérées par les bordures QSS.
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

        # Création de la grille graphique
        self.draw_grid()

    def draw_grid(self) -> None:
        """
        Génère la grille vide composée d'objets CaseWidget.
        """

        for r in range(self.rows):
            for c in range(self.cols):

                # Création du widget graphique correspondant à la case
                cw = CaseWidget(r, c)

                # Lorsqu'une valeur est saisie,
                # on appelle le slot interne de traitement
                cw.textEdited.connect(
                    lambda text, ligne=r, col=c:
                    self._on_text_edited(ligne, col, text)
                )

                # Ajout dans le layout Qt
                self.layout.addWidget(cw, r, c)

                # Mémorisation pour accès rapide futur
                self.widgets_cases[(r, c)] = cw

    def _on_text_edited(self, ligne: int, colonne: int, text: str) -> None:
        """
        Slot appelé automatiquement lorsqu'un utilisateur
        modifie le contenu d'une case.
        """

        # Conversion du texte saisi en entier.
        # Si la case est vide, on transmet la valeur 0.
        valeur = int(text) if text.isdigit() else 0

        # Notification du contrôleur via le signal Qt
        self.saisie_utilisateur.emit(colonne, ligne, valeur)

    def draw_values(self, donnees: dict) -> None:
        """
        Met à jour l'affichage à partir des données du modèle.

        Paramètre :
            donnees :
            {
                (ligne, colonne):
                {
                    "valeur": int,
                    "fixee": bool
                }
            }
        """

        # Parcourt toutes les données fournies par le modèle
        for (r, c), info in donnees.items():

            cw = self.widgets_cases.get((r, c))

            if cw:

                val = info["valeur"]

                # Désactive temporairement les signaux
                # pour éviter de déclencher une nouvelle saisie
                # lors du rafraîchissement de l'affichage
                cw.blockSignals(True)

                # Affiche la valeur si elle existe
                if val is not None and val > 0:
                    cw.setText(str(val))
                else:
                    cw.clear()

                # Une case fixée devient non modifiable
                cw.setReadOnly(info["fixee"])

                # Mise en évidence visuelle des cases fixées
                if info["fixee"]:
                    cw.setStyleSheet(
                        cw.styleSheet()
                        + " font-weight: bold;"
                        + " color: black;"
                        + " background-color: #e0e0e0;"
                    )

                # Réactivation des signaux utilisateur
                cw.blockSignals(False)

    def refresh_view(self) -> None:
        """
        Force le rafraîchissement global du composant graphique.

        Cette méthode peut être appelée par le contrôleur
        après une modification du modèle.
        """
        self.update()

    # ---------------------------------------------------------
    # Méthodes exposées à Jonas
    # ---------------------------------------------------------

    def get_widget_at(self, ligne: int, colonne: int) -> CaseWidget | None:
        """
        Retourne le widget situé à une position donnée.

        Cette méthode permet à Jonas d'appliquer facilement :
        - les bordures épaisses des motifs,
        - les indicateurs visuels d'erreur,
        - tout autre style graphique spécifique.
        """
        return self.widgets_cases.get((ligne, colonne))