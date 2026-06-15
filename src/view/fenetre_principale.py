# src/view/fenetre_principale.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QFileDialog, QMessageBox, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from src.view.composant_grille import ComposantGrille


class FenetrePrincipale(QMainWindow):
    """
    Fenêtre principale de l'application Néonaure.

    La vue affiche l'interface et transmet les actions au contrôleur.
    Elle ne charge pas le JSON elle-même et ne modifie pas directement le modèle.
    """

    def __init__(self, controleur):
        super().__init__()

        self.controleur = controleur
        self.mode_sombre = True
        self._chargement_en_cours = False

        self.setWindowTitle("Néonaure - SAÉ Graphes-IHM")
        self.resize(1000, 720)
        self.setMinimumSize(820, 620)

        self.initialiser_menus()
        self.initialiser_interface()
        self.brancher_controleur()
        self.appliquer_theme_jeu()

    def initialiser_menus(self) -> None:
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

        action_jouer = QAction("Charger une grille", self)
        action_jouer.triggered.connect(self.action_charger)
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

        menu_options = barre_menu.addMenu("Options")

        self.action_mode_sombre = QAction("Mode sombre", self)
        self.action_mode_sombre.setCheckable(True)
        self.action_mode_sombre.setChecked(self.mode_sombre)
        self.action_mode_sombre.triggered.connect(self.changer_theme)
        menu_options.addAction(self.action_mode_sombre)

        menu_aide = barre_menu.addMenu("Aide")

        action_regles = QAction("Règles du jeu", self)
        action_regles.triggered.connect(self.action_regles)
        menu_aide.addAction(action_regles)

        action_credits = QAction("Crédits", self)
        action_credits.triggered.connect(self.action_credits)
        menu_aide.addAction(action_credits)

    def initialiser_interface(self) -> None:
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page_menu = self.creer_page_menu()
        self.page_jeu = self.creer_page_jeu()

        self.stack.addWidget(self.page_menu)
        self.stack.addWidget(self.page_jeu)

        self.stack.setCurrentWidget(self.page_menu)

    def creer_page_menu(self) -> QWidget:
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
        layout_menu.addSpacing(20)

        self.bouton_jouer = self.creer_bouton_menu("JOUER", self.action_charger)
        self.bouton_continuer = self.creer_bouton_menu("CONTINUER", self.afficher_page_jeu)
        self.bouton_options = self.creer_bouton_menu("OPTIONS", self.ouvrir_options)
        self.bouton_credits = self.creer_bouton_menu("CRÉDITS", self.action_credits)
        self.bouton_quitter = self.creer_bouton_menu("QUITTER", self.action_quitter)

        layout_menu.addWidget(self.bouton_jouer, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_continuer, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_options, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_credits, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addWidget(self.bouton_quitter, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_menu.addStretch()

        layout_principal.addWidget(carte_menu)

        return page

    def creer_bouton_menu(self, texte: str, slot) -> QPushButton:
        bouton = QPushButton(texte)
        bouton.setFixedSize(280, 58)
        bouton.clicked.connect(slot)
        bouton.setCursor(Qt.CursorShape.PointingHandCursor)
        bouton.setObjectName("boutonMenu")
        return bouton

    def creer_page_jeu(self) -> QWidget:
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
        layout_carte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        carte.setLayout(layout_carte)

        titre_jeu = QLabel("Plateau de jeu")
        titre_jeu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_jeu.setObjectName("titreJeu")

        self.composant_grille = ComposantGrille(parent=self)

        layout_carte.addWidget(titre_jeu)
        layout_carte.addWidget(self.composant_grille, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_principal.addLayout(entete)
        layout_principal.addWidget(carte)

        return page

    def brancher_controleur(self) -> None:
        """
        Branche les callbacks du contrôleur vers la vue.
        C'est ce qui permet à la grille chargée de s'afficher.
        """
        if hasattr(self.controleur, "on_grille_chargee"):
            self.controleur.on_grille_chargee(self.afficher_grille)

        if hasattr(self.controleur, "on_grille_modifiee"):
            self.controleur.on_grille_modifiee(self.apres_saisie_case)

        if hasattr(self.controleur, "on_solution_trouvee"):
            self.controleur.on_solution_trouvee(self.afficher_solution)

        if hasattr(self.controleur, "on_erreur"):
            self.controleur.on_erreur(self.afficher_erreur)

        self.composant_grille.saisie_utilisateur.connect(self.envoyer_saisie_au_controleur)

    def envoyer_saisie_au_controleur(self, ligne: int, colonne: int, valeur: int) -> None:
        """
        La vue travaille en ligne / colonne.
        Le modèle travaille en colonne / ligne.
        On inverse donc avant d'envoyer au contrôleur.
        """
        if self._chargement_en_cours:
            return

        valeur_modele = None if valeur == 0 else valeur
        self._appeler_controleur("saisir_valeur", colonne, ligne, valeur_modele)

    def afficher_grille(self, grille) -> None:
        """
        Affiche la grille reçue depuis le contrôleur.
        La taille est calculée à partir des cases réellement présentes.

        On calcule aussi la valeur maximale autorisée par case :
        motif de N cases => valeurs autorisées de 1 à N.
        """
        self._chargement_en_cours = True
        self.composant_grille.setUpdatesEnabled(False)

        try:
            donnees_vue = {}

            for (colonne, ligne), case in grille._cases.items():
                donnees_vue[(ligne, colonne)] = {
                    "valeur": case.valeur,
                    "fixee": case.fixee
                }

            if donnees_vue:
                nb_lignes = max(ligne for ligne, colonne in donnees_vue.keys()) + 1
                nb_colonnes = max(colonne for ligne, colonne in donnees_vue.keys()) + 1
            else:
                nb_lignes = 1
                nb_colonnes = 1

            self.composant_grille.changer_dimensions(nb_lignes, nb_colonnes)

            motifs_vue = []
            valeurs_max_par_case = {}

            for motif in grille.motifs:
                cases_motif = []

                for case in motif.cases:
                    cases_motif.append((case.ligne, case.col))

                motifs_vue.append(cases_motif)

                taille_motif = len(cases_motif)

                for coordonnees in cases_motif:
                    valeurs_max_par_case[coordonnees] = taille_motif

            self.composant_grille.bloquer_signaux(True)
            self.composant_grille.set_cases_actives(donnees_vue.keys())
            self.composant_grille.set_valeurs_max_par_case(valeurs_max_par_case)
            self.composant_grille.draw_values(donnees_vue)
            self.composant_grille.set_motifs(motifs_vue)

        finally:
            self.composant_grille.bloquer_signaux(False)
            self.composant_grille.setUpdatesEnabled(True)
            self._chargement_en_cours = False
            self.composant_grille.update()

        self.afficher_page_jeu()
        self.statusBar().showMessage("Grille chargée et affichée.")


    def apres_saisie_case(self, colonne: int, ligne: int, valeur: int | None, est_valide: bool) -> None:
        """
        Appelée par le contrôleur après une saisie.
        """
        if self._chargement_en_cours:
            return

        if est_valide:
            self.composant_grille.effacer_erreurs()
            self.statusBar().showMessage("Saisie acceptée.")
        else:
            self.composant_grille.set_cases_en_erreur([(ligne, colonne)])
            self.statusBar().showMessage("Cette saisie crée une erreur.")

    def afficher_solution(self, succes: bool, grille) -> None:
        """
        Affiche le résultat du solveur.
        """
        if succes:
            self.afficher_grille(grille)
            QMessageBox.information(self, "Résolution", "Une solution a été trouvée.")
            self.statusBar().showMessage("Solution trouvée.")
        else:
            QMessageBox.warning(
                self,
                "Résolution",
                "Aucune solution trouvée ou le solveur s'est arrêté."
            )
            self.statusBar().showMessage("Résolution arrêtée.")

    def afficher_erreur(self, message: str) -> None:
        QMessageBox.critical(self, "Erreur", message)
        self.statusBar().showMessage("Erreur.")

    def appliquer_theme_jeu(self) -> None:
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
        self.mode_sombre = self.action_mode_sombre.isChecked()
        self.appliquer_theme_jeu()

    def afficher_page_menu(self) -> None:
        self.stack.setCurrentWidget(self.page_menu)
        self.statusBar().showMessage("Menu principal")

    def afficher_page_jeu(self) -> None:
        self.stack.setCurrentWidget(self.page_jeu)
        self.statusBar().showMessage("Écran de jeu")

    def ouvrir_options(self) -> None:
        boite = QMessageBox(self)
        boite.setWindowTitle("Options")
        boite.setText("Souhaites-tu activer ou désactiver le mode sombre ?")

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
            self.statusBar().showMessage(f"Chargement : {filepath}")
            QTimer.singleShot(0, lambda: self._appeler_controleur("charger_grille", filepath))

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
            self.composant_grille.effacer_erreurs()
            self.statusBar().showMessage("La grille est correcte.")
            QMessageBox.information(self, "Vérification", "La grille est correcte.")

        elif resultat is False:
            self.statusBar().showMessage("La grille contient encore des erreurs.")
            QMessageBox.warning(self, "Vérification", "La grille contient encore des erreurs.")

        else:
            QMessageBox.information(self, "Vérification", "Aucune grille n'est chargée.")

    def action_resoudre(self) -> None:
        reponse = QMessageBox.question(
            self,
            "Résoudre",
            "Le solveur peut prendre du temps. Voulez-vous continuer ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reponse != QMessageBox.StandardButton.Yes:
            return

        self.statusBar().showMessage("Résolution en cours...")
        QTimer.singleShot(0, lambda: self._appeler_controleur("resoudre_grille"))

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
            "3. Un motif de N cases doit comporter tous les chiffres de 1 à N."
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