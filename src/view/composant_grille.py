from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt

class ComposantGrille(QWidget):
    """
    Ce widget personnalisé prend en charge tout le dessin de la grille du Néonaure.
    Il intercepte les clics de souris et les saisies clavier, puis délègue le dessin 
    à des sous-fonctions bien spécifiques pour cloisonner le travail de l'équipe.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Cette option permet au widget de capter les entrées clavier dès qu'on clique dessus.
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Dimensions par défaut d'une grille classique de Néonaure.
        self.nb_lignes = 8
        self.nb_colonnes = 8
        
        # Variables de suivi de l'état du jeu qui seront mises à jour par le contrôleur.
        self.case_selectionnee = None
        self.valeurs_cases = {}
        self.motifs = []
        self.cases_en_erreur = []

    def paintEvent(self, event) -> None:
        """
        Cette méthode s'exécute automatiquement dès que l'interface a besoin d'être redessinée.
        Pour éviter que Henry et toi ne vous marchiez sur les pieds lors des fusions de branches,
        le dessin est découpé en quatre blocs autonomes.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Nous calculons la dimension idéale d'une case pour qu'elle reste carrée et 
        # s'adapte dynamiquement si l'utilisateur redimensionne la fenêtre.
        largeur_case = self.width() // self.nb_colonnes
        hauteur_case = self.height() // self.nb_lignes
        taille_case = min(largeur_case, hauteur_case)
        
        # --- ZONE DE TRAVAIL DE HENRY ---
        # Henry s'occupera de coder le fond des cases, le quadrillage de base et les nombres.
        self.dessiner_fond_et_grille_base(painter, taille_case)
        self.dessiner_chiffres(painter, taille_case)
        
        # --- ZONE DE TRAVAIL DE JONAS (TOI) ---
        # C'est ici que tu viendras ajouter tes méthodes visuelles à l'étape 3 et 4.
        self.dessiner_bordures_motifs(painter, taille_case)
        self.dessiner_surbrillance_erreurs(painter, taille_case)
        
        painter.end()

    def dessiner_fond_et_grille_base(self, painter, taille_case) -> None:
        """
        [Zone Henry] Cette méthode dessinera les lignes grises classiques de la grille
        et appliquera une couleur distinctive sur la case actuellement sélectionnée par le joueur.
        """
        # Henry complétera cette méthode lors de sa tâche IHM.
        pass

    def dessiner_chiffres(self, painter, taille_case) -> None:
        """
        [Zone Henry] Cette fonction se chargera d'écrire les chiffres au centre de chaque case,
        en appliquant éventuellement un style différent si le chiffre est fixé au départ ou saisi par le joueur.
        """
        # Henry lira le dictionnaire self.valeurs_cases pour afficher les éléments textuels.
        pass

    def dessiner_bordures_motifs(self, painter, taille_case) -> None:
        """
        [Zone Jonas] C'est ta méthode pour l'Étape 3. Elle consistera à parcourir la liste des motifs
        pour tracer des bordures noires très épaisses tout autour, afin de bien les délimiter visuellement.
        """
        # Tu coderas cette partie pour valider les contraintes de délimitation des motifs.
        pass

    def dessiner_surbrillance_erreurs(self, painter, taille_case) -> None:
        """
        [Zone Jonas] C'est ta méthode pour l'Étape 4. Si une case est jugée en erreur par le modèle,
        tu appliqueras ici un filtre ou un rectangle rouge translucide par-dessus pour avertir le joueur.
        """
        # Tu coderas cette fonction en inspectant la liste self.cases_en_erreur.
        pass

    def mousePressEvent(self, event) -> None:
        """
        [Zone Henry] Capte les clics sur la grille pour identifier quelle case a été visée,
        puis demande un rafraîchissement graphique de l'écran.
        """
        # Henry déterminera la ligne et la colonne cliquées à l'aide de la position du clic.
        self.update()