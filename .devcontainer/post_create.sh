#!/bin/bash

# Install Python packages
pip install -r requirements.txt
python -m textblob.download_corpora

