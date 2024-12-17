from .manage_db import ManageDB

class ManageDeck(ManageDB):
    def __init__(self, db, deck):
        super().__init__(db)
        self.deck = deck
        self.selected_decks = []
        self.selected_deck_id = None

    def get_decks(self):
        return self.deck.get_all_decks()

    def on_deck_selection(self, check_vars, thema_list):
        selected_themes = [thema_list[i] for i, var in enumerate(check_vars) if var.get() == 1]
        return selected_themes
    
    def update_selected_decks(self, check_vars):
        thema_list = self.get_decks()
        self.selected_decks = self.on_deck_selection(check_vars, thema_list)

    def get_selected_decks(self):
        return self.selected_decks
    
    def set_selected_deck_id(self, deck_id):
        self.selected_deck_id = deck_id
    
    def add_deck(self, deck_name):
        return self.deck.add_deck(deck_name)
    
    def update_deck(self, deck_id, deck_new_name):
        return self.deck.update_deck(deck_id, deck_new_name)
    
    def delete_deck(self, deck_id):
        return self.deck.delete_deck(deck_id)
