# database.py
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def create_connection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('variants.db')
    if not db.open():
        print("Не удалось подключиться к базе данных!")
        return None
    print("База данных успешно подключена!")
    return db

def init_db():
    query = QSqlQuery()

    
    query.exec_("CREATE TABLE IF NOT EXISTS Categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")

    
    query.exec_("CREATE TABLE IF NOT EXISTS Variants (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES Categories(id))")

    print("База данных и таблицы созданы или уже существуют!")
