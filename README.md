## Быстрый старт

### Требования

- Свободные порты на хосте: **8501**, **8080**, **9095**, **5430**, **2181**
- Модель `catboost_fraud.cbm` в папке `fraude_detector/models/`

### Запуск

```bash
# 1. Создать файл окружения с кредами Postgres
cp .env.example .env

# 2. Собрать и поднять весь стек
docker compose up -d --build
```

Дождаться, пока сервисы поднимутся:

```bash
docker compose ps
```

После старта доступны:

| Сервис | URL |
|--------|-----|
| Streamlit (приложение) | <http://localhost:8501> |
| Kafka UI | <http://localhost:8080> |
| Postgres | `localhost:5430` |

## Структура проекта

```
.
├── fraude_detector/            # ML-сервис
│   ├── models/
│   │   └── catboost_fraud.cbm  # предобученная модель
│   ├── preprocessing.py        # генерация признаков
│   ├── inference.py            # загрузка модели и предсказание
│   ├── kafka_broker.py         # consume transactions → score → produce scoring
│   ├── logger_config.py        # настройка loguru
│   ├── main.py                 # точка входа
│   └── Dockerfile
├── interface/                  # Streamlit UI
│   ├── app.py                  # интерфейс
│   ├── kafka_broker.py         # отправка транзакций / чтение scoring
│   ├── db.py                   # чтение результатов из Postgres
│   ├── logger_config.py
│   └── Dockerfile
├── db_writer/                  # scoring → Postgres
│   ├── kafka_broker.py         # consume scoring → запись в БД
│   ├── db.py                   # подключение и схема таблицы scores
│   ├── logger_config.py
│   ├── main.py
│   └── Dockerfile
├── docker-compose.yaml
├── .env.example                # шаблон переменных окружения
└── README.md
```