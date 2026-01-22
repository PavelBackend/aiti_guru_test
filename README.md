# Aiti Guru Test

## Описание

Проект реализован на FastAPI с использованием SQLAlchemy (async) и Alembic.
Структура разделена на слои router / service / repository.

---
- Реализованы модели, миграции бд
- Реализован эндпоинт сервиса на добавление товаров в заказ
- В корневой папке проекта находится папка `sql`, в ней представлены запросы из ТЗ и шаги оптимизации запроса 2.3.1
---

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/PavelBackend/aiti_guru_test.git
```

2. Запустите проект через Docker Compose с указанием .env файла:
```bash
docker compose -f aiti_guru_test/docker-compose.yml --env-file aiti_guru_test/.env.sample up --build -d
```

3. Примените миграции:
```bash
docker compose -f aiti_guru_test/docker-compose.yml --env-file aiti_guru_test/.env.sample run --rm app alembic upgrade head
```

## Тестирование

Документация Swagger будет по адресу:
```bash
http://localhost:8000/docs/
```

4. Остановить проект:
```bash
docker compose -f aiti_guru_test/docker-compose.yml --env-file aiti_guru_test/.env.sample down
```
(-v в последний раз добавьте в конец команды, чтобы базы данных в следующих тестовых заданиях создавались автоматически заново)
