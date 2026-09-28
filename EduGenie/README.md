# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project document.

## Features

- Ask academic/general questions
- Explain complex concepts simply
- Generate exactly 3 MCQs with 4 options each
- Summarize educational text
- Generate a beginner-to-advanced learning path with resources and practice
- Responsive browser UI
- REST API with Pydantic validation
- Current Google GenAI SDK integration
- Optional local `MBZUAI/LaMini-Flan-T5-783M` explanation model
- Automated API tests with mocked AI calls

## Architecture

```text
Browser
  |
  | POST /qa, /explain, /quiz, /summarize, /learn/recommendations
  v
FastAPI
  |
  +--> routers/api.py
  |
  +--> GeminiClient --------> Google Gemini API
  |
  +--> LocalExplanationModel -> Hugging Face LaMini (optional)
  |
  +--> Feature modules
       |-- qna.py
       |-- explanation_module.py
       |-- quiz_module.py
       |-- summary_module.py
       `-- learning_path.py
```

## Project tree

```text
EduGenie/
├── main.py
├── config.py
├── schemas.py
├── requirements.txt
├── requirements-minimal.txt
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── ai/
│   ├── __init__.py
│   ├── gemini_client.py
│   └── local_explainer.py
├── modules/
│   ├── __init__.py
│   ├── explanation_module.py
│   ├── learning_path.py
│   ├── qna.py
│   ├── quiz_module.py
│   └── summary_module.py
├── routers/
│   ├── __init__.py
│   └── api.py
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    ├── __init__.py
    └── test_api.py
```

## VS Code setup

### 1. Prerequisites

Install Python 3.10 or newer.

### 2. Open the project

Open the `EduGenie` folder in VS Code.

### 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

For the normal Gemini-first setup:

```bash
pip install -r requirements-minimal.txt
```

If you want the local LaMini explanation model:

```bash
pip install -r requirements.txt
```

The full requirements include PyTorch and Transformers. The LaMini checkpoint is large, so it is intentionally loaded only when selected.

### 5. Configure Gemini

Copy `.env.example` to `.env`.

Windows:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Put your Google AI Studio API key in:

```env
GEMINI_API_KEY=your_real_key_here
```

The application reads the key only on the backend. Do not put it in `static/app.js` or HTML.

### 6. Run

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Local LaMini explanation mode

The supplied document specifies `MBZUAI/LaMini-Flan-T5-783M` for concept explanation.

To enable it:

```env
EXPLANATION_PROVIDER=local
LOCAL_EXPLANATION_ENABLED=true
```

Then start the server normally.

The first explanation request downloads the model from Hugging Face and caches it. Subsequent runs use the local cache.

If the local model is unavailable, set:

```env
EXPLANATION_PROVIDER=gemini
```

for a simpler setup.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Which is the largest ocean?\"}"
```

### Explanation

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"topic\":\"Pythagoras theorem\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"The water cycle describes evaporation, condensation, precipitation, and collection.\"}"
```

### Summary

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Paste a long educational paragraph here.\"}"
```

### Learning path

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"topic\":\"SQL\",\"level\":\"beginner\",\"weeks\":8}"
```

## Testing

Tests do not require a real Gemini API key because AI calls are mocked.

```bash
pytest -q
```

Expected result:

```text
5 passed
```

## Docker

Create `.env` first, then:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000
```

The default Docker image uses the minimal requirements and therefore uses Gemini for explanations.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Add a valid key to `.env` and restart Uvicorn.

### Gemini model not available

Change `GEMINI_MODEL` in `.env` to a model available to your Google AI Studio/API account.

### Local model is slow

That is expected on CPU. Use Gemini mode for a lightweight development experience.

### PowerShell blocks activation

Run PowerShell as a user who can execute local scripts, or use:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

## Security notes

- Never commit `.env`.
- Never expose the Gemini API key in frontend JavaScript.
- Input lengths are bounded.
- AI output for quizzes and learning paths is schema-validated.
- The app does not store user prompts or generated answers in a database.
