
# Week 3 - LLM Monitoring System

## Project Overview
This project monitors Large Language Model (LLM) API calls using Gemini and Ollama.

## Technologies Used
- Python
- Google Gemini API
- Ollama (Llama 3.2)
- MongoDB
- Pytest

## Features
1. Supports Gemini and Ollama providers.
2. Generates AI responses from user prompts.
3. Tracks input and output tokens.
4. Measures response latency.
5. Calculates API cost.
6. Logs call details in MongoDB.
7. Implements retry handling for temporary failures.
8. Includes automated cost calculator tests.

## Database
- Database: llm_monitoring
- Collection: call_logs

## How to Run

Activate virtual environment:

```powershell
venv\Scripts\activate
```

Run the application:

```powershell
python main.py
```

Run tests:

```powershell
pytest -v
```

## Test Results
4 cost calculator tests passed successfully.

## Current Status
Ollama and MongoDB logging are working.
Gemini integration is implemented, but API availability errors occurred during testing.
