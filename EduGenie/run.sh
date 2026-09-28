#!/usr/bin/env bash
set -e
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements-minimal.txt
if [ ! -f .env ]; then cp .env.example .env; fi
uvicorn main:app --reload
