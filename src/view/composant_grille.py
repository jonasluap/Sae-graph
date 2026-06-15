# src/view/composant_grille.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QFont

# Palette de fonds attribuée à chaque motif pour les distinguer visuellement.
# Les couleurs sont sombres pour rester lisibles sur le thème nuit tout en
# différenciant clairement les régions (style Killer Sudoku).
COULEURS_MOTIFS = [
    "#1B2A4A",  # bleu marine
    "#1A3A24",  # vert forêt
    "#3A1A2A",  # framboise
    "#2A2A14",  # olive
    "#0D2A3A",  # cyan nuit
    "#3A1A12",  # brique
    "#1A1A3C",  # violet nuit
    "#103020",  # émeraude
    "#2C1A3A",  # prune
    "#3A2A0E",  # ambre
    "#143030",  # teal
    "#2A1018",  # bordeaux
    "#1E301A",  # vert mousse
    "#10203A",  # bleu acier
    "#301A1E",  # rose foncé
]


class CaseWidget(QLineEdit):
    """
    Widget représentant une case individuelle à l'écran.

    Chaque case connaît sa position (ligne, colonne), la couleur de son motif,
    son état (fixée / en erreur) et l'épaisseur de chacune de ses bordures.
    Le validateur est mis à jour à chaque chargement de grille pour n'autoriser
    que les valeurs 1..N correspondant à la taille du motif auquel elle appartient.
    """

    def __init__(self, ligne: int, colonne: int):
        super().__init__()

        self.ligne = ligne
        self.colonne = colonne

        self.est_fixee = False
        self.est_en_erreur = False
        self.couleur_motif = "#160B35"

        self.bordures = {
            "top": 1,
            "right": 1,
            "bottom": 1,
            "left": 1
        }

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(1)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        font = QFont("Segoe UI", 18)
        font.setBold(True)
        self.setFont(font)

        self.appliquer_style()

    def appliquer_style(self) -> None:
        """
        Recalcule et applique le style complet de la case.

        Le fond utilise la couleur du motif assignée par ComposantGrille.
        Les bordures épaisses (>= 4 px) délimitant les motifs sont blanches ;
        les bordures fines internes sont quasi invisibles.
        En cas d'erreur, le fond passe au rouge et les bordures épaisses au rose.
        """
        fond = self.couleur_motif
        couleur_texte = "#C8D4E8"
        bordure_fine = "#0A0A1A"
        bordure_epaisse = "#FFFFFF"
        graisse = "normal"

        if self.est_fixee:
            couleur_texte = "#FFFFFF"
            graisse = "bold"

        if self.est_en_erreur:
            fond = "#7F1D1D"
            couleur_texte = "#FEE2E2"
            bordure_fine = "#7F1D1D"
            bordure_epaisse = "#F87171"
            graisse = "bold"

        def bc(epaisseur):
            return bordure_epaisse if epaisseur >= 4 else bordure_fine

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {fond};
                color: {couleur_texte};
                font-weight: {graisse};
                border-top: {self.bordures["top"]}px solid {bc(self.bordures["top"])};
                border-right: {self.bordures["right"]}px solid {bc(self.bordures["right"])};
                border-bottom: {self.bordures["bottom"]}px solid {bc(self.bordures["bottom"])};
                border-left: {self.bordures["left"]}px solid {bc(self.bordures["left"])};
                selection-background-color: #A5B4FC;
            }}

            QLineEdit:hover {{
                background-color: {fond}CC;
            }}

            QLineEdit:focus {{
                background-color: {fond};
                color: #FFFFFF;
                border: 2px solid #60A5FA;
            }}

            QLineEdit:read-only {{
                background-color: {fond};
                color: {couleur_texte};
            }}
        """)


class ComposantGrille(QWidget):
    """
    Composant IHM principal affichant la grille.

    Il ne modifie jamais le modèle directement.
    Quand l'utilisateur saisit une valeur, il émet un signal vers le contrôleur.
    """

    # Signal émis lors d'une saisie : ligne, colonne, valeur.
    # La valeur 0 représente une case vidée.
    saisie_utilisateur = pyqtSignal(int, int, int)

    def __init__(self, rows: int = 8, cols: int = 8, parent=None):
        super().__init__(parent)

        self.rows = rows
        self.cols = cols

        self.widgets_cases = {}
        self.motifs = []
        self.cases_en_erreur = set()

        self._init_ui()

    def _init_ui(self) -> None:
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.draw_grid()

    def draw_grid(self) -> None:
        """
        Génère la grille vide avec des CaseWidget.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                case_widget = CaseWidget(r, c)

                # Subtilité Python :
                # ligne=r et col=c évitent que toutes les lambdas gardent
                # la dernière valeur de la boucle.
                case_widget.textEdited.connect(
                    lambda text, ligne=r, col=c: self._on_text_edited(ligne, col, text)
                )

                self.layout.addWidget(case_widget, r, c)
                self.widgets_cases[(r, c)] = case_widget

    def _on_text_edited(self, ligne: int, colonne: int, text: str) -> None:
        """
        Appelé quand le joueur tape un chiffre.
        La vue ne vérifie pas les règles du jeu : elle transmet seulement la saisie.
        """
        valeur = int(text) if text.isdigit() else 0
        self.saisie_utilisateur.emit(ligne, colonne, valeur)

    def draw_values(self, donnees: dict) -> None:
        """
        Met à jour l'affichage avec les données du modèle.

        Format attendu :
        {
            (ligne, colonne): {"valeur": int, "fixee": bool}
        }
        """
        for (ligne, colonne), info in donnees.items():
            case_widget = self.widgets_cases.get((ligne, colonne))

            if case_widget is None:
                continue

            valeur = info.get("valeur")
            fixee = info.get("fixee", False)

            case_widget.blockSignals(True)

            if valeur is not None and valeur > 0:
                case_widget.setText(str(valeur))
            else:
                case_widget.clear()

            case_widget.est_fixee = fixee
            case_widget.setReadOnly(fixee)

            case_widget.blockSignals(False)

        self.appliquer_styles_cases()

    def reconstruire(self, rows: int, cols: int) -> None:
        """
        Supprime tous les widgets existants et recrée la grille aux nouvelles dimensions.
        Appelé à chaque chargement de fichier.
        """
        for widget in self.widgets_cases.values():
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.widgets_cases.clear()
        self.motifs = []
        self.cases_en_erreur = set()
        self.rows = rows
        self.cols = cols
        self.draw_grid()

    def refresh_view(self) -> None:
        """
        Force le rafraîchissement global de l'interface.
        """
        self.update()

    def get_widget_at(self, ligne: int, colonne: int) -> CaseWidget | None:
        """
        Récupère une case précise de la grille.
        """
        return self.widgets_cases.get((ligne, colonne))

    def set_motifs(self, motifs: list) -> None:
        """
        Reçoit les motifs depuis le contrôleur.
        La méthode accepte plusieurs formats pour rester compatible
        avec les classes du modèle.
        """
        self.motifs = motifs
        self.appliquer_styles_cases()

    def set_cases_en_erreur(self, cases: list) -> None:
        """
        Reçoit les cases en erreur depuis le contrôleur.

        Exemple simple :
        [(1, 2), (3, 4)]
        """
        self.cases_en_erreur = set()

        for case in cases:
            coordonnees = self._extraire_coordonnees_case(case)

            if coordonnees is not None:
                self.cases_en_erreur.add(coordonnees)

        self.appliquer_styles_cases()

    def effacer_erreurs(self) -> None:
        """
        Retire le retour visuel d'erreur sans toucher aux valeurs.
        """
        self.cases_en_erreur.clear()
        self.appliquer_styles_cases()

    def appliquer_styles_cases(self) -> None:
        """
        Réapplique l'ensemble des styles visuels sur toutes les cases.

        Pour chaque motif : attribue sa couleur de fond (depuis COULEURS_MOTIFS),
        pose des bordures épaisses (6 px, blanches) sur les côtés qui touchent
        un motif différent, et met à jour le validateur pour n'accepter que 1..N.
        Les cases signalées comme en erreur reçoivent un fond rouge quel que soit
        leur motif.
        """
        for coordonnees, case_widget in self.widgets_cases.items():
            case_widget.bordures = {
                "top": 1,
                "right": 1,
                "bottom": 1,
                "left": 1
            }
            case_widget.couleur_motif = "#160B35"
            case_widget.est_en_erreur = coordonnees in self.cases_en_erreur

        for i, motif in enumerate(self.motifs):
            couleur = COULEURS_MOTIFS[i % len(COULEURS_MOTIFS)]
            cases_motif = self._extraire_coordonnees_motif(motif)
            n = len(cases_motif)

            for ligne, colonne in cases_motif:
                case_widget = self.get_widget_at(ligne, colonne)

                if case_widget is None:
                    continue

                case_widget.couleur_motif = couleur
                if n <= 9:
                    pattern = f"[1-{n}]"
                else:
                    pattern = "|".join(str(i) for i in range(1, n + 1))
                case_widget.setMaxLength(len(str(n)))
                case_widget.setValidator(QRegularExpressionValidator(QRegularExpression(pattern)))

                if (ligne - 1, colonne) not in cases_motif:
                    case_widget.bordures["top"] = 6

                if (ligne, colonne + 1) not in cases_motif:
                    case_widget.bordures["right"] = 6

                if (ligne + 1, colonne) not in cases_motif:
                    case_widget.bordures["bottom"] = 6

                if (ligne, colonne - 1) not in cases_motif:
                    case_widget.bordures["left"] = 6

        for case_widget in self.widgets_cases.values():
            case_widget.appliquer_style()

    def _extraire_coordonnees_motif(self, motif) -> set[tuple[int, int]]:
        """
        Convertit un motif en ensemble de coordonnées.

        On garde cette méthode souple parce que le modèle peut représenter
        un motif de plusieurs manières : dictionnaire, objet Motif,
        liste de tuples, liste de Case, etc.
        """
        cases = None

        if isinstance(motif, dict):
            cases = motif.get("cases")
        elif hasattr(motif, "get_cases"):
            cases = motif.get_cases()
        elif hasattr(motif, "getCases"):
            cases = motif.getCases()
        elif hasattr(motif, "cases"):
            cases = motif.cases
        elif hasattr(motif, "_cases"):
            cases = motif._cases
        else:
            cases = motif

        resultat = set()

        if cases is None:
            return resultat

        for case in cases:
            coordonnees = self._extraire_coordonnees_case(case)

            if coordonnees is not None:
                resultat.add(coordonnees)

        return resultat

    def _extraire_coordonnees_case(self, case) -> tuple[int, int] | None:
        """
        Convertit une case en tuple (ligne, colonne).
        Cela évite de casser l'IHM si le modèle évolue légèrement.
        """
        if isinstance(case, tuple) or isinstance(case, list):
            if len(case) >= 2:
                return int(case[0]), int(case[1])

        if isinstance(case, dict):
            if "ligne" in case and "colonne" in case:
                return int(case["ligne"]), int(case["colonne"])

            if "row" in case and "col" in case:
                return int(case["row"]), int(case["col"])

        if hasattr(case, "ligne") and hasattr(case, "col"):
            return int(case.ligne), int(case.col)

        if hasattr(case, "ligne") and hasattr(case, "colonne"):
            return int(case.ligne), int(case.colonne)

        if hasattr(case, "get_ligne") and hasattr(case, "get_colonne"):
            return int(case.get_ligne()), int(case.get_colonne())

        if hasattr(case, "getLigne") and hasattr(case, "getColonne"):
            return int(case.getLigne()), int(case.getColonne())

        return None