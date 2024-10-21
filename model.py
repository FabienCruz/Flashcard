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

    def add_card(self, question, answer, priority, deck_id):
        new_card = Card(question=question, answer=answer, priority=priority, deck_id=deck_id)
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
    priority = Column(Integer, default=1)
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
    
    """
import sqlite3

class Database:
    def __init__(self, db_name="flashcards.db"):
        self.conn = sqlite3.connect(db_name)

    def close(self):
        self.conn.close()

class Deck:
    def __init__(self, db):
        self.conn = db.conn
        self.create_table()

    def create_table(self):
        try:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS decks (
                        deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thema TEXT NOT NULL
                    );
                """)
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table 'decks' : {e}")

    def add_deck(self, thema):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO decks (thema) VALUES (?);", (thema,))
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du deck : {e}")

    def get_all_decks(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM decks;")
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des decks : {e}")
            return []

class Card:
    def __init__(self, db):
        self.conn = db.conn
        self.create_table()

    def create_table(self):
        try:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS cards (
                        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        priority INTEGER DEFAULT 1,
                        deck_id INTEGER,
                        FOREIGN KEY(deck_id) REFERENCES decks(deck_id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table 'cards' : {e}")

    def add_card(self, question, answer, priority, deck_id):
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO cards (question, answer, priority, deck_id)
                    VALUES (?, ?, ?, ?);
                """, (question, answer, priority, deck_id))
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de la carte : {e}")

    def get_all_cards(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM cards;")
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes : {e}")
            return []

# Exemple d'utilisation
if __name__ == "__main__":
    db = Database()

    # Gestion des decks
    deck_manager = Deck(db)
    deck_manager.add_deck("Mathématiques")
    decks = deck_manager.get_all_decks()
    print(f"Decks : {decks}")

    # Gestion des cartes
    card_manager = Card(db)
    if decks:
        deck_id = decks[0][0]  # Le premier deck trouvé
        card_manager.add_card("Qu'est-ce que Python ?", "Un langage de programmation", 1, deck_id)

    cards = card_manager.get_all_cards()
    print(f"Cartes : {cards}")

    db.close()

"""