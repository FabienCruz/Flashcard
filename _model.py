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
            print("Erreur lors de la fermeture de session: {e}")

class Card(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    deck_id = Column(Integer, ForeignKey("decks.deck_id", ondelete="CASCADE"))
    # Relation avec 'decks'
    deck = relationship("Deck", back_populates="cards")

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
    def get_all_decks(cls, session):
        return session.query(cls).all()