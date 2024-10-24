class Deal:
    def __init__(self, deck, card):
        self.deck = deck
        self.card = card
    
    def selected_thema(self):
        all_decks = self.deck.get_all_decks()
        return all_decks

    def pick_a_card():
        pass

    def show_question():
        pass

    def show_answer():
        pass

class ManageCards:
    pass

class ManageDecks:
    pass

"""
# controller.py
class TaskController:
    def __init__(self, model):
        self.model = model

    def add_task(self, description):
        self.model.add_task(description)

    def show_tasks(self):
        return self.model.get_tasks()
"""