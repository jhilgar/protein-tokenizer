import tokenizers as tk

class DataAnalyzer():
    characters_to_remove = ['B', 'J', 'O', 'U', 'X', 'Z']
    translation_table = {ord(x): '' for x in characters_to_remove}
    
    def get_tokenizer(tokenizer_type, params):
        if tokenizer_type == "BPE":
            tokenizer = tk.Tokenizer(tk.models.BPE(unk_token = params["unk_token"]))
            trainer = tk.trainers.BpeTrainer(
                vocab_size = params["vocab_size"], 
                special_tokens = params["special_tokens"] + [params["unk_token"]])
        else:
            raise Exception("Tokenizer type not recognized/supported.")
        
        return (tokenizer, trainer)
        
    def prune_sequences(sequences):

        return map(lambda x: x.translate(DataAnalyzer.translation_table), sequences)
    
    def train_tokenizer(tokenizer_type, params, sequences):
        tokenizer, trainer = DataAnalyzer.get_tokenizer(tokenizer_type, params)

        tokenizer.train_from_iterator(
            iterator = DataAnalyzer.prune_sequences(sequences),
            trainer = trainer
        )
        
        cls_token_id = tokenizer.token_to_id("[CLS]")
        tokenizer.post_processor = tk.processors.TemplateProcessing(
            single = "[CLS] $A",
            special_tokens = [("[CLS]", cls_token_id)]
        )

        return tokenizer.to_str(pretty = True)