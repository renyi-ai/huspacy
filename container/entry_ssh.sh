#!/bin/bash

env | egrep -v "^(PWD=|PATH=|OLDPWD=)" | sudo tee -a /etc/environment  # Ensure env variable are set
sudo service ssh start

source /installation/hu_core_news_trf/.venv/bin/activate
exec "$@"
