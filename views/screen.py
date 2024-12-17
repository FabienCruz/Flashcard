import tkinter as tk
from tkinter import ttk

class Screen(tk.Tk):
    """
    la Classe Screen est responsable de l'affichage de l'interface graphique.

    """
    def __init__(self, manage_screen):
        super().__init__()
        self.title("Flashcards")
        self.manage_db = manage_screen.manage_db
        # Attributs pour stocker les instances des écrans
        self.deck_screen = None # Instance de DeckManagerScreen
        self.card_screen = None # Instance de CardManagerScreen
        self.return_button = None # Instance de ReturnButton
        self.dealer = None # Instance de Dealer
        self.card_mat = None # Instance de CardMat


        # --- L'écran (Screen) est divisé en quatre cadres (frame)
        
        # frame (up-left)
        self.frm_up_left = ttk.Frame(master=self)
        self.frm_up_left.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.N))

        # frame (down-left)
        self.frm_down_left = ttk.Frame(master=self)
        self.frm_down_left.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

        # frame (up-right)
        self.frm_up_right = ttk.Frame(master=self)
        self.frm_up_right.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.E, tk.N))

        # frame (down-right)
        self.frm_down_right = ttk.Frame(master=self)
        self.frm_down_right.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.E, tk.S))

        # frame (bottom)
        self.frm_bottom = ttk.Frame(master=self)
        self.frm_bottom.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.S))

    # --- Méthodes pour effacer le contenu des cadres

    # efface le frame (up-left)
    def clear_frm_up_left(self):
        for widget in self.frm_up_left.winfo_children():
            widget.destroy()

    # efface le frame (down-left)
    def clear_frm_down_left(self):
        for widget in self.frm_down_left.winfo_children():
            widget.destroy()

    # efface le frame (up-right)
    def clear_frm_up_right(self):
        for widget in self.frm_up_right.winfo_children():
            widget.destroy()

    # efface le frame (down-right)
    def clear_frm_down_right(self):
        for widget in self.frm_down_right.winfo_children():
            widget.destroy()
    
    # efface le frame (bottom)
    def clear_frm_bottom(self):
        for widget in self.frm_bottom.winfo_children():
            widget.destroy()

    # efface le contenu de tous les cadres
    def clear_all_frames(self):
        self.clear_frm_up_left()
        self.clear_frm_down_left()
        self.clear_frm_up_right()
        self.clear_frm_down_right()
        self.clear_frm_bottom()

    # ---- Méthodes pour afficher les écrans

    def set_game(self, dealer, card_mat):
        self.dealer = dealer
        self.card_mat = card_mat

    def show_game(self):
        if self.dealer and self.card_mat:
            self.dealer.initialize_dealer()
            self.card_mat.initialize_card_mat()
    
    def set_managers(self, deck_screen, card_screen, return_button):
        """
        Stocke les références vers les écrans de gestion.
        
        Args:
            deck_screen: Instance de DeckManagerScreen
            card_screen: Instance de CardManagerScreen
        """
        self.deck_screen = deck_screen
        self.card_screen = card_screen
        self.return_button = return_button

    def show_deck_manager(self):
        """Affiche l'écran de gestion des paquets."""
        if self.deck_screen:
            self.deck_screen.initialize_deck_manager()

    def show_card_manager(self):
        """Affiche l'écran de gestion des cartes."""
        if self.card_screen:
            self.card_screen.initialize_card_manager()

    def show_return_button(self):
        if self.return_button:
            self.return_button.initialize_return_button()

    # --- Méthodes pour activer l'écran (Screen), de fait active l'application

    # méthode pour lancer l'application et écouter les événements
    def run(self):
        self.protocol("WM_DELETE", self.stop)
        self.mainloop()

    # méthode pour fermer l'application
    def stop(self):
        print("fermeture de l'application")
        self.destroy()
        self.manage_db.close_database()
