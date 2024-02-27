import sqlalchemy as db
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

# initialize session on instantiation?
class DatabaseHandler():
    def __init__(self):
        self.engine = db.create_engine("sqlite+pysqlite:///:memory:", echo = True)
        self.connection = self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

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
        stmt = db.select(Dataset).where(Dataset.query.in_([query_id]))
        return self.session.scalars(stmt)
    
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