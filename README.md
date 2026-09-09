# Мини-анкета — Домашнее задание

Простое full-stack приложение «Мини-анкета» на тему **«Мои домашние питомцы»**.

## Технологический стек

| Компонент  | Технология              |
| ---------- | ----------------------- |
| Backend    | Python + FastAPI        |
| Frontend   | React (CDN), HTML, JS   |
| Тесты      | pytest                  |
| Зависимости| uv, httpx               |

## Структура проекта

```
.
├── main.py              # FastAPI приложение
├── questions.json       # Вопросы анкеты (5 шт.)
├── test_main.py         # pytest-тесты
├── static/
│   ├── index.html       # Frontend (React CDN)
│   └── style.css        # Стили
├── pyproject.toml       # Зависимости и метаданные
└── README.md
```

## Установка и запуск

### Предварительные требования

- **Python 3.10+**
- **uv** — быстрый менеджер пакетов для Python

Установка uv (если ещё не установлен):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux / macOS
# или
# PowerShell: iwr -useb https://astral.sh/uv/install.ps1 | iex   # Windows
```

### На Mac (macOS)

```bash
# 1. Клонируйте репозиторий
cd ai-for-dev/homework1

# 2. Создайте виртуальное окружение
uv venv

# 3. Запустите сервер
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Откройте в браузере
open http://localhost:8000
```

### На Linux

```bash
# 1. Перейдите в директорию проекта
cd ai-for-dev/homework1

# 2. Создайте виртуальное окружение и установите зависимости
uv venv
source .venv/bin/activate
uv pip install -r /dev/null   # зависимости из pyproject.toml

# 3. Запустите сервер
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Откройте в браузере
xdg-open http://localhost:8000
```

### На Windows

```powershell
# 1. Перейдите в директорию проекта
cd ai-for-dev\homework1

# 2. Создайте виртуальное окружение и установите зависимости
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r .\pyproject.toml

# 3. Запустите сервер
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Откройте в браузере
start http://localhost:8000
```

> **Примечание для Windows:** если PowerShell блокирует выполнение скриптов,
> выполните `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` перед активацией venv.

## Использование

1. Откройте приложение в браузере по адресу `http://localhost:8000`.
2. Заполните 5 вопросов анкеты о домашних питомцах.
3. Нажмите **«Отправить»**.
4. Всплывающее окно покажет **«Спасибо!»** или **«Ошибка отправки»**.
5. Статистика (всего анкет / заполнено ответов) обновляется автоматически каждые 15 секунд.

## API

| Метод    | Endpoint        | Описание                           |
| -------- | --------------- | ---------------------------------- |
| GET      | `/questions`    | Список вопросов анкеты             |
| POST     | `/answers`      | Отправка ответов пользователя      |
| GET      | `/answers/stats`| Статистика: всего анкет и ответов  |

## Тестирование

```bash
uv run pytest test_main.py -v
```

### Покрытие тестами

- `test_get_questions` — проверка получения списка вопросов
- `test_submit_answers` — отправка одного пакета ответов
- `test_submit_multiple_answers` — множественные отправки
- `test_stats_empty` — статистика при пустом хранилище
- `test_stats_after_submission` — статистика после одной отправки (подсчёт непустых)
- `test_stats_multiple_submissions` — статистика после нескольких отправок
- `test_serve_frontend` — проверка раздачи фронтенда
