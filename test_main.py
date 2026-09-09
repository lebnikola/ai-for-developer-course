from fastapi.testclient import TestClient

from main import app, answers_store

client = TestClient(app)


def _clear_store():
    """Очистка in-memory хранилища перед каждым тестом."""
    answers_store.clear()


# --- Вопросы ---

def test_get_questions():
    _clear_store()
    resp = client.get("/questions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["id"] == 1
    assert "question" in data[0]


# --- Ответы ---

def test_submit_answers():
    _clear_store()
    payload = {
        "answers": [
            {"question_id": 1, "answer": "Да"},
            {"question_id": 2, "answer": "Кошка и собака"},
            {"question_id": 3, "answer": "Мурка и Барсик"},
            {"question_id": 4, "answer": "2 часа"},
            {"question_id": 5, "answer": "Гулять в парке"},
        ]
    }
    resp = client.post("/answers", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "ok"
    assert body["saved"] == 1


def test_submit_multiple_answers():
    _clear_store()
    payload = {
        "answers": [
            {"question_id": 1, "answer": "Да"},
            {"question_id": 2, "answer": "Только кошки"},
            {"question_id": 3, "answer": "Рекс"},
            {"question_id": 4, "answer": "1 час"},
            {"question_id": 5, "answer": "Играть с мячом"},
        ]
    }
    client.post("/answers", json=payload)
    resp = client.post("/answers", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["saved"] == 2


# --- Статистика ---

def test_stats_empty():
    _clear_store()
    resp = client.get("/answers/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_submissions"] == 0
    assert data["non_empty_answers"] == 0


def test_stats_after_submission():
    _clear_store()
    payload = {
        "answers": [
            {"question_id": 1, "answer": "Да"},
            {"question_id": 2, "answer": ""},  # пустой ответ
            {"question_id": 3, "answer": "Кеша"},
            {"question_id": 4, "answer": ""},  # пустой ответ
            {"question_id": 5, "answer": "Кормить"},
        ]
    }
    client.post("/answers", json=payload)
    resp = client.get("/answers/stats")
    data = resp.json()
    assert data["total_submissions"] == 1
    assert data["non_empty_answers"] == 3  # только непустые


def test_stats_multiple_submissions():
    _clear_store()
    payload = {
        "answers": [
            {"question_id": 1, "answer": "Да"},
            {"question_id": 2, "answer": "Собака"},
            {"question_id": 3, "answer": "Шарик"},
            {"question_id": 4, "answer": "3 часа"},
            {"question_id": 5, "answer": "Играть"},
        ]
    }
    client.post("/answers", json=payload)
    client.post("/answers", json=payload)
    resp = client.get("/answers/stats")
    data = resp.json()
    assert data["total_submissions"] == 2
    assert data["non_empty_answers"] == 10


# --- Фронтенд ---

def test_serve_frontend():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Мои домашние питомцы" in resp.text
