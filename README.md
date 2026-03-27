# Анонимные записки

Сервис для создания анонимных записок с уничтожением после прочтения

Python, FastAPI, MongoDB, Beanie, Loguru

## Ссылки

- [Репозиторий](https://github.com/Kematin/anon-notes)
## Документация

- [1. ТЗ](docs/technical_specifications.md)
- [2. Дизайн]
- [3. Makefile]
- Backend
	- [Архитектура](docs/backend_architecture.md)

## Основные возможности

- Создание и получение анонимных записок
- Шифрование записок сквозным путем
- Расшифровка записок только на стороне клиента
- Автоматическое удаление записок через определенный интервал

## Технологии

- Backend: FastAPI, MongoDB
- Frontend: React, TypeScript, WebCrypto
- Инфраструктура: Docker, Docker Compose, Nginx

## Установка и запуск

### Требования

- Docker и Docker Compose
- Make (для удобства команд)

### Локальная разработка

1. Клонировать репозиторий
```bash
git clone https://github.com/Kematin/anon-notes.git
cd anon-notes
```

2. Создать и настроить переменные окружения `.env` файлы для backend и frontend директорий по `.env.example` шаблону
3. Запустить проект, используя Make:
```bash
make start_dev
```

4. ? Или запустить все процессы отдельно
```bash
uv sync
npm i

// Backend
uv run uvicorn src.app:app --reload
uv run celery -A worker worker --loglevel=info

// Frontend
npm run dev
```
### Тесты бэкенда

Тесты запускаются командой `make test`. После запуска тестов можно увидеть отчет о покрытие кода тестами в файле `htmlcov/index.html`

## Разработка

Структура проекта
```
anon-notes/
├── backend/
├── frontend/
├── docs/
├── nginx/
```
## Руководство по запуску проекта

### Режим разработки
- Работает Vite dev server с Hot Module Replacement (HMR)
- Используется HTTP без SSL
- Монтируются локальные папки для быстрой разработки
- Включен режим отладки

### Режим продакшена
- Используется собранная production-версия фронтенда
- Настроен SSL через Let's Encrypt
- Оптимизированные настройки nginx
- Отключен режим отладки
- Минимальные права доступа для безопасности