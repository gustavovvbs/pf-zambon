from database import create_db_and_tables
from models import Book  # Import Book to register it with SQLModel

def main():
    create_db_and_tables()
    print("Database tables created!")

if __name__ == "__main__":
    main()
