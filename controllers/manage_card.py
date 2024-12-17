import random
from .manage_db import ManageDB

class ManageCard(ManageDB):
    def __init__(self, db, card):
        super().__init__(db)
        self.card = card
    
    def get_card_by_id(self, card_id):
        return self.card.get_card_by_id(card_id)
    
    def get_cards_by_deck(self, selected_decks):
        selected_themes_ids = [theme[0] for theme in selected_decks]
        return self.card.get_cards_by_decks(selected_themes_ids)
    
    def get_cards_by_deck_id(self, deck_id):
        return self.card.get_cards_by_deck_id(deck_id)

    def order_cards_by_priority(self, cards):
        return sorted(cards, key=lambda x: x[3])
    
    def shuffle_cards(self, cards):
        if not cards:
            return None
        random.shuffle(cards)
        return cards
    
    def pick_a_card(self, selected_decks_id):
        if not selected_decks_id:
            return None
        # sélectionne les cartes avec les paquets sélectionnés
        # cards est une liste de tuples [(id, question, answer, priority, deck_id, deck_name)]
        cards = self.get_cards_by_deck(selected_decks_id)
        # mélange les cartes et les trie par priorité
        cards = self.shuffle_cards(cards)
        cards = self.order_cards_by_priority(cards)
        return cards[0]
      
    def update_card_priority(self, card_id, current_priority, is_good_answer):
        new_priority = current_priority + 1 if is_good_answer else 1
        return self.card.update_card_priority(card_id, new_priority)

    def add_card(self, question, answer, priority, deck_id):
        return self.card.add_card(question=question, answer=answer, priority=1, deck_id=deck_id)

    def update_card(self, card_id, question, answer):
        return self.card.update_card(card_id, question, answer)

    def delete_card(self, card_id):
        return self.card.delete_card(card_id)
