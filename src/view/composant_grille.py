# src/view/composant_grille.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator, QFont


class CaseWidget(QLineEdit):
    """
    Représente une case de la grille.
    La case affiche une valeur, mais ne modifie jamais le modèle directement.
    """

    def __init__(self, ligne: int, colonne: int):
        super().__init__()

        self.ligne = ligne
        self.colonne = colonne

        self.est_fixee = False
        self.est_en_erreur = False
        self.est_active = True

        # Valeur maximale autorisée dans cette case.
        # Elle dépend de la taille du motif.
        self.valeur_max = 99

        self.bordures = {
            "top": 2,
            "right": 2,
            "bottom": 2,
            "left": 2
        }

        self.couleurs_bordures = {
            "top": "#000000",
            "right": "#000000",
            "bottom": "#000000",
            "left": "#000000"
        }

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(2)
        self.setValidator(QIntValidator(1, self.valeur_max))
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        font = QFont("Segoe UI", 15)
        font.setBold(True)
        self.setFont(font)

        self.appliquer_style()

    def set_valeur_max(self, valeur_max: int) -> None:
        """
        Définit la valeur maximale autorisée dans la case.
        Exemple : motif de 5 cases => valeurs autorisées de 1 à 5.
        """
        self.valeur_max = max(1, valeur_max)
        self.setValidator(QIntValidator(1, self.valeur_max))

    def appliquer_style(self) -> None:
        """
        Applique le style visuel de la case.
        Cases fixées : grisées.
        Cases modifiables : blanches.
        Cases en erreur : rouges.
        """
        if not self.est_active:
            self.blockSignals(True)
            self.clear()
            self.blockSignals(False)
            self.setReadOnly(True)
            self.setVisible(False)
            return

        self.setVisible(True)

        fond = "#FFFFFF"
        couleur_texte = "#000000"
        graisse = "bold"

        if self.est_fixee:
            fond = "#D1D5DB"
            couleur_texte = "#000000"

        if self.est_en_erreur:
            fond = "#FCA5A5"
            couleur_texte = "#7F1D1D"

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {fond};
                color: {couleur_texte};
                font-weight: {graisse};

                border-top: {self.bordures["top"]}px solid {self.couleurs_bordures["top"]};
                border-right: {self.bordures["right"]}px solid {self.couleurs_bordures["right"]};
                border-bottom: {self.bordures["bottom"]}px solid {self.couleurs_bordures["bottom"]};
                border-left: {self.bordures["left"]}px solid {self.couleurs_bordures["left"]};

                selection-background-color: #F9A8D4;
            }}

            QLineEdit:hover {{
                background-color: #FCE7F3;
            }}

            QLineEdit:focus {{
                background-color: #FBCFE8;
                color: #000000;
            }}

            QLineEdit:read-only {{
                background-color: {fond};
                color: {couleur_texte};
            }}
        """)


class ComposantGrille(QWidget):
    """
    Composant graphique qui affiche la grille.

    Il s'adapte au nombre réel de lignes et de colonnes.
    Il ne modifie jamais directement le modèle.
    Quand l'utilisateur saisit une valeur, il émet un signal vers le contrôleur.
    """

    # Signal envoyé vers la fenêtre / le contrôleur : ligne, colonne, valeur.
    saisie_utilisateur = pyqtSignal(int, int, int)

    def __init__(self, rows: int = 8, cols: int = 8, parent=None):
        super().__init__(parent)

        self.rows = rows
        self.cols = cols

        self.widgets_cases = {}
        self.motifs = []
        self.cases_en_erreur = set()
        self.cases_actives = None

        # Pour chaque case, on stocke la valeur maximale autorisée.
        # Exemple : {(0, 0): 5, (0, 1): 5}
        self.valeurs_max_par_case = {}

        # Évite les boucles pendant que la vue se remplit.
        self._mise_a_jour_vue = False

        self._init_ui()

    def _init_ui(self) -> None:
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.draw_grid()
        self.ajuster_taille_cases()

    def bloquer_signaux(self, bloquer: bool) -> None:
        """
        Bloque les signaux pendant le remplissage de la grille.
        Cela évite que la vue renvoie des modifications au contrôleur pendant le chargement.
        """
        self._mise_a_jour_vue = bloquer

        for case_widget in self.widgets_cases.values():
            case_widget.blockSignals(bloquer)

    def changer_dimensions(self, rows: int, cols: int) -> None:
        """
        Reconstruit la grille avec le vrai nombre de lignes et de colonnes.
        """
        self._mise_a_jour_vue = True
        self.setUpdatesEnabled(False)

        try:
            while self.layout.count():
                item = self.layout.takeAt(0)
                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()

            self.rows = max(1, rows)
            self.cols = max(1, cols)

            self.widgets_cases = {}
            self.motifs = []
            self.cases_en_erreur = set()
            self.cases_actives = None
            self.valeurs_max_par_case = {}

            self.draw_grid()
            self.ajuster_taille_cases()

        finally:
            self.setUpdatesEnabled(True)
            self._mise_a_jour_vue = False

    def draw_grid(self) -> None:
        """
        Génère les cases de la grille.
        """
        for ligne in range(self.rows):
            for colonne in range(self.cols):
                case_widget = CaseWidget(ligne, colonne)

                case_widget.textEdited.connect(
                    lambda text, l=ligne, c=colonne: self._on_text_edited(l, c, text)
                )

                self.layout.addWidget(case_widget, ligne, colonne)
                self.widgets_cases[(ligne, colonne)] = case_widget

    def ajuster_taille_cases(self) -> None:
        """
        Adapte la taille des cases au nombre de lignes et colonnes.
        Petite grille : grandes cases.
        Grande grille : cases plus petites.
        """
        largeur_max = 520
        hauteur_max = 520

        if self.cols <= 0 or self.rows <= 0:
            return

        taille_colonne = largeur_max // self.cols
        taille_ligne = hauteur_max // self.rows

        taille_case = min(taille_colonne, taille_ligne)

        if taille_case > 58:
            taille_case = 58

        if taille_case < 30:
            taille_case = 30

        for case_widget in self.widgets_cases.values():
            case_widget.setFixedSize(taille_case, taille_case)

            font = case_widget.font()
            font.setPointSize(max(10, taille_case // 3))
            font.setBold(True)
            case_widget.setFont(font)

        self.setFixedSize(self.cols * taille_case, self.rows * taille_case)

    def set_valeurs_max_par_case(self, valeurs_max: dict) -> None:
        """
        Reçoit la valeur maximale autorisée pour chaque case.

        Format :
        {
            (ligne, colonne): valeur_max
        }

        Exemple :
        si une case est dans un motif de 5 cases,
        alors elle accepte seulement les valeurs de 1 à 5.
        """
        self.valeurs_max_par_case = valeurs_max

        for coordonnees, valeur_max in valeurs_max.items():
            case_widget = self.widgets_cases.get(coordonnees)

            if case_widget is not None:
                case_widget.set_valeur_max(valeur_max)

    def _on_text_edited(self, ligne: int, colonne: int, text: str) -> None:
        """
        Envoie la saisie utilisateur vers le contrôleur.

        On bloque aussi les valeurs plus grandes que la taille du motif.
        Exemple : motif de 4 cases => impossible de mettre 5.
        """
        if self._mise_a_jour_vue:
            return

        if text == "":
            self.saisie_utilisateur.emit(ligne, colonne, 0)
            return

        if not text.isdigit():
            return

        valeur = int(text)

        valeur_max = self.valeurs_max_par_case.get((ligne, colonne), 99)

        if valeur < 1 or valeur > valeur_max:
            case_widget = self.widgets_cases.get((ligne, colonne))

            if case_widget is not None:
                case_widget.blockSignals(True)
                case_widget.clear()
                case_widget.blockSignals(False)

            return

        self.saisie_utilisateur.emit(ligne, colonne, valeur)

    def set_cases_actives(self, cases) -> None:
        """
        Indique quelles cases existent réellement dans la grille chargée.
        """
        self._mise_a_jour_vue = True

        try:
            self.cases_actives = set(cases)

            for coordonnees, case_widget in self.widgets_cases.items():
                case_widget.est_active = coordonnees in self.cases_actives

            self.appliquer_styles_cases()

        finally:
            self._mise_a_jour_vue = False

    def draw_values(self, donnees: dict) -> None:
        """
        Affiche les valeurs dans les cases.

        Format attendu :
        {
            (ligne, colonne): {"valeur": int, "fixee": bool}
        }
        """
        self._mise_a_jour_vue = True
        self.setUpdatesEnabled(False)

        try:
            for coordonnees, case_widget in self.widgets_cases.items():
                case_widget.blockSignals(True)

                if self.cases_actives is not None and coordonnees not in self.cases_actives:
                    case_widget.est_active = False
                    case_widget.clear()
                    case_widget.blockSignals(False)
                    continue

                info = donnees.get(coordonnees)

                if info is None:
                    case_widget.clear()
                    case_widget.est_fixee = False
                    case_widget.setReadOnly(True)
                    case_widget.blockSignals(False)
                    continue

                valeur = info.get("valeur")
                fixee = info.get("fixee", False)

                if valeur is not None and valeur > 0:
                    case_widget.setText(str(valeur))
                else:
                    case_widget.clear()

                case_widget.est_fixee = fixee
                case_widget.setReadOnly(fixee)

                case_widget.blockSignals(False)

            self.appliquer_styles_cases()

        finally:
            self.setUpdatesEnabled(True)
            self._mise_a_jour_vue = False

    def refresh_view(self) -> None:
        self.update()

    def get_widget_at(self, ligne: int, colonne: int) -> CaseWidget | None:
        return self.widgets_cases.get((ligne, colonne))

    def set_motifs(self, motifs: list) -> None:
        """
        Reçoit les motifs depuis la fenêtre.
        Les motifs sont utilisés seulement pour dessiner les bordures.
        """
        self.motifs = motifs
        self.appliquer_styles_cases()

    def set_cases_en_erreur(self, cases: list) -> None:
        """
        Affiche les cases en erreur en rouge.
        """
        self.cases_en_erreur = set()

        for case in cases:
            coordonnees = self._extraire_coordonnees_case(case)

            if coordonnees is not None:
                self.cases_en_erreur.add(coordonnees)

        self.appliquer_styles_cases()

    def effacer_erreurs(self) -> None:
        self.cases_en_erreur.clear()
        self.appliquer_styles_cases()

    def appliquer_styles_cases(self) -> None:
        """
        Dessine les bordures des motifs.

        Les traits normaux sont fins.
        Les contours de motifs sont noirs et plus épais.
        """
        couleur_normale = "#000000"
        couleur_motif = "#000000"

        for coordonnees, case_widget in self.widgets_cases.items():
            case_widget.bordures = {
                "top": 2,
                "right": 2,
                "bottom": 2,
                "left": 2
            }

            case_widget.couleurs_bordures = {
                "top": couleur_normale,
                "right": couleur_normale,
                "bottom": couleur_normale,
                "left": couleur_normale
            }

            if self.cases_actives is not None:
                case_widget.est_active = coordonnees in self.cases_actives

            case_widget.est_en_erreur = coordonnees in self.cases_en_erreur

        for motif in self.motifs:
            cases_motif = self._extraire_coordonnees_motif(motif)

            for ligne, colonne in cases_motif:
                case_widget = self.get_widget_at(ligne, colonne)

                if case_widget is None:
                    continue

                if (ligne - 1, colonne) not in cases_motif:
                    case_widget.bordures["top"] = 6
                    case_widget.couleurs_bordures["top"] = couleur_motif

                if (ligne, colonne + 1) not in cases_motif:
                    case_widget.bordures["right"] = 6
                    case_widget.couleurs_bordures["right"] = couleur_motif

                if (ligne + 1, colonne) not in cases_motif:
                    case_widget.bordures["bottom"] = 6
                    case_widget.couleurs_bordures["bottom"] = couleur_motif

                if (ligne, colonne - 1) not in cases_motif:
                    case_widget.bordures["left"] = 6
                    case_widget.couleurs_bordures["left"] = couleur_motif

        for case_widget in self.widgets_cases.values():
            case_widget.appliquer_style()

        self.ajuster_taille_cases()
        self.update()

    def _extraire_coordonnees_motif(self, motif) -> set[tuple[int, int]]:
        """
        Convertit un motif en ensemble de coordonnées.
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
        """
        if isinstance(case, tuple) or isinstance(case, list):
            if len(case) >= 2:
                return int(case[0]), int(case[1])

        if isinstance(case, dict):
            if "ligne" in case and "colonne" in case:
                return int(case["ligne"]), int(case["colonne"])

            if "row" in case and "col" in case:
                return int(case["row"]), int(case["col"])

        if hasattr(case, "ligne") and hasattr(case, "colonne"):
            return int(case.ligne), int(case.colonne)

        if hasattr(case, "ligne") and hasattr(case, "col"):
            return int(case.ligne), int(case.col)

        if hasattr(case, "get_ligne") and hasattr(case, "get_colonne"):
            return int(case.get_ligne()), int(case.get_colonne())

        if hasattr(case, "getLigne") and hasattr(case, "getColonne"):
            return int(case.getLigne()), int(case.getColonne())

        return None