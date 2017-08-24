#!/bin/bash

virtualenv --no-site-packages --distribute .env && \
  source .env/bin/activate && \
  pip install -r requirements.txt

echo "In dev mode the dev.sh script will set GAMEFILE_TREE and GAMEFILE_UPLOADS"
