from fastapi import FastAPI

from components.database.databasehandler import DatabaseHandler

handler = DatabaseHandler()

app = FastAPI()

@app.get("/")
def read_root():
    return {"num_database_entries": str(handler.get_num_dataset())}