import tkinter as tk
from tkinter import ttk, messagebox

class CardManagerScreen:
    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.manage_screen = manage_screen
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
            return card_id

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
        """Affiche le formulaire pour ajouter une carte."""
        deck_id = self.manage_screen.manage_deck.selected_deck_id
        CardForm(self.screen, self.card_manager, deck_id, card=None, callback=lambda: self.load_cards(deck_id))
    
    def update_card(self):
        """Affiche le formulaire pour modifier une carte."""
        deck_id = self.manage_screen.manage_deck.selected_deck_id
        card_id = self.get_selected_card_id()
        if card_id:
            card = self.card_manager.get_card_by_id(card_id)
            CardForm(self.screen, self.card_manager, deck_id, card)
        else:
            messagebox.showinfo("Modifier une carte", "Sélectionnez une carte à modifier")

    def delete_card(self):
        card_id = self.get_selected_card_id()
        if card_id:
            security = messagebox.askyesno("Avertissement", "Voulez-vous vraiment supprimer cette carte ?")
            if security:
                self.card_manager.delete_card(card_id)
                self.load_cards(self.manage_screen.manage_deck.selected_deck_id)
        else:
            messagebox.showinfo("Supprimer une carte", "Sélectionnez une carte à supprimer")
