import json
import os
from collections.abc import Mapping
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "questions.json"

app = FastAPI(title="Мини-анкета")

# Serve static files (CSS, JS, etc.)
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# In-memory storage: list of submissions
# Each submission: {"id": str, "answers": [{"question_id": int, "answer": str}]}
answers_store: list[dict] = []


def _load_questions() -> list[Mapping]:
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


class AnswerItem(BaseModel):
    question_id: int
    answer: str


class AnswersPayload(BaseModel):
    answers: list[AnswerItem]


@app.get("/questions", tags="survey")
def get_questions():
    """Возвращает список вопросов анкеты."""
    return _load_questions()


@app.post("/answers", status_code=201, tags="survey")
def submit_answers(payload: AnswersPayload):
    """Принимает и сохраняет ответы пользователя в памяти приложения."""
    submission = {
        "id": str(uuid4()),
        "answers": [
            {"question_id": item.question_id, "answer": item.answer}
            for item in payload.answers
        ],
    }
    answers_store.append(submission)
    return {"status": "ok", "saved": len(answers_store)}


@app.get("/answers/stats", tags="survey")
def get_stats():
    """Возвращает статистику: всего анкет и заполненных ответов."""
    total_submissions = len(answers_store)
    non_empty = sum(
        1
        for sub in answers_store
        for a in sub["answers"]
        if a["answer"].strip()
    )
    return {
        "total_submissions": total_submissions,
        "non_empty_answers": non_empty,
    }


@app.get("/")
def serve_frontend():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Frontend not found")
