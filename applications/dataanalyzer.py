import datetime
import tokenizers as tk

from components.models import TrainCommand, TokenizerResults
from components.database import DatabaseHandler
from components.api_queue import setup_app

class DataAnalyzer():
    def get_tokenizer(type, params):
        if type == 'BPE':
            tokenizer = tk.Tokenizer(tk.models.BPE(unk_token = params["unk_token"]))
            trainer = tk.trainers.BpeTrainer(
                vocab_size = params["vocab_size"], 
                special_tokens = params["special_tokens"] + [params["unk_token"]])
        
        return (tokenizer, trainer)
        
    def prune_sequences(sequences):
        characters_to_remove = ['B', 'J', 'O', 'U', 'X', 'Z']
        translation_table = {ord(x): '' for x in characters_to_remove}

        sequences = map(lambda x: x.translate(translation_table), sequences)
        return sequences
        

app, router = setup_app()
datahandler = DatabaseHandler()

@router.subscriber("dataanalyzer_train")
@router.publisher("backend_tokenizer_results")
async def dataanalyzer_train_command(message: TrainCommand) -> TokenizerResults:
    tokenizer, trainer = DataAnalyzer.get_tokenizer(message.type, message.params)
    sequences = datahandler.get_query_results(message.query_id)
    tokenizer.train_from_iterator(
        iterator = DataAnalyzer.prune_sequences(sequences),
        trainer = trainer
    )

    cls_token_id = tokenizer.token_to_id("[CLS]")
    tokenizer.post_processor = tk.processors.TemplateProcessing(
        single = "[CLS] $A",
        special_tokens = [("[CLS]", cls_token_id)]
    )

    tokenizer_results = TokenizerResults(
        destination = "backend",
        source = "dataanalyzer",
        query_id = message.query_id,
        tokenizer_json = tokenizer.to_str(pretty = True)
    )
    print(tokenizer_results)
    return tokenizer_results