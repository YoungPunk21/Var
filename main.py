import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTableView, QComboBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlRelation
from database import create_connection, init_db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRUD операции с Variants")
        self.setGeometry(100, 100, 800, 600)

        
        create_connection()
        init_db()

        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Введите название варианта")
        layout.addWidget(self.name_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Введите описание варианта")
        layout.addWidget(self.description_input)

        
        self.category_combo = QComboBox(self)
        self.fill_categories()
        layout.addWidget(self.category_combo)

        
        self.add_button = QPushButton("Добавить вариант", self)
        self.add_button.clicked.connect(self.add_variant)
        layout.addWidget(self.add_button)

        
        self.table_view = QTableView(self)
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable('Variants')

        
        self.model.setRelation(2, QSqlRelation("Categories", "id", "name"))
        self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.model.select()

        
        self.table_view.setModel(self.model)
        self.table_view.setItemDelegate(QSqlRelationalDelegate(self.table_view))

        layout.addWidget(self.table_view)

        
        self.delete_button = QPushButton("Удалить выбранный вариант", self)
        self.delete_button.clicked.connect(self.delete_variant)
        layout.addWidget(self.delete_button)

        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def fill_categories(self):
        """Заполняем комбобокс только тремя категориями"""
        query = QSqlQuery("SELECT id, name FROM Categories WHERE name IN ('Электроника', 'Одежда', 'Продукты')")
        while query.next():
            self.category_combo.addItem(query.value(1), query.value(0))  

    def add_variant(self):
        """Добавление нового варианта в базу данных"""
        name = self.name_input.text()
        description = self.description_input.text()
        category_id = self.category_combo.currentData()  

        if name and description:
            query = QSqlQuery()
            query.prepare("INSERT INTO Variants (name, description, category_id) VALUES (?, ?, ?)")
            query.addBindValue(name)
            query.addBindValue(description)
            query.addBindValue(category_id)

            if not query.exec_():
                print("Ошибка при добавлении варианта:", query.lastError().text())
            else:
                print("Вариант добавлен!")
                self.model.select()  
        else:
            print("Введите имя и описание варианта.")

    def delete_variant(self):
        """Удаление выбранного варианта из базы данных"""
        selected_row = self.table_view.currentIndex().row()
        if selected_row >= 0:
            variant_id = self.model.record(selected_row).value("id")
            query = QSqlQuery()
            query.prepare("DELETE FROM Variants WHERE id = ?")
            query.addBindValue(variant_id)

            if not query.exec_():
                print("Ошибка при удалении варианта:", query.lastError().text())
            else:
                print("Вариант удален!")
                self.model.select()  
        else:
            print("Выберите вариант для удаления")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
