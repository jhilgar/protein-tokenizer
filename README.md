# protein tokenizer

A small web application. Protein tokenizer fetches protein amino acid sequences from the [UniProtKB](https://www.uniprot.org) database and trains a byte pair encoding [tokenizer](https://huggingface.co/docs/tokenizers/en/index) on the results.

## installation

**requirements**

- make
- python
- virtualenv
- pip
- node

**setup**

`make install`

**tests**

`make test`

## running

- first start rabbitmq and postgres

`docker compuse up`

- run the services

`make run backend`

`make run datacollector`

`make run dataanalyzer`

`make run frontend`

## project info

todo