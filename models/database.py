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