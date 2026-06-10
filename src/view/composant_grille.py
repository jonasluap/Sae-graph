# src/view/composant_grille.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator, QFont


class CaseWidget(QLineEdit):
    """
    Widget représentant une case individuelle à l'écran.
    La case reste un QLineEdit pour garder le travail d'Henry sur la saisie,
    mais on garde quelques attributs simples pour que Jonas puisse appliquer
    les bordures des motifs et les retours visuels d'erreur.
    """
    def __init__(self, ligne: int, colonne: int):
        super().__init__()

        self.ligne = ligne
        self.colonne = colonne

        # Ces attributs sont uniquement visuels. Les vraies données restent dans le modèle.
        self.est_fixee = False
        self.est_en_erreur = False
        self.bordures = {
            "top": 1,
            "right": 1,
            "bottom": 1,
            "left": 1
        }

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(2)  # Permet des tailles de motifs jusqu'à 99
        self.setValidator(QIntValidator(1, 99))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        font = QFont("Arial", 16)
        self.setFont(font)

        self.appliquer_style()

    def appliquer_style(self) -> None:
        """
        Centralise le style d'une case.
        La subtilité est importante : au lieu d'ajouter du CSS avec +=,
        on reconstruit le style complet à chaque fois pour éviter les doublons.
        """
        fond = "#ffffff"
        couleur_texte = "#2c3e50"
        graisse = "normal"

        if self.est_fixee:
            fond = "#e0e0e0"
            couleur_texte = "#000000"
            graisse = "bold"

        # L'erreur est prioritaire visuellement.
        if self.est_en_erreur:
            fond = "#ffcccc"

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {fond};
                color: {couleur_texte};
                font-weight: {graisse};
                border-top: {self.bordures["top"]}px solid black;
                border-right: {self.bordures["right"]}px solid black;
                border-bottom: {self.bordures["bottom"]}px solid black;
                border-left: {self.bordures["left"]}px solid black;
            }}
            QLineEdit:focus {{
                background-color: #dff3ff;
            }}
        """)


class ComposantGrille(QWidget):
    """
    Composant IHM principal affichant la grille.
    Il ne modifie jamais le modèle directement. Il émet un signal au contrôleur.
    """
    # Signal émis lors d'une saisie : (ligne, colonne, nouvelle_valeur)
    # 0 représente une case vidée.
    saisie_utilisateur = pyqtSignal(int, int, int)

    def __init__(self, rows: int = 8, cols: int = 8, parent=None):
        super().__init__(parent)

        self.rows = rows
        self.cols = cols

        # Accès rapide aux cases : {(ligne, colonne): CaseWidget}
        self.widgets_cases = {}

        # Ces deux listes sont alimentées par le contrôleur.
        self.motifs = []
        self.cases_en_erreur = set()

        self._init_ui()

    def _init_ui(self) -> None:
        self.layout = QGridLayout()
        self.layout.setSpacing(0)  # Les bordures sont gérées par le style des cases.
        self.setLayout(self.layout)
        self.draw_grid()

    def draw_grid(self) -> None:
        """Génère la grille vide d'objets QLineEdit."""
        for r in range(self.rows):
            for c in range(self.cols):
                cw = CaseWidget(r, c)

                # On capture r et c avec des valeurs par défaut dans la lambda.
                # Sinon Python utiliserait la dernière valeur de la boucle pour toutes les cases.
                cw.textEdited.connect(
                    lambda text, ligne=r, col=c: self._on_text_edited(ligne, col, text)
                )

                self.layout.addWidget(cw, r, c)
                self.widgets_cases[(r, c)] = cw

    def _on_text_edited(self, ligne: int, colonne: int, text: str) -> None:
        """
        Slot interne appelé quand le joueur tape un chiffre.
        La vue ne vérifie pas la validité métier : elle transmet simplement la saisie.
        """
        valeur = int(text) if text.isdigit() else 0

        # Attention à l'ordre : le signal est déclaré en (ligne, colonne, valeur).
        self.saisie_utilisateur.emit(ligne, colonne, valeur)

    def draw_values(self, donnees: dict) -> None:
        """
        Met à jour l'affichage avec les données du modèle.
        donnees : dictionnaire {(ligne, colonne): {"valeur": int, "fixee": bool}}
        """
        for (r, c), info in donnees.items():
            cw = self.widgets_cases.get((r, c))
            if cw is None:
                continue

            val = info.get("valeur")
            fixee = info.get("fixee", False)

            cw.blockSignals(True)

            if val is not None and val > 0:
                cw.setText(str(val))
            else:
                cw.clear()

            cw.est_fixee = fixee
            cw.setReadOnly(fixee)
            cw.blockSignals(False)

        # On remet le style après avoir modifié les valeurs,
        # car une case peut être fixée, en erreur, ou située sur une bordure de motif.
        self.appliquer_styles_cases()

    def refresh_view(self) -> None:
        """
        Méthode générique pour forcer le rafraîchissement global de l'interface.
        Le contrôleur peut l'appeler après une modification du modèle.
        """
        self.update()

    def get_widget_at(self, ligne: int, colonne: int) -> CaseWidget | None:
        """
        Permet de récupérer une case spécifique pour appliquer :
        - les bordures épaisses des motifs ;
        - les fonds rouges des erreurs.
        """
        return self.widgets_cases.get((ligne, colonne))

    def set_motifs(self, motifs: list) -> None:
        """
        Reçoit la liste des motifs depuis le contrôleur.
        La méthode accepte volontairement plusieurs formats pour rester compatible
        avec le travail d'Adel et Henry : liste de tuples, objets Case, objet Motif, etc.
        """
        self.motifs = motifs
        self.appliquer_styles_cases()

    def set_cases_en_erreur(self, cases: list) -> None:
        """
        Reçoit les cases en erreur depuis le contrôleur.
        Exemple attendu simple : [(1, 2), (3, 4)].
        """
        self.cases_en_erreur = set()

        for case in cases:
            coord = self._extraire_coordonnees_case(case)
            if coord is not None:
                self.cases_en_erreur.add(coord)

        self.appliquer_styles_cases()

    def effacer_erreurs(self) -> None:
        """Retire le retour visuel d'erreur sans toucher aux valeurs de la grille."""
        self.cases_en_erreur.clear()
        self.appliquer_styles_cases()

    def appliquer_styles_cases(self) -> None:
        """
        Réapplique tous les styles visuels.
        Cette méthode est la zone Jonas : elle gère les bordures épaisses des motifs
        et la mise en rouge des cases signalées en erreur.
        """
        # On remet d'abord toutes les cases avec une bordure fine.
        for coord, cw in self.widgets_cases.items():
            cw.bordures = {
                "top": 1,
                "right": 1,
                "bottom": 1,
                "left": 1
            }
            cw.est_en_erreur = coord in self.cases_en_erreur

        # Puis on épaissit uniquement les côtés qui séparent deux motifs différents.
        for motif in self.motifs:
            cases_motif = self._extraire_coordonnees_motif(motif)

            for ligne, colonne in cases_motif:
                cw = self.get_widget_at(ligne, colonne)
                if cw is None:
                    continue

                if (ligne - 1, colonne) not in cases_motif:
                    cw.bordures["top"] = 4

                if (ligne, colonne + 1) not in cases_motif:
                    cw.bordures["right"] = 4

                if (ligne + 1, colonne) not in cases_motif:
                    cw.bordures["bottom"] = 4

                if (ligne, colonne - 1) not in cases_motif:
                    cw.bordures["left"] = 4

        for cw in self.widgets_cases.values():
            cw.appliquer_style()

    def _extraire_coordonnees_motif(self, motif) -> set[tuple[int, int]]:
        """
        Convertit un motif en ensemble de coordonnées.
        On garde cette fonction souple car le modèle définitif peut représenter un motif
        avec une liste de tuples, une liste de Case, ou une classe Motif avec un getter.
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
            coord = self._extraire_coordonnees_case(case)
            if coord is not None:
                resultat.add(coord)

        return resultat

    def _extraire_coordonnees_case(self, case) -> tuple[int, int] | None:
        """
        Convertit une case en tuple (ligne, colonne).
        Cette souplesse évite de casser la vue si le modèle évolue légèrement.
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

        if hasattr(case, "get_ligne") and hasattr(case, "get_colonne"):
            return int(case.get_ligne()), int(case.get_colonne())

        if hasattr(case, "getLigne") and hasattr(case, "getColonne"):
            return int(case.getLigne()), int(case.getColonne())

        return None