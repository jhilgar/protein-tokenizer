from components.dataanalyzer import DataAnalyzer
from components.models import TrainCommand, TokenizerResults
from components.database import DatabaseHandler
from components.api_queue import setup_app

app, router = setup_app()
datahandler = DatabaseHandler()

@router.subscriber("dataanalyzer_train")
@router.publisher("backend_tokenizer_results")
async def dataanalyzer_train_command(message: TrainCommand) -> TokenizerResults:

    sequences = datahandler.get_query_results(message.query_id)
    tokenizer_json = DataAnalyzer.train_tokenizer(message.type, message.params, sequences)

    tokenizer_results = TokenizerResults(
        destination = "backend",
        source = "dataanalyzer",
        query_id = message.query_id,
        tokenizer_json = tokenizer_json
    )
    return tokenizer_results