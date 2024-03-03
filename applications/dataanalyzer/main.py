from fastapi import Response
import prometheus_client as pc

from components.dataanalyzer import DataAnalyzer
from components.models import TrainCommand, TokenizerResults
from components.database import DatabaseHandler
from components.api_queue import setup_app

app, router = setup_app()
datahandler = DatabaseHandler()

num_train_commands = pc.Counter("num_train_commands", "The number of training requests received from the backend.")

@router.subscriber("dataanalyzer_train")
@router.publisher("backend_tokenizer_results")
async def dataanalyzer_train_command(message: TrainCommand) -> TokenizerResults:
    num_train_commands.inc()
    sequences = datahandler.get_query_results(message.query_id)
    tokenizer_json = DataAnalyzer.train_tokenizer(message.type, message.params, sequences)

    tokenizer_results = TokenizerResults(
        destination = "backend",
        source = "dataanalyzer",
        query_id = message.query_id,
        tokenizer_json = tokenizer_json
    )
    return tokenizer_results

@app.get("/metrics")
async def metrics():
    return Response(content = pc.generate_latest(), media_type = "text/plain")