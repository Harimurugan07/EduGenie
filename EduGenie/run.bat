@echo off
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements-minimal.txt
if not exist .env copy .env.example .env
uvicorn main:app --reload
