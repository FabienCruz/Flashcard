from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# initialise la base
Base = declarative_base()

class Database:
    def __init__(self):
        # Création de l'engine pour la base de données
        self.engine = create_engine("sqlite+pysqlite:///flashcards.db", echo=True)
        # Création des tables dans la base de données
        Base.metadata.create_all(self.engine)
        # Création de la session pour interagir avec la base de données
        self.Session = sessionmaker(bind=self.engine)

    def open_session(self):
        # Méthode pour créer une nouvelle session
        return self.Session()
    
    def close_session(self, session):
        try:
            session.close()
        except Exception as e:
            print(f"Erreur lors de la fermeture de session: {e}")

    def add(self, obj):
        session = self.open_session()
        try:
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout de l'objet : {e}")
        finally:
            self.close_session(session)

    def delete(self, obj):
        session = self.open_session()
        try:
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de la suppression de l'objet : {e}")
        finally:
            self.close_session(session)

    def add_card(self, question, answer, deck_id):
        new_card = Card(question=question, answer=answer, deck_id=deck_id)
        self.add(new_card)

    def add_deck(self, thema):
        new_deck = Deck(thema=thema)
        self.add(new_deck)

    def delete_card(self, card_id):
        session = self.open_session()
        card = Card.get_card(session, card_id)
        if card:
            self.delete(card)
        else:
            print(f"Aucune card trouvée avec l'ID {card_id}")
        self.close_session(session)

    def delete_deck(self, deck_id):
        session = self.open_session()
        deck = Deck.get_deck(session, deck_id)
        if deck:
            self.delete(deck)
        else:
            print(f"Aucun deck trouvé avec l'ID {deck_id}")
        self.close_session(session)
      

class Card(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    deck_id = Column(Integer, ForeignKey("decks.deck_id", ondelete="CASCADE"))
    # Relation avec 'decks'
    deck = relationship("Deck", back_populates="cards")

    @classmethod
    def get_card(cls, session, card_id):
        return session.query(cls).filter_by(card_id=card_id).first()

    @classmethod
    def get_all_cards(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_cards_by_deck(cls, session, deck_id):
        return session.query(cls).filter_by(deck_id=deck_id).all()

class Deck(Base):
    __tablename__ = 'decks'
    deck_id = Column(Integer, primary_key=True)
    thema = Column(String, nullable=False)
    # Relation avec la table 'cards' (relation une-à-plusieurs)
    cards = relationship("Card", back_populates="deck", cascade="all, delete, delete-orphan")

    @classmethod
    def get_deck(cls, session, deck_id):
        return session.query(cls).filter_by(deck_id=deck_id).first()
    
    @classmethod
    def get_all_decks(cls, session):
        return session.query(cls).all()