# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A
- Simple concept explanations
- 3-question MCQ quiz generation
- Educational text summarization
- Beginner-to-advanced learning paths

## Architecture

```text
Browser
  |
  v
FastAPI (main.py)
  |
  +--> qna.py --------------------+
  +--> explanation_module.py -----+
  +--> quiz_module.py ------------+--> gemini_client.py --> Google Gemini API
  +--> summary_module.py ---------+
  +--> learning_path.py ----------+
  |
  +--> templates/index.html
  +--> static/style.css
```

The source document specifies Gemini for Q&A, summarization, quizzes, and learning paths, and LaMini-Flan-T5 for concept explanations. This implementation preserves that separation. By default, explanations use Gemini for a simpler installation; optional local LaMini-Flan-T5 mode is available through `.env`.

## Requirements

- Python 3.10+
- A Google Gemini API key

The current Google Python SDK is `google-genai`. The application uses its async `client.aio.models.generate_content(...)` interface.

## VS Code setup

### 1. Open the project

Open the `EduGenie` folder in VS Code.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-3.8-flash
USE_LOCAL_EXPLANATION=false
```

Never commit `.env` to Git.

### 5. Start the server

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Test the application

Run automated tests:

```bash
pytest -q
```

Expected result:

```text
4 passed
```

Then manually test each task in the web UI.

### Q&A

Input:

```text
Which is the largest ocean?
```

### Explain

Input:

```text
Pythagoras theorem
```

### Quiz

Input:

```text
The Earth revolves around the Sun once approximately every 365.25 days.
This movement is called revolution.
```

The application asks Gemini for exactly three questions with four options each.

### Summarize

Paste a long educational passage.

### Learning path

Input:

```text
SQL
```

## API examples

Q&A:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is photosynthesis?\"}"
```

Explanation:

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Explain Pythagoras theorem\"}"
```

Quiz:

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Water boils at 100 degrees Celsius at standard atmospheric pressure.\"}"
```

Summary:

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Paste your educational passage here.\"}"
```

Learning recommendations:

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Learn SQL\"}"
```

## Optional local LaMini-Flan-T5 explanations

The original project document identifies `MBZUAI/LaMini-Flan-T5-783M` as the local explanation model.

Because PyTorch and Transformers can be large and platform-specific, they are optional in the base installation.

1. Install the appropriate PyTorch build for your machine.
2. Install Transformers:

```bash
pip install transformers
```

3. Set:

```env
USE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first request downloads the model from Hugging Face and may take time and disk space.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Check that `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart Uvicorn after changing `.env`.

### Gemini API error

Check the API key, model availability, quota, and Google AI Studio project configuration.

### PowerShell blocks activation

Use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### Port 8000 is busy

Use:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Security notes

- The Gemini key stays server-side and is never embedded in HTML or JavaScript.
- `.env` is ignored by Git.
- Input lengths are bounded by Pydantic validation.
- The UI renders model output through escaping before inserting it into HTML.
- Quiz output is validated using Pydantic before being returned.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```
