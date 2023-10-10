#!/bin/bash

echo
echo $(date '+%c')

cd /Users/o_chang/Code/hg_scheduler

source bin/activate

# pip3 install -r requirements.txt

python3 main.py

deactivate

echo