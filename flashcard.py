from dataclasses import dataclass

@dataclass
class Flashcard:
    question: str
    answer: str
    priority: int = 1 # default value

    def update_priority(self):
        # to remake considering test result
        if self.priority < 3:
            self.priority += 1
        return self.priority

    def add_to_deck(self, deck):
        pass
    
@dataclass
class Deck:
    thema: str
    flashcards: list

    def add_flashcard(self, flashcard):
        pass

    def remove_flashcard(self, flashcard):
        pass

    def shuffle(self):
        pass
