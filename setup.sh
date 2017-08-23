#!/bin/bash

virtualenv --no-site-packages --distribute .env && \
  source .env/bin/activate && \
  pip install -r requirements.txt

echo "Set GAMEFILE_TREE to the top of the gamefile dir tree"
