from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtSql import QSqlQueryModel, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt
import sys
from database import create_connection, init_db, check_table_structure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.db = create_connection()
        if self.db:
            init_db()

        self.setWindowTitle('CRUD Variants Application')
        self.setGeometry(100, 100, 600, 400)

        
        self.model = QSqlTableModel()
        self.model.setTable('Variants')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        
        self.view = QTableView()
        self.view.setModel(self.model)

        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Enter variant name')
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText('Enter variant description')

        
        self.add_button = QPushButton('Add Variant', self)
        self.add_button.clicked.connect(self.add_variant)

        self.remove_button = QPushButton('Remove Variant', self)
        self.remove_button.clicked.connect(self.remove_variant)

        
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_variant(self):
        name = self.name_input.text()
        description = self.description_input.text()

        if name and description:
            query = QSqlQuery()
            query.prepare('INSERT INTO Variants (name, description) VALUES (?, ?)')
            query.addBindValue(name)
            query.addBindValue(description)

            if not query.exec_():
                print("Ошибка при добавлении варианта:", query.lastError().text())
            else:
                print("Вариант добавлен!")
                self.model.select()
        else:
            print("Введите имя и описание варианта.")

    def remove_variant(self):
        selected_row = self.view.selectionModel().selectedRows()

        if selected_row:
            row = selected_row[0].row()
            id_value = self.model.index(row, 0).data()

            query = QSqlQuery()
            query.prepare('DELETE FROM Variants WHERE id = ?')
            query.addBindValue(id_value)

            if not query.exec_():
                print("Ошибка при удалении варианта:", query.lastError().text())
            else:
                print(f"Вариант с ID {id_value} удален!")
                self.model.select()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
