import pytest

import tokenizers as tk

from components.dataanalyzer import DataAnalyzer

def test_prune_sequences():
    weird_input = 5
    weird_sequences = ['ZZLYDVAEBYAGVSYQTJVSRVV']
    good_sequences = ['LYDVAEYAGVSYQTVSRVV']

    assert list(DataAnalyzer.prune_sequences(weird_sequences)) == good_sequences

    with pytest.raises(Exception):
        DataAnalyzer.prune_sequences(weird_input)

def test_get_tokenizer():
    good_tokenizer_type = "BPE"
    good_params = { "unk_token": "[UNK]", "vocab_size": 30, "special_tokens": ["[CLS]"] }
    tokenizer, trainer = DataAnalyzer.get_tokenizer(good_tokenizer_type, good_params)

    assert isinstance(tokenizer, tk.Tokenizer)
    assert isinstance(trainer, tk.trainers.Trainer)

    weird_tokenizer_type = "ASS"
    with pytest.raises(Exception):
        tokenizer, trainer = DataAnalyzer.get_tokenizer(weird_tokenizer_type, good_params)

    weird_params = { "some_token" }
    with pytest.raises(Exception):
        tokenizer, trainer = DataAnalyzer.get_tokenizer(good_tokenizer_type, weird_params)

def test_train_tokenizer():
    good_sequences = ['LYDVAEYAGVSYQTVSRVV']
    good_tokenizer_type = "BPE"
    good_params = { "unk_token": "[UNK]", "vocab_size": 30, "special_tokens": ["[CLS]"] }

    tokenizer_string = DataAnalyzer.train_tokenizer(good_tokenizer_type, good_params, good_sequences)
    assert "[UNK]" in tokenizer_string

    no_cls_params = { "unk_token": "[UNK]", "vocab_size": 30, "special_tokens": ["[ASS]"] }
    with pytest.raises(Exception):
        DataAnalyzer.train_tokenizer(good_tokenizer_type, no_cls_params)