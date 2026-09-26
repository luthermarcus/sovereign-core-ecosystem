#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python3 sovereign_master_engine.py
python3 sovereign_terminal_dashboard.py
