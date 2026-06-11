# src/view/fenetre_principale.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QFileDialog, QMessageBox, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from src.view.composant_grille import ComposantGrille


class FenetrePrincipale(QMainWindow):
    """
    Fenêtre principale de l'application Néonaure.

    L'interface est séparée en deux écrans :
    - un menu principal sobre, dans un style jeu ;
    - un écran de jeu avec la grille et les actions principales.

    La vue ne modifie jamais directement le modèle.
    Toutes les actions importantes passent par le contrôleur.
    """

    def __init__(self, controleur):
        super().__init__()

        self.controleur = controleur

        # L'application démarre en mode sombre pour garder une ambiance sobre.
        self.mode_sombre = True

        self.setWindowTitle("Néonaure - SAÉ Graphes-IHM")
        self.resize(1000, 720)
        self.setMinimumSize(820, 620)

        self.initialiser_menus()
        self.initialiser_interface()
        self.appliquer_theme_jeu()

    def initialiser_menus(self) -> None:
        """
        Crée la barre de menus en haut.
        Elle reste utile même si l'utilisateur a aussi un menu principal au centre.
        """
        barre_menu = self.menuBar()

        menu_fichier = barre_menu.addMenu("Fichier")

        action_charger = QAction("Charger une grille...", self)
        action_charger.triggered.connect(self.action_charger)
        menu_fichier.addAction(action_charger)

        action_sauvegarder = QAction("Sauvegarder", self)
        action_sauvegarder.triggered.connect(self.action_sauvegarder)
        menu_fichier.addAction(action_sauvegarder)

        menu_fichier.addSeparator()

        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.action_quitter)
        menu_fichier.addAction(action_quitter)

        menu_jeu = barre_menu.addMenu("Jouer")

        action_jouer = QAction("Aller au jeu", self)
        action_jouer.triggered.connect(self.afficher_page_jeu)
        menu_jeu.addAction(action_jouer)

        action_verifier = QAction("Vérifier la grille", self)
        action_verifier.triggered.connect(self.action_verifier)
        menu_jeu.addAction(action_verifier)

        action_resoudre = QAction("Résoudre la grille", self)
        action_resoudre.triggered.connect(self.action_resoudre)
        menu_jeu.addAction(action_resoudre)

        action_reinitialiser = QAction("Réinitialiser la partie", self)
        action_reinitialiser.triggered.connect(self.action_reinitialiser)
        menu_jeu.addAction(action_reinitialiser)

        menu_affichage = barre_menu.addMenu("Options")

        self.action_mode_sombre = QAction("Mode sombre", self)
        self.action_mode_sombre.setCheckable(True)
        self.action_mode_sombre.setChecked(self.mode_sombre)
        self.action_mode_sombre.triggered.connect(self.changer_theme)
        menu_affichage.addAction(self.action_mode_sombre)

        menu_aide = barre_menu.addMenu("Aide")

        action_regles = QAction("Règles du jeu", self)
        action_regles.triggered.connect(self.action_regles)
        menu_aide.addAction(action_regles)

        action_credits = QAction("Crédits", self)
        action_credits.triggered.connect(self.action_credits)
        menu_aide.addAction(action_credits)

    def initialiser_interface(self) -> None:
        """
        Utilise un QStackedWidget pour passer facilement du menu principal
        à l'écran de jeu.
        """
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page_menu = self.creer_page_menu()
        self.page_jeu = self.creer_page_jeu()

        self.stack.addWidget(self.page_menu)
        self.stack.addWidget(self.page_jeu)

        self.stack.setCurrentWidget(self.page_menu)

    def creer_page_menu(self) -> QWidget:
        """
        Crée un menu principal sobre, inspiré d'un écran de jeu.
        On garde les gros boutons verticaux, mais avec des couleurs plus discrètes.
        """
        page = QWidget()
        page.setObjectName("pageMenu")

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        page.setLayout(layout_principal)

        carte_menu = QFrame()
        carte_menu.setObjectName("carteMenu")

        layout_menu = QVBoxLayout()
        layout_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_menu.setSpacing(14)
        layout_menu.setContentsMargins(40, 40, 40, 40)
        carte_menu.setLayout(layout_menu)

        titre = QLabel("NÉONAURE")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setObjectName("titreMenu")

        sous_titre = QLabel("Jeu de logique")
        sous_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sous_titre.setObjectName("sousTitreMenu")

        layout_menu.addStretch()
        layout_menu.addWidget(titre)
        layout_menu.addWidget(sous_titre)

        self.bouton_jouer = self.creer_bouton_menu("JOUER", self.lancer_nouvelle_partie)
        self.bouton_continuer = self.creer_bouton_menu("CONTINUER", self.afficher_page_jeu)
        self.bouton_options = self.creer_bouton_menu("OPTIONS", self.ouvrir_options)
        self.bouton_credits = self.creer_bouton_menu("CRÉDITS", self.action_credits)
        self.bouton_quitter = self.creer_bouton_menu("QUITTER", self.action_quitter)

        layout_menu.addSpacing(20)
        layout_menu.addWidget(self.bouton_jouer, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_continuer, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_options, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_credits, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_quitter, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addStretch()

        layout_principal.addWidget(carte_menu)

        return page

    def creer_bouton_menu(self, texte: str, slot) -> QPushButton:
        """
        Crée un gros bouton vertical pour le menu principal.
        Le style est appliqué dans appliquer_theme_jeu().
        """
        bouton = QPushButton(texte)
        bouton.setFixedSize(280, 58)
        bouton.clicked.connect(slot)
        bouton.setCursor(Qt.CursorShape.PointingHandCursor)
        bouton.setObjectName("boutonMenu")
        return bouton

    def creer_page_jeu(self) -> QWidget:
        """
        Crée l'écran de jeu avec une barre d'actions en haut
        et la grille au centre.
        """
        page = QWidget()
        page.setObjectName("pageJeu")

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(24, 20, 24, 24)
        layout_principal.setSpacing(16)
        page.setLayout(layout_principal)

        entete = QHBoxLayout()
        entete.setSpacing(10)

        bouton_retour_menu = QPushButton("← Menu")
        bouton_retour_menu.clicked.connect(self.afficher_page_menu)

        bouton_charger = QPushButton("Charger")
        bouton_charger.clicked.connect(self.action_charger)

        bouton_sauvegarder = QPushButton("Sauvegarder")
        bouton_sauvegarder.clicked.connect(self.action_sauvegarder)

        bouton_verifier = QPushButton("Vérifier")
        bouton_verifier.clicked.connect(self.action_verifier)

        bouton_resoudre = QPushButton("Résoudre")
        bouton_resoudre.clicked.connect(self.action_resoudre)

        bouton_reset = QPushButton("Réinitialiser")
        bouton_reset.clicked.connect(self.action_reinitialiser)

        entete.addWidget(bouton_retour_menu)
        entete.addStretch()
        entete.addWidget(bouton_charger)
        entete.addWidget(bouton_sauvegarder)
        entete.addWidget(bouton_verifier)
        entete.addWidget(bouton_resoudre)
        entete.addWidget(bouton_reset)

        carte = QFrame()
        carte.setObjectName("carteGrille")

        layout_carte = QVBoxLayout()
        layout_carte.setContentsMargins(20, 20, 20, 20)
        layout_carte.setSpacing(14)
        carte.setLayout(layout_carte)

        titre_jeu = QLabel("Plateau de jeu")
        titre_jeu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_jeu.setObjectName("titreJeu")

        # Important : on passe parent=self.
        # Si on écrit ComposantGrille(self), self serait pris pour le nombre de lignes.
        self.composant_grille = ComposantGrille(parent=self)

        layout_carte.addWidget(titre_jeu)
        layout_carte.addWidget(self.composant_grille)

        layout_principal.addLayout(entete)
        layout_principal.addWidget(carte)

        return page

    def appliquer_theme_jeu(self) -> None:
        """
        Applique un thème sobre.
        Le mode sombre reprend une ambiance violet / bleu nuit,
        proche de l'image donnée, mais sans couleurs trop agressives.
        """
        if self.mode_sombre:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #0B1020;
                }

                QMenuBar {
                    background-color: #111827;
                    color: #E5E7EB;
                    border-bottom: 1px solid #27324A;
                    padding: 5px;
                    font-size: 14px;
                }

                QMenuBar::item {
                    padding: 7px 12px;
                    border-radius: 5px;
                }

                QMenuBar::item:selected {
                    background-color: #1E293B;
                }

                QMenu {
                    background-color: #111827;
                    color: #E5E7EB;
                    border: 1px solid #334155;
                    padding: 6px;
                }

                QMenu::item {
                    padding: 8px 24px;
                    border-radius: 5px;
                }

                QMenu::item:selected {
                    background-color: #312E81;
                }

                QWidget#pageMenu {
                    background-color: #0B1020;
                }

                QFrame#carteMenu {
                    background-color: #120A2A;
                    border: 1px solid #3B2F63;
                }

                QLabel#titreMenu {
                    color: #F8FAFC;
                    font-size: 36px;
                    font-weight: bold;
                    letter-spacing: 3px;
                }

                QLabel#sousTitreMenu {
                    color: #A5B4FC;
                    font-size: 15px;
                    margin-bottom: 8px;
                }

                QPushButton#boutonMenu {
                    background-color: #241547;
                    color: #F8FAFC;
                    border: 2px solid #6D5BA6;
                    border-radius: 6px;
                    padding: 10px;
                    font-size: 17px;
                    font-weight: bold;
                }

                QPushButton#boutonMenu:hover {
                    background-color: #31225E;
                    border: 2px solid #A5B4FC;
                }

                QPushButton#boutonMenu:pressed {
                    background-color: #1A1038;
                }

                QWidget#pageJeu {
                    background-color: #0B1020;
                }

                QLabel#titreJeu {
                    color: #F8FAFC;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 8px;
                }

                QPushButton {
                    background-color: #241547;
                    color: #F8FAFC;
                    border: 1px solid #6D5BA6;
                    border-radius: 7px;
                    padding: 9px 13px;
                    font-size: 14px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #31225E;
                }

                QPushButton:pressed {
                    background-color: #1A1038;
                }

                QFrame#carteGrille {
                    background-color: #120A2A;
                    border-radius: 14px;
                    border: 1px solid #3B2F63;
                }

                QStatusBar {
                    background-color: #111827;
                    color: #E5E7EB;
                }
            """)

            self.statusBar().showMessage("Mode sombre activé")

        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #F3F4F6;
                }

                QMenuBar {
                    background-color: #FFFFFF;
                    color: #111827;
                    border-bottom: 1px solid #D1D5DB;
                    padding: 5px;
                    font-size: 14px;
                }

                QMenuBar::item {
                    padding: 7px 12px;
                    border-radius: 5px;
                }

                QMenuBar::item:selected {
                    background-color: #E5E7EB;
                }

                QMenu {
                    background-color: #FFFFFF;
                    color: #111827;
                    border: 1px solid #D1D5DB;
                    padding: 6px;
                }

                QMenu::item {
                    padding: 8px 24px;
                    border-radius: 5px;
                }

                QMenu::item:selected {
                    background-color: #E0E7FF;
                }

                QWidget#pageMenu {
                    background-color: #F3F4F6;
                }

                QFrame#carteMenu {
                    background-color: #FFFFFF;
                    border: 1px solid #CBD5E1;
                }

                QLabel#titreMenu {
                    color: #111827;
                    font-size: 36px;
                    font-weight: bold;
                    letter-spacing: 3px;
                }

                QLabel#sousTitreMenu {
                    color: #4B5563;
                    font-size: 15px;
                    margin-bottom: 8px;
                }

                QPushButton#boutonMenu {
                    background-color: #E5E7EB;
                    color: #111827;
                    border: 2px solid #9CA3AF;
                    border-radius: 6px;
                    padding: 10px;
                    font-size: 17px;
                    font-weight: bold;
                }

                QPushButton#boutonMenu:hover {
                    background-color: #D1D5DB;
                    border: 2px solid #6366F1;
                }

                QPushButton#boutonMenu:pressed {
                    background-color: #CBD5E1;
                }

                QWidget#pageJeu {
                    background-color: #F3F4F6;
                }

                QLabel#titreJeu {
                    color: #111827;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 8px;
                }

                QPushButton {
                    background-color: #E5E7EB;
                    color: #111827;
                    border: 1px solid #9CA3AF;
                    border-radius: 7px;
                    padding: 9px 13px;
                    font-size: 14px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #D1D5DB;
                }

                QPushButton:pressed {
                    background-color: #CBD5E1;
                }

                QFrame#carteGrille {
                    background-color: #FFFFFF;
                    border-radius: 14px;
                    border: 1px solid #CBD5E1;
                }

                QStatusBar {
                    background-color: #FFFFFF;
                    color: #111827;
                    border-top: 1px solid #D1D5DB;
                }
            """)

            self.statusBar().showMessage("Mode clair activé")

    def changer_theme(self) -> None:
        """
        Bascule entre mode sombre et mode clair.
        """
        self.mode_sombre = self.action_mode_sombre.isChecked()
        self.appliquer_theme_jeu()

    def afficher_page_menu(self) -> None:
        """
        Revient au menu principal.
        """
        self.stack.setCurrentWidget(self.page_menu)
        self.statusBar().showMessage("Menu principal")

    def afficher_page_jeu(self) -> None:
        """
        Affiche l'écran de jeu.
        """
        self.stack.setCurrentWidget(self.page_jeu)
        self.statusBar().showMessage("Écran de jeu")

    def lancer_nouvelle_partie(self) -> None:
        """
        Lance une nouvelle partie.
        Pour l'instant, on affiche l'écran de jeu.
        Si le contrôleur possède une méthode nouvelle_partie, elle sera appelée.
        """
        self.afficher_page_jeu()

        methode = getattr(self.controleur, "nouvelle_partie", None)
        if callable(methode):
            methode()

    def ouvrir_options(self) -> None:
        """
        Ouvre une petite boîte de dialogue pour changer le thème.
        """
        boite = QMessageBox(self)
        boite.setWindowTitle("Options")
        boite.setText(
            "Souhaites-tu activer ou désactiver le mode sombre ?"
        )

        boite.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )

        boite.button(QMessageBox.StandardButton.Yes).setText("Activer")
        boite.button(QMessageBox.StandardButton.No).setText("Désactiver")
        boite.button(QMessageBox.StandardButton.Cancel).setText("Annuler")

        reponse = boite.exec()

        if reponse == QMessageBox.StandardButton.Yes:
            self.mode_sombre = True
            self.action_mode_sombre.setChecked(True)
            self.appliquer_theme_jeu()

        elif reponse == QMessageBox.StandardButton.No:
            self.mode_sombre = False
            self.action_mode_sombre.setChecked(False)
            self.appliquer_theme_jeu()

    def _appeler_controleur(self, nom_methode: str, *args):
        """
        Appelle une méthode du contrôleur seulement si elle existe.
        Cela évite que l'interface plante pendant le développement.
        """
        methode = getattr(self.controleur, nom_methode, None)

        if callable(methode):
            return methode(*args)

        QMessageBox.warning(
            self,
            "Fonction indisponible",
            f"La méthode du contrôleur '{nom_methode}' n'est pas encore disponible."
        )

        return None

    def action_charger(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Charger une grille Néonaure",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )

        if filepath:
            self.statusBar().showMessage(f"Grille chargée : {filepath}")
            self._appeler_controleur("charger_grille", filepath)

    def action_sauvegarder(self) -> None:
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder la grille",
            "",
            "Fichiers JSON (*.json)"
        )

        if filepath:
            self.statusBar().showMessage(f"Sauvegarde : {filepath}")
            self._appeler_controleur("sauvegarder_grille", filepath)

    def action_verifier(self) -> None:
        resultat = self._appeler_controleur("verifier_grille")

        if resultat is True:
            self.statusBar().showMessage("La grille est correcte.")
            QMessageBox.information(self, "Vérification", "La grille est correcte.")

        elif resultat is False:
            self.statusBar().showMessage("La grille contient encore des erreurs.")
            QMessageBox.warning(self, "Vérification", "La grille contient encore des erreurs.")

    def action_resoudre(self) -> None:
        self.statusBar().showMessage("Résolution en cours...")
        self._appeler_controleur("resoudre_grille")

    def action_reinitialiser(self) -> None:
        reponse = QMessageBox.question(
            self,
            "Réinitialiser",
            "Voulez-vous vraiment réinitialiser la grille ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reponse == QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage("Grille réinitialisée.")
            self._appeler_controleur("reinitialiser_grille")

    def action_quitter(self) -> None:
        reponse = QMessageBox.question(
            self,
            "Quitter",
            "Voulez-vous vraiment quitter le jeu ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reponse == QMessageBox.StandardButton.Yes:
            self.close()

    def action_regles(self) -> None:
        regles = (
            "Règles du Néonaure :\n\n"
            "1. Un chiffre par case.\n"
            "2. Un chiffre doit être entouré de chiffres différents, y compris en diagonale.\n"
            "3. Un motif de N cases, repéré en traits gras, doit comporter tous les chiffres de 1 à N."
        )

        QMessageBox.information(self, "Règles du jeu", regles)

    def action_credits(self) -> None:
        QMessageBox.information(
            self,
            "Crédits",
            "Néonaure\n\n"
            "Projet SAÉ Graphes-IHM\n"
            "BUT Informatique 2025-2026\n\n"
            "Membres du groupe :\n"
            "- Adel\n"
            "- Henry\n"
            "- Jonas\n\n"
            "Interface réalisée avec PyQt6."
        )