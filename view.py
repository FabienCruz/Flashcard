import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Screen:
    """
    la Classe Screen est responsable de l'affichage de l'interface graphique.

    """
    def __init__(self, controller):
        self.window = tk.Tk()
        self.window.title("Flashcards")
        self.controller = controller
        
        # --- L'écran (Screen) est divisé en quatre cadres (frame)
        
        # frame (up-left)
        self.frm_up_left = ttk.Frame(master=self.window)
        self.frm_up_left.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.N))

        # frame (down-left)
        self.frm_down_left = ttk.Frame(master=self.window)
        self.frm_down_left.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

        # frame (up-right)
        self.frm_up_right = ttk.Frame(master=self.window)
        self.frm_up_right.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.E, tk.N))

        # frame (down-right)
        self.frm_down_right = ttk.Frame(master=self.window)
        self.frm_down_right.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.E, tk.S))

        # frame (bottom)
        self.frm_bottom = ttk.Frame(master=self.window)
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

    # --- Méthodes pour activer l'écran (Screen), de fait active l'application

    # méthode pour lancer l'application et écouter les événements
    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    # méthode pour fermer l'application
    def stop(self):
        print("fermeture de l'application")
        self.window.destroy()
        self.controller.close_database()


class Dealer:
    """

    La Classe Dealer est responsable du menu 'croupier'.
    Elle fait fonction de menu.

    """
    def __init__(self, screen, manage_deck):
        self.screen = screen
        self.decks = manage_deck
        self.selected_decks = []
        self.initialize_dealer()

    def initialize_dealer(self):
        # efface le contenu des cadres
        self.screen.clear_frm_up_left()
        self.screen.clear_frm_down_left()

        # bouton pour gérer les cartes
        self.manage_btn = ttk.Button(master=self.screen.frm_down_left, text='Gérer les cartes', command=self.show_manager) # command=self.manage_cards
        self.manage_btn.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))
        
        # section with selection of dealer's menu
        self.deck_lbl = ttk.Label(self.screen.frm_up_left, text='Sélectionner:', font=('Helvetica', 12, 'bold'))
        self.deck_lbl.grid(sticky=tk.W, padx=5, pady=5)
        
        #--- variables to track the state of checkboxes
        self.check_vars = []
        
        #--- display list of themes with checkboxes
        for deck in self.decks.get_decks():
            var = tk.IntVar()  # Variable to track the checkbox state (0 = unchecked, 1 = checked)
            self.check_vars.append(var)
            checkbox = ttk.Checkbutton(
                master=self.screen.frm_up_left, 
                text=deck, 
                variable=var,
                command=self.update_selected_decks
                )
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    
    def update_selected_decks(self):
        thema_list = self.decks.get_decks()
        self.selected_decks = self.decks.on_deck_selection(self.check_vars, thema_list)

    def get_selected_decks(self):
        return self.selected_decks
    
    def show_manager(self):
        print("show_manager")
        self.screen.clear_all_frames()
        DeckManagerScreen(self.screen, self.decks)
        # CardManagerScreen(self.screen, self.decks)

class CardMat:
    """

    La classe CardMat est responsable de l'affichage du 'tapis de jeu'.
    Elle affiche les cartes, face question, face réponse, les boutons d'actions.

    """

    def __init__(self, screen, dealer, manage_card):
        self.screen = screen
        self.dealer = dealer
        self.cards = manage_card
        self.initialize_card_mat()

    def initialize_card_mat(self):
        # efface le contenu des cadres
        self.screen.clear_frm_up_right()
        self.screen.clear_frm_down_right()

        # affichage bouton pour tirer une carte
        self.btn_draw = ttk.Button(master=self.screen.frm_down_right, text='tirer carte', command=lambda: self.deal_a_card(is_question=True))
        self.btn_draw.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.E, tk.S))

        # affichage de la carte
        self.card_title_lbl = ttk.Label(master=self.screen.frm_up_right, text='Carte:', font=('Helvetica', 12, 'bold'))
        self.card_title_lbl.grid(padx=5, pady=5)

        # Utilisation d'un widget Text pour afficher le contenu de la carte
        self.card_content_txt = tk.Text(master=self.screen.frm_up_right, wrap=tk.WORD, font=('Helvetica', 18), height=10, width=50)
        self.card_content_txt.grid(padx=5, pady=5)
        self.card_content_txt.config(state=tk.DISABLED)  # Désactiver l'édition par l'utilisateur

    def deal_a_card(self, is_question):
        card = self.draw_card()
        self.display_card(card, is_question)
        
    def draw_card(self):
        selected_decks = self.dealer.get_selected_decks()
        if selected_decks:
            card = self.cards.pick_a_card(selected_decks)
            return card
        else:
            print("No decks selected")
            return None
        
    def display_card(self, card, is_question):
        self.card_content_txt.config(state=tk.NORMAL)  # Activer l'édition pour mettre à jour le texte
        self.card_content_txt.delete(1.0, tk.END)  # Effacer le contenu précédent
        if card:
            if is_question:
                card_text = f"Question: {card[1]}"
                self.btn_see_answer()
            else: 
                card_text= f"Answer: {card[2]}"
                self.btn_is_good_answer(card)
            self.card_content_txt.insert(tk.END, card_text)
        else:
            self.card_content_txt.insert(tk.END, "Sélectionnez un ou plusieurs thèmes pour tirer une carte")
        self.card_content_txt.config(state=tk.DISABLED)  # Désactiver l'édition après mise à jour

    def btn_see_answer(self):
        # Effacer le contenu de self.screen.frm_down_right
        for widget in self.screen.frm_down_right.winfo_children():
            widget.destroy()
            
        # bouton pour voir la réponse
        self.card_btn_see_answer = ttk.Button(master=self.screen.frm_down_right, text='voir la réponse', command=lambda: self.deal_a_card(is_question=False))
        self.card_btn_see_answer.grid(padx=5, pady=5)

    def btn_is_good_answer(self, card):
        # Effacer le contenu de self.screen.frm_down_right
        for widget in self.screen.frm_down_right.winfo_children():
            widget.destroy()
    
        # bouton "Bonne réponse ?"
        self.btn_good = ttk.Button(master=self.screen.frm_down_right, text='Bonne réponse ?', command=lambda: self.update_priority(card, is_good_answer=True))
        self.btn_good.grid(column=0, row=0, padx=5, pady=5)

        # bouton "Mauvaise réponse ?"
        self.btn_bad = ttk.Button(master=self.screen.frm_down_right, text='Mauvaise réponse ?', command=lambda: self.update_priority(card, is_good_answer=False))
        self.btn_bad.grid(column=1, row=0, padx=5, pady=5)

    def update_priority(self, card, is_good_answer):
        # Appeler la méthode du contrôleur pour mettre à jour la priorité de la carte
        self.cards.update_card_priority(card_id=card[0], current_priority=card[3], is_good_answer=is_good_answer)
        # Afficher la prochaine carte ou un message de confirmation
        messagebox.showinfo("Réponse", "Votre réponse est enregistrée \n Tirer une nouvelle carte")
        self.initialize_card_mat()

class DeckManagerScreen:
    def __init__(self, screen, manage_deck):
        self.screen = screen
        self.decks = manage_deck
        self.initialize_deck_manager()

    # initialisation de l'écran de gestion des paquets
    def initialize_deck_manager(self):
        print("initialize_deck_manager")
        # efface le contenu des cadres
        self.screen.clear_frm_up_left()
        self.screen.clear_frm_down_left()

        # affichage du titre
        self.deck_title_lbl = ttk.Label(master=self.screen.frm_up_left, text='Sélectionner un paquet:', font=('Helvetica', 12, 'bold'))
        self.deck_title_lbl.grid(padx=5, pady=5)

        # affichage de la liste des paquets
        self.deck_listbox = tk.Listbox(master=self.screen.frm_up_left, height=10, width=50)
        self.deck_listbox.grid(padx=5, pady=5)

        # charger la liste des paquets
        self.load_decks()
    
    def load_decks(self):
        """Charge la liste des paquets dans la Listbox."""
        self.deck_listbox.delete(0, tk.END)  # Effacer la liste existante
        decks = self.decks.get_decks()
        for deck in decks:
            self.deck_listbox.insert(tk.END, f"{deck[0]}: {deck[1]}")