#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
screen -dmS psp_api python3 psp_api.py