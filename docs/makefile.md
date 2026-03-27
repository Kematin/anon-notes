# Команды в режиме разработки

## Форматирование, тесты и проверка кода Backend

```bash
make backend_lint           # Общая проверка кода ruff
make backend_mypy           # Проверка типов mypy
make backend_test           # Запуск тестов
make backend_ci             # Полный CI цикл [lint,mypy,test]
make backend_coverage       # Проверка покрытия тестами с детальной информацией
make backend_coverage_html  # Проверка покрытия тестами + html отчет
```