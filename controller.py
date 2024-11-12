class Play:
    def __init__(self, db, deck, card):
        self.db = db
        self.deck = deck
        self.card = card
    
    def get_decks(self):
        return self.deck.get_all_decks()
    
    def close_database(self):
        self.db.close()

    def on_deck_selection(self, check_vars, thema_list):
        selected_themes = [thema_list[i] for i, var in enumerate(check_vars) if var.get() == 1]
        return selected_themes

    def get_cards_by_deck(self, selected_decks):
        selected_themes_ids = [theme[0] for theme in selected_decks]
        return self.card.get_cards_by_decks(selected_themes_ids)
    
    def pick_a_card(self, selected_decks_id):
        if not selected_decks_id:
            return None
        # sélectionne les cartes avec les paquets sélectionnés
        cards = self.get_cards_by_deck(selected_decks_id)
        # retourne la première carte
        return cards[0]