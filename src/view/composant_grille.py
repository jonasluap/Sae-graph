# src/view/composant_grille.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator, QFont

class CaseWidget(QLineEdit):
    """
    Widget représentant une case individuelle à l'écran.
    Hérite de QLineEdit pour permettre la saisie. Jonas pourra utiliser
    les QSS (Qt Style Sheets) sur ce widget pour modifier les bordures.
    """
    def __init__(self, ligne: int, colonne: int):
        super().__init__()
        self.ligne = ligne
        self.colonne = colonne
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(2) # Permet des tailles de motifs jusqu'à 99
        self.setValidator(QIntValidator(1, 99))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Style de base, Jonas écrasera ceci pour les bordures épaisses
        self.setStyleSheet("border: 1px solid gray; background-color: white;")
        font = QFont("Arial", 16)
        self.setFont(font)

class ComposantGrille(QWidget):
    """
    Composant IHM principal affichant la grille.
    Il ne modifie jamais le modèle directement. Il émet un signal au contrôleur.
    """
    # Signal émis lors d'une saisie: (ligne, colonne, nouvelle_valeur)
    # 0 représente une case vidée
    saisie_utilisateur = pyqtSignal(int, int, int)

    def __init__(self, rows: int = 8, cols: int = 8, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.widgets_cases = {}  # Dictionnaire pour accès rapide {(ligne, col): CaseWidget}
        self._init_ui()

    def _init_ui(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(0) # Jonas gérera l'espacement/les bordures via le CSS
        self.setLayout(self.layout)
        self.draw_grid()

    def draw_grid(self) -> None:
        """Génère la grille vide d'objets QLineEdit."""
        for r in range(self.rows):
            for c in range(self.cols):
                cw = CaseWidget(r, c)
                # Connexion de l'événement de saisie au slot interne
                cw.textEdited.connect(lambda text, ligne=r, col=c: self._on_text_edited(ligne, col, text))
                
                self.layout.addWidget(cw, r, c)
                self.widgets_cases[(r, c)] = cw

    def _on_text_edited(self, ligne: int, colonne: int, text: str) -> None:
        """Slot interne appelé quand le joueur tape un chiffre."""
        valeur = int(text) if text.isdigit() else 0
        self.saisie_utilisateur.emit(colonne, ligne, valeur)

    def draw_values(self, donnees: dict) -> None:
        """
        Met à jour l'affichage avec les données du modèle.
        donnees: dictionnaire {(ligne, colonne): {"valeur": int, "fixee": bool}}
        """
        for (r, c), info in donnees.items():
            cw = self.widgets_cases.get((r, c))
            if cw:
                val = info["valeur"]
                cw.blockSignals(True) # Évite de déclencher des signaux lors du rafraîchissement
                
                if val is not None and val > 0:
                    cw.setText(str(val))
                else:
                    cw.clear()
                    
                cw.setReadOnly(info["fixee"])
                
                # Applique un style visuel différent si la case est fixée (indice visuel de base)
                if info["fixee"]:
                    cw.setStyleSheet(cw.styleSheet() + " font-weight: bold; color: black; background-color: #e0e0e0;")
                    
                cw.blockSignals(False)

    def refresh_view(self) -> None:
        """
        Méthode générique pour forcer le rafraîchissement global de l'interface.
        Adel/Le contrôleur pourra l'appeler.
        """
        self.update()

    # --- MÉTHODES EXPOSÉES POUR JONAS ---
    
    def get_widget_at(self, ligne: int, colonne: int) -> CaseWidget | None:
        """
        Permet à Jonas de récupérer une case spécifique pour appliquer :
        - Ses bordures épaisses (motifs)
        - Ses fonds rouges (erreurs)
        """
        return self.widgets_cases.get((ligne, colonne))