from PyQt5.QtSql import QSqlRelationalTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt

class VariantsModel(QSqlRelationalTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable("Variants")
        self.setRelation(2, self.create_relation())  
        self.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)

    def create_relation(self):
        db = QSqlDatabase.database()
        relation = db.driver().createRelation("Variants", "category_id", "Categories", "id", "name")
        return relation

    def load_data(self):
        self.select()  
