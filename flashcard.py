from dataclasses import dataclass, field

@dataclass
class Card:
    id_card = int
    question: str
    answer: str
    priority: int = 1

    def __post_init__(self):
        # Assure que la priorité est toujours entre 1 et 3
        if not (1 <= self.priority <= 3):
            raise ValueError("La priorité doit être comprise entre 1 et 3")

    def upgrade_priority(self):
        # Augmente la priorité à 3 sinon 1
        self.priority = self.priority + 1 if self.priority < 3 else 1
        return self.priority

    def reset_priority(self) -> int:
        self.priority = 1
        return self.priority

    
@dataclass
class Deck:
    thema: str
    cards: list = field(default_factory=list)

    def add_card(self, card: Card):
        self.cards.append(card)
        return f"deck {self.thema} get card {card.question}"

    def show_cards(self):
        pass

    def remove_card(self, card):
        pass

    def shuffle(self):
        pass

@dataclass
class Screen():
    header =  str
    content = str
    action = str
