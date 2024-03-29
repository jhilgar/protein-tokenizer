import os

import sqlalchemy as db
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

class DatabaseHandler():
    def __init__(self):
        url = os.getenv("DATABASE_URL")
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://')

        self.engine = db.create_engine(url, echo = True)

        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        
        self.connection = self.engine.connect()
        self.session = Session(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def insert_query(self, raw):
        query = Query(name = "test", raw = raw)
        self.session.add(query)
        self.session.commit()
        return query.id

    def insert_dataset(self, query_id, dataset):
        dataset = Dataset(fasta = dataset, query = query_id)
        self.session.add(dataset)
        self.session.commit()

    def get_num_query_results(self, query_id):
        return self.session.scalar(
            db.select(db.func.count(Dataset.query)).
            filter(Dataset.query == query_id)
        )
    
    def get_query_results(self, query_id):
        stmt = db.select(Dataset.fasta).where(Dataset.query == query_id)
        return self.session.scalars(stmt).all()
    
    def get_num_dataset(self):
        return self.session.scalar(
            db.select(db.func.count(Dataset.id))
        )

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