import tkinter as tk
from tkinter import ttk

class Dealer:
    """

    La Classe Dealer est responsable du menu 'croupier'.
    Elle fait fonction de menu.

    """
    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.manage_screen = manage_screen

    def initialize_dealer(self):
        # efface le contenu des cadres
        self.screen.clear_frm_up_left()
        self.screen.clear_frm_down_left()

        # bouton pour gérer les cartes
        self.manage_btn = ttk.Button(master=self.screen.frm_down_left, text='Gérer les cartes', command=self.show_manager_screen) # command=self.manage_cards
        self.manage_btn.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))
        
        # section with selection of dealer's menu
        self.deck_lbl = ttk.Label(self.screen.frm_up_left, text='Sélectionner:', font=('Helvetica', 12, 'bold'))
        self.deck_lbl.grid(sticky=tk.W, padx=5, pady=5)
        
        #--- variables to track the state of checkboxes
        self.check_vars = []
        
        #--- display list of themes with checkboxes
        for deck in self.manage_screen.manage_deck.get_decks():
            var = tk.IntVar()  # Variable to track the checkbox state (0 = unchecked, 1 = checked)
            self.check_vars.append(var)
            checkbox = ttk.Checkbutton(
                master=self.screen.frm_up_left, 
                text=deck[1], # deck is a tuple (id, name) 
                variable=var,
                command=lambda v=self.check_vars: self.manage_screen.manage_deck.update_selected_decks(v)
                )
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    def show_manager_screen(self):
        self.screen.clear_all_frames()
        self.manage_screen.show_manager_screen()
