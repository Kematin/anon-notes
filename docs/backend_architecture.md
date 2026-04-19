# Архитектура Backend приложения

## Обзор

Backend построен на **FastAPI** с использованием **многослойной архитектуры**. Приложение реализует анонимный сервис эфемерных заметок с шифрованием на стороне клиента — сервер хранит только зашифрованный текст и не имеет доступа к исходному содержимому.

## Структура проекта

```
backend/
├── src/
│   ├── app.py                  # Точка входа FastAPI
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py     # Агрегация роутеров
│   │       └── note.py         # Эндпоинты заметок
│   ├── core/
│   │   ├── config.py           # Pydantic Settings, конфигурация
│   │   ├── db.py               # Инициализация MongoDB + Beanie
│   │   ├── exceptions.py       # DatabaseError, ServiceError
│   │   └── logger.py           # Loguru, конфигурация логирования
│   ├── crud/
│   │   ├── base.py             # Обобщённый базовый CRUD класс
│   │   └── note.py             # NoteCrud
│   ├── enums/
│   │   ├── db.py               # DatabaseCreateType (MAIN | TEST)
│   │   └── note.py             # TimingForDestroy (minute|hour|day|week)
│   ├── models/
│   │   ├── base.py             # BaseDocument с UUID id
│   │   └── note.py             # Note ODM модель с TTL индексом
│   ├── schemas/
│   │   └── note.py             # Pydantic схемы запросов/ответов
│   ├── services/
│   │   └── note/
│   │       ├── note_service.py    # Оркестрация бизнес-логики
│   │       └── note_destroyer.py  # Логика удаления заметки
│   └── utils/
└── tests/
```

## Слои архитектуры

### 1. Слой представления — `api/v1/`

Обрабатывает HTTP запросы, валидирует входные данные, формирует ответы. Не содержит бизнес-логику.

**Эндпоинты** (`api/v1/note.py`):

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/notes` | Создать заметку |
| `GET` | `/api/v1/notes/{id}` | Получить заметку |
| `DELETE` | `/api/v1/notes/{id}` | Удалить заметку |

### 2. Сервисный слой — `services/note/`

Реализует бизнес-логику. Координирует работу CRUD слоя и обеспечивает операции над заметками.

**NoteService** (`note_service.py`):
```python
@classmethod
async def create_note(note_create_data: NoteCreateSchema) -> NoteCreatedResponse

@classmethod
async def get_one_note(id: UUID) -> NoteSchema

@classmethod
async def destroy_note(id: UUID) -> None
```

**NoteDestroyer** (`note_destroyer.py`) — стратегия удаления:
```python
async def destroy(self) -> None
# Роутит к мгновенному или отложенному удалению

async def _destroy_instantly(note: Note) -> None
# Удаляет немедленно если destroy_after_read=True

async def _destroy_after_timing(note: Note) -> None
# Устанавливает expires_at, MongoDB TTL индекс удалит запись автоматически
# Вычисление: now() + timedelta(minutes={1, 60, 1440, 10080})
```

### 3. Слой доступа к данным — `crud/`

Инкапсулирует операции с MongoDB через Beanie ODM.

**BaseCrud** (`crud/base.py`) — обобщённый Generic класс:
```python
class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    @classmethod
    async def create(create_data, return_type) -> Optional[Model | UUID | int]

    @classmethod
    async def update(instance_id, update_data, return_type) -> Optional[Model | UUID | int]

    @classmethod
    async def get_one(instance_id) -> ModelType  # Raises DatabaseError если не найдено

    @classmethod
    async def delete_instance(instance: ModelType) -> None

    @classmethod
    async def delete_by_id(instance_id) -> None
```

**NoteCrud** (`crud/note.py`) — тонкая обёртка:
```python
class NoteCrud(BaseCrud[Note, NoteCreateSchema, NoteUpdateSchema]):
    model = Note
```

### 4. Модели данных — `models/`

ODM модели для MongoDB через **Beanie**.

**BaseDocument** (`models/base.py`):
```python
class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)
```

**Note** (`models/note.py`):
```python
class Note(BaseDocument):
    encrypted_content: str
    expires_at: Optional[datetime] = None         # TTL поле
    timing_for_destroy: Optional[TimingForDestroy] = None
    destroy_after_read: bool = False

    class Settings:
        name = "notes_collection"
        indexes = [IndexModel([("expires_at", 1)], expireAfterSeconds=0)]
```

Механизм TTL: MongoDB автоматически удаляет документ когда `expires_at` наступает.

### 5. Схемы данных — `schemas/`

Pydantic схемы для валидации и сериализации.

```python
# NoteCreateSchema — запрос создания
class NoteCreateSchema(BaseModel):
    encrypted_content: str
    timing_for_destroy: Optional[TimingForDestroy]
    destroy_after_read: bool
    # Валидация: XOR — только один способ уничтожения

# NoteSchema — ответ при чтении
class NoteSchema(BaseModel):
    id: UUID
    encrypted_content: str
    timing_for_destroy: Optional[TimingForDestroy]
    destroy_after_read: bool

# NoteCreatedResponse — ответ при создании
class NoteCreatedResponse(BaseModel):
    created_id: UUID
```

### 6. Ядро приложения — `core/`

**Конфигурация** (`core/config.py`) — Pydantic Settings с поддержкой `.env`:
```python
class Settings:
    debug: bool           # DEBUG
    host: str             # API_HOST
    port: int             # API_PORT
    secret: SecretStr     # SECRET_KEY
    origins: List[str]    # API_ORIGINS

class DBSettings:
    host, port, name, test_db_name

class MiscSettings:
    delete_time: int      # DELETE_TIME
```

**База данных** (`core/db.py`): Motor (async MongoDB driver) + Beanie ODM. Инициализация через `init_db(type: DatabaseCreateType)`, поддерживает отдельную тестовую БД.

**Логирование** (`core/logger.py`): Loguru с двумя стоками:
- Файл: `logs/fastapi/log_{YYYY-MM-DD}.log` (INFO, ротация ежедневно, zip-архив)
- Stdout: форматированный вывод с цветами

**Исключения** (`core/exceptions.py`):
```python
class DatabaseError(Exception)   # Ошибки CRUD слоя
class ServiceError(Exception)    # Ошибки бизнес-логики
```

## Взаимодействие слоёв

```
HTTP Request
    ↓
Route (api/v1/note.py)       ← HTTP слой, валидация схем
    ↓
NoteService                  ← Бизнес-логика
    ↓
NoteCrud / NoteDestroyer     ← Доступ к данным
    ↓
Note (Beanie ODM)            ← Доменная модель
    ↓
MongoDB
```

## Поток обработки запросов

### Создание заметки

1. `POST /api/v1/notes` с `NoteCreateSchema`
2. Роут валидирует схему (XOR на способ уничтожения)
3. `NoteService.create_note()` → `NoteCrud.create()` → MongoDB
4. Ответ: `NoteCreatedResponse { created_id }`

### Получение и уничтожение заметки

1. `GET /api/v1/notes/{id}` → возвращает зашифрованный `encrypted_content`
2. Клиент расшифровывает локально своим паролем
3. `DELETE /api/v1/notes/{id}` → `NoteDestroyer.destroy()`:
   - `destroy_after_read=True` → немедленное удаление из MongoDB
   - `timing_for_destroy` задан → устанавливается `expires_at`, TTL индекс удалит запись автоматически

## Ключевые паттерны

- **Generic CRUD с Overloads**: типобезопасные возвращаемые типы (`Model | UUID | None`)
- **Async throughout**: Motor + async/await для неблокирующего I/O
- **MongoDB TTL Indexes**: авто-удаление на уровне БД без фоновых задач
- **Pydantic validation**: бизнес-правила (XOR уничтожение) проверяются на уровне схем
- **12-factor конфигурация**: Pydantic Settings + `.env` файлы
