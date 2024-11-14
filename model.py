import sqlite3

class Database:
    """
    Classe gérant la connexion à la base de données SQLite.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Design Pattern Singleton : retourne une seule instance de la classe.
        pour éviter de créer plusieurs connexions à la base de données.
        
        Retourne l'instance existante si elle existe, sinon en crée une nouvelle.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name="flashcards.db"):
        """
        Initialise la connexion à la base de données.
        
        Args:
            db_name (str): Nom du fichier de base de données
        """
        self.connexion = sqlite3.connect(db_name)
        # Activer les foreign keys
        self.connexion.execute("PRAGMA foreign_keys = ON")

    def close(self):
        """Ferme la connexion à la base de données."""
        self.connexion.close()

class Deck:
    """
    Classe gérant les opérations sur les decks de cartes.
    """
    def __init__(self, db):
        """
        Initialise la gestion des decks.
        
        Args:
            db (Database): Instance de la classe Database
        """
        self.connexion = db.connexion
        self.create_table()

    def create_table(self):
        """Crée la table des decks si elle n'existe pas."""
        try:
            with self.connexion:
                self.connexion.execute("""
                    CREATE TABLE IF NOT EXISTS decks (
                        deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thema TEXT NOT NULL UNIQUE
                    );
                """)
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table 'decks' : {e}")

    def add_deck(self, thema):
        """
        Ajoute un nouveau deck.
        
        Args:
            thema (str): Le thème du deck
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        try:
            with self.connexion:
                self.connexion.execute(
                    "INSERT INTO decks (thema) VALUES (?);", 
                    (thema,)
                )
                return True
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du deck : {e}")
            return False

    def get_all_decks(self):
        """
        Récupère tous les decks de la base de données.
        
        Returns:
            list: Liste de tuples (deck_id, thema)
        """
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT deck_id, thema FROM decks ORDER BY deck_id;")
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des decks : {e}")
            return []

    def get_deck_by_id(self, deck_id):
        """
        Récupère un deck spécifique par son ID.
        
        Args:
            deck_id (int): L'ID du deck à récupérer
            
        Returns:
            tuple: (deck_id, thema) ou None si non trouvé
        """
        try:
            cur = self.connexion.cursor()
            cur.execute(
                "SELECT deck_id, thema FROM decks WHERE deck_id = ?;",
                (deck_id,)
            )
            return cur.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du deck {deck_id} : {e}")
            return None

class Card:
    """
    Classe gérant les opérations sur les cartes.
    """
    def __init__(self, db):
        """
        Initialise la gestion des cartes.
        
        Args:
            db (Database): Instance de la classe Database
        """
        self.connexion = db.connexion
        self.create_table()

    def create_table(self):
        """Crée la table des cartes si elle n'existe pas."""
        try:
            with self.connexion:
                self.connexion.execute("""
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
        """
        Ajoute une nouvelle carte dans la base de données.
        
        Args:
            question (str): La question de la carte
            answer (str): La réponse de la carte
            priority (int): La priorité de la carte
            deck_id (int): L'ID du deck auquel appartient la carte
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        try:
            with self.connexion:
                # Vérifier que le deck existe
                cur = self.connexion.cursor()
                cur.execute("SELECT deck_id FROM decks WHERE deck_id = ?;", (deck_id,))
                if not cur.fetchone():
                    print(f"Erreur : le deck_id {deck_id} n'existe pas")
                    return False
                
                # Ajouter la carte
                cur.execute("""
                    INSERT INTO cards (question, answer, priority, deck_id)
                    VALUES (?, ?, ?, ?);
                """, (question, answer, priority, deck_id))
                return True
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de la carte : {e}")
            return False

    def get_all_cards(self):
        """
        Récupère toutes les cartes de la base de données.
        
        Returns:
            list: Liste de tuples (card_id, question, answer, priority, deck_id)
        """
        try:
            cur = self.connexion.cursor()
            cur.execute("""
                SELECT card_id, question, answer, priority, deck_id 
                FROM cards 
                ORDER BY priority DESC;
            """)
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes : {e}")
            return []

    def get_cards_by_decks(self, deck_ids):
        """
        Récupère les cartes correspondant aux decks sélectionnés.
        
        Args:
            deck_ids (list): Liste des deck_id sélectionnés
            
        Returns:
            list: Liste de tuples (card_id, question, answer, priority, deck_id, thema)
        """
        try:
            cur = self.connexion.cursor()
            placeholders = ','.join('?' * len(deck_ids))
            query = f"""
                SELECT c.card_id, c.question, c.answer, c.priority, c.deck_id, d.thema
                FROM cards c
                JOIN decks d ON c.deck_id = d.deck_id
                WHERE c.deck_id IN ({placeholders})
                ORDER BY c.priority ASC;
            """
            cur.execute(query, deck_ids)
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes par deck : {e}")
            return []

    def update_card_priority(self, card_id, new_priority):
        """
        Met à jour la priorité d'une carte.
        
        Args:
            card_id (int): L'ID de la carte à modifier
            new_priority (int): La nouvelle priorité
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            with self.connexion:
                cur = self.connexion.cursor()
                cur.execute("""
                    UPDATE cards 
                    SET priority = ? 
                    WHERE card_id = ?;
                """, (new_priority, card_id))
                print(f"card_id: {card_id}, new_priority: {new_priority}")
                return cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de la priorité : {e}")
            return False