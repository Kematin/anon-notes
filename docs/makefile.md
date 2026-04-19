# Команды Makefile

## Режим разработки

```bash
make start_dev          # Запустить dev-окружение (docker compose up --build)
make stop_dev           # Остановить dev-окружение
make remove_dev         # Остановить и удалить volumes dev-окружения
make logs_backend_dev   # Логи backend-контейнера (dev)
make logs_frontend_dev  # Логи frontend-контейнера (dev)
```

## Продакшн

```bash
make start_prod         # Запустить prod-окружение (docker compose up --build)
make stop_prod          # Остановить prod-окружение
make remove_prod        # Остановить и удалить volumes prod-окружения
make logs_backend       # Логи backend-контейнера (prod)
make logs_nginx         # Логи nginx-контейнера (prod)
```

## Форматирование, тесты и проверка кода Backend

```bash
make backend_lint           # Общая проверка кода ruff
make backend_mypy           # Проверка типов mypy
make backend_test           # Запуск тестов
make backend_ci             # Полный CI цикл [lint, test, mypy]
make backend_coverage       # Проверка покрытия тестами с детальной информацией
make backend_coverage_html  # Проверка покрытия тестами + html отчет
```

## Проверка кода Frontend

```bash
make front_types        # Проверка типов TypeScript (tsc --noEmit)
make front_lint         # Проверка кода ESLint
make front_build        # Сборка production-бандла
make front_ci           # Полный CI цикл [types, lint, build]
```
