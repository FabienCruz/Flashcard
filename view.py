import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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
    
    def set_managers(self, deck_screen, card_screen):
        """
        Stocke les références vers les écrans de gestion.
        
        Args:
            deck_screen: Instance de DeckManagerScreen
            card_screen: Instance de CardManagerScreen
        """
        self.deck_screen = deck_screen
        self.card_screen = card_screen

    def show_deck_manager(self):
        """Affiche l'écran de gestion des paquets."""
        if self.deck_screen:
            self.deck_screen.initialize_deck_manager()

    def show_card_manager(self):
        """Affiche l'écran de gestion des cartes."""
        if self.card_screen:
            self.card_screen.initialize_card_manager()

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
                text=deck, 
                variable=var,
                command=lambda v=self.check_vars: self.manage_screen.manage_deck.update_selected_decks(v)
                )
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    def show_manager_screen(self):
        self.screen.clear_all_frames()
        self.manage_screen.show_manager_screen()

class CardMat:
    """

    La classe CardMat est responsable de l'affichage du 'tapis de jeu'.
    Elle affiche les cartes, face question, face réponse, les boutons d'actions.

    """

    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.decks = manage_screen.manage_deck
        self.cards = manage_screen.manage_card

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
        selected_decks = self.decks.get_selected_decks()
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
    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.manage_screen = manage_screen
        self.decks = manage_screen.manage_deck

    # initialisation de l'écran de gestion des paquets
    def initialize_deck_manager(self):
        # efface le contenu des cadres
        self.screen.clear_frm_up_left()
        self.screen.clear_frm_down_left()

        # affichage du titre
        self.deck_title_lbl = ttk.Label(master=self.screen.frm_up_left, text='Sélectionner un paquet:', font=('Helvetica', 12, 'bold'))
        self.deck_title_lbl.grid(padx=5, pady=5)

        # affichage de la liste des paquets
        self.deck_listbox = tk.Listbox(master=self.screen.frm_up_left, height=15, width=15)
        self.deck_listbox.grid(padx=5, pady=5)

        # charger la liste des paquets
        self.load_decks()

        # affichage des boutons
        self.btn_delete_deck = ttk.Button(master=self.screen.frm_down_left, text='Supprimer', command=self.delete_deck, width=11)
        self.btn_delete_deck.pack(side=tk.TOP, padx=5, pady=5)
        self.btn_update_deck = ttk.Button(master=self.screen.frm_down_left, text='Modifier', command=self.update_deck, width=11)
        self.btn_update_deck.pack(side=tk.TOP, padx=5, pady=5)
        self.btn_add_deck = ttk.Button(master=self.screen.frm_down_left, text='Ajouter', command=self.add_deck, width=11)
        self.btn_add_deck.pack(side=tk.TOP, padx=5, pady=5)

        # Lier l'événement de sélection de la Listbox à la méthode on_deck_select
        self.deck_listbox.bind('<<ListboxSelect>>', self.on_deck_select)

    def load_decks(self):
        """Charge la liste des paquets dans la Listbox."""
        self.deck_listbox.delete(0, tk.END)  # Effacer la liste existante
        decks = self.decks.get_decks()
        for deck in decks:
            self.deck_listbox.insert(tk.END, f"{deck[0]}: {deck[1]}")
    
    def get_selected_deck_id(self):
        """Récupère le paquet sélectionné dans la Listbox."""
        try:
            index = self.deck_listbox.curselection()[0]
            deck = self.deck_listbox.get(index)
            deck_id = deck.split(":")[0]
            return deck_id
        except IndexError:
            return None
    
    def on_deck_select(self, event):
        """Méthode appelée lorsqu'un paquet est sélectionné dans la Listbox."""
        deck_id = self.get_selected_deck_id()
        if deck_id is not None:
            self.manage_screen.update_card_manager(deck_id)

    def add_deck(self):
        """Ajoute un paquet."""
        deck_name = simpledialog.askstring("Ajouter un paquet", "Nom du paquet:")
        if deck_name:
            self.decks.add_deck(deck_name)
            self.load_decks()

    def delete_deck(self):
        """Supprime un paquet."""
        deck_id = self.get_selected_deck_id()
        if deck_id:
            security = messagebox.askyesno("Avertissement", "Voulez-vous vraiment supprimer ce paquet ?")
            if security:
                self.decks.delete_deck(deck_id)
                self.load_decks()
        else:
            messagebox.showinfo("Supprimer un paquet", "Sélectionnez un paquet à supprimer")

    def update_deck(self):
        """Modifie un paquet."""
        deck_id = self.get_selected_deck_id()
        if deck_id:
            new_name = simpledialog.askstring("Modifier un paquet", "Nouveau nom du paquet :")
            if new_name:
                self.decks.update_deck(deck_id, new_name)
                self.load_decks()  # Recharger la liste des paquets
        else:
            messagebox.showwarning("Avertissement", "Sélectionnez un paquet à modifier")

class CardManagerScreen:
    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.card_manager = manage_screen.manage_card

    def initialize_card_manager(self):
        # Efface le contenu des cadres
        self.screen.clear_frm_up_right()
        self.screen.clear_frm_down_right()
        # affichage du titre
        self.card_title_lbl = ttk.Label(master=self.screen.frm_up_right, text='Gestion des cartes:', font=('Helvetica', 12, 'bold'))
        self.card_title_lbl.grid(padx=5, pady=5)
        # affiche liste des cartes (questions)
        self.card_listbox = tk.Listbox(master=self.screen.frm_up_right, height=15, width=50)
        self.card_listbox.grid(padx=5, pady=5)
        # affichage des boutons
        self.btn_delete_card = ttk.Button(master=self.screen.frm_down_right, text='Supprimer', command=self.delete_card, width=11)
        self.btn_delete_card.pack(side=tk.TOP, padx=5, pady=5)
        self.btn_update_card = ttk.Button(master=self.screen.frm_down_right, text='Modifier', command=self.update_card, width=11)
        self.btn_update_card.pack(side=tk.TOP, padx=5, pady=5)
        self.btn_add_card = ttk.Button(master=self.screen.frm_down_right, text='Ajouter', command=self.add_card, width=11)  
        self.btn_add_card.pack(side=tk.TOP, padx=5, pady=5)

        # Lier l'événement de sélection de la Listbox à la méthode on_card_select
        self.card_listbox.bind('<<ListboxSelect>>', self.on_card_select)

    # --- chargement des cartes en fonctions du paquet sélectionné
    def load_cards(self, deck_id):
        """Charge la liste des cartes dans la Listbox."""
        self.card_listbox.delete(0, tk.END)
        cards = self.card_manager.get_cards_by_deck_id(deck_id)
        for card in cards:
            self.card_listbox.insert(tk.END, f"{card[0]}: {card[1]}")
    
    # --- récupère l'identifiant de la carte sélectionnée
    def on_card_select(self, event):
        """Méthode appelée lorsqu'une carte est sélectionnée dans la Listbox."""
        card_id = self.get_selected_card_id()
        if card_id is not None:
            print(f"Carte sélectionnée : {card_id}")
    
    def get_selected_card_id(self):
        """Récupère l'identifiant de la carte sélectionnée dans la Listbox."""
        try:
            index = self.card_listbox.curselection()[0]
            card = self.card_listbox.get(index)
            card_id = card.split(":")[0]
            return card_id
        except IndexError:
            return None

    # --- méthodes pour gérer les cartes (CRUD)
    def add_card(self):
        return print("Ajouter une carte")
    
    def delete_card(self):
        return print("Supprimer une carte")
    
    def update_card(self):
        return print("Modifier une carte")

