#!/usr/bin/bash

cd "$(dirname "$0")"/..
echo $PWD
source ./.venv/bin/activate
python crypto_fetcher.py -c cardano --save-db