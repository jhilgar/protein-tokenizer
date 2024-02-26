import sqlalchemy as db
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DatabaseHandler():
    def __init__(self):
        self.engine = db.create_engine("sqlite+pysqlite:///:memory:", echo = True)
        self.connection = self.engine.connect()
        Base.metadata.create_all(self.engine)

class Dataset(Base):
    __tablename__ = "dataset"

    id = db.Column(db.Integer, primary_key = True)
    fasta = db.Column(db.String())
    query = db.Column(db.Integer, db.ForeignKey("query.id"), nullable = False)

    def __repr__(self):
        return f"Dataset(id = {self.id!r}, query = {self.query!r})"
    
class Query(Base):
    __tablename__ = "query"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    raw = db.Column(db.String())

    def __repr__(self):
        return f"Query(id = {self.id!r}, name = {self.name!r})"
    
database = DatabaseHandler()