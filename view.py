import tkinter as tk
from tkinter import ttk

class Screen:
    def __init__(self, controller):
        self.window = tk.Tk()
        self.window.title("Flashcards")
        self.controller = controller
        
        # frame (up-left) to select thema
        self.dealer_frm = ttk.Frame(master=self.window)
        self.dealer_frm.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.N))

        # frame (down-left) to activate
        self.action_thema_frm = ttk.Frame(master=self.window)
        self.action_thema_frm.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

        # frame (up-right) to display cards (card mats)
        self.card_mat_frm = ttk.Frame(master=self.window)
        self.card_mat_frm.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.E, tk.N))

        # frame (down-right) to act
        self.card_action_frm = ttk.Frame(master=self.window)
        self.card_action_frm.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.E, tk.S))

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()
    
    def stop(self):
        print("fermeture de l'application")
        self.window.destroy()
        self.controller.close_database()


class Dealer:
    
    def __init__(self, screen):
        self.screen = screen
        self.decks = screen.controller.get_decks()
        self.selected_decks = []

        # section with selection of dealer's menu
        self.deck_lbl = ttk.Label(self.screen.dealer_frm, text='Sélectionner:', font=('Helvetica', 12, 'bold'))
        self.deck_lbl.grid(sticky=tk.W, padx=5, pady=5)
               
        #--- variables to track the state of checkboxes
        self.check_vars = []
        
        #--- display list of themes with checkboxes
        for deck in self.decks:
            var = tk.IntVar()  # Variable to track the checkbox state (0 = unchecked, 1 = checked)
            self.check_vars.append(var)
            checkbox = ttk.Checkbutton(
                master=self.screen.dealer_frm, 
                text=deck, 
                variable=var,
                command=self.update_selected_decks
                )
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    def update_selected_decks(self):
        self.selected_decks = self.screen.controller.on_deck_selection(self.check_vars, self.decks)

    def get_selected_decks(self):
        return self.selected_decks
    
    def give_a_card(self):
        selected_cards = self.screen.controller.get_cards_by_deck(self.selected_decks)
        return selected_cards

class CardMat:
    def __init__(self, screen, dealer):
        self.screen = screen
        self.selected_decks_id = dealer.get_selected_decks()
        #self.card = screen.controller.pick_a_card(selected_decks_id)

        # affichage de la carte
        self.card_title_lbl = ttk.Label(master=self.screen.card_mat_frm, text='Carte:', font=('Helvetica', 12, 'bold'))
        self.card_title_lbl.grid(padx=5, pady=5)
"""
class CardAction:
    def __init__(self, screen):
        self.screen = screen

        self.card_action_btn_1 = ttk.Button(master=self.screen.card_action_frm, text='choix 1')
        self.card_action_btn_1.grid(column=0, row=0, padx=5, pady=5)
        self.card_action_btn_2 = ttk.Button(master=self.screen.card_action_frm, text='choix 2')
        self.card_action_btn_2.grid(column=1, row=0, padx=5, pady=5)
"""

"""
class ActionThema:
    def __init__(self, screen):
        self.screen = screen

        # button to modify
        self.action_thema_btn_modif = ttk.Button(master=self.screen.action_thema_frm, text='modifier')
        self.action_thema_btn_modif.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.S))
        
        # button "pick a card"
        self.action_thema_btn_launch = ttk.Button(master=self.screen.action_thema_frm, text='tirer carte')
        self.action_thema_btn_launch.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))
"""      
