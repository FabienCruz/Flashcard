import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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
        self.deck_title_lbl = ttk.Label(master=self.screen.frm_up_left, text='Gérer un paquet:', font=('Helvetica', 12, 'bold'))
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
            self.deck_listbox.insert(tk.END, f"{deck[0]}:{deck[1]}")
    
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
            self.manage_screen.manage_deck.set_selected_deck_id(deck_id)
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