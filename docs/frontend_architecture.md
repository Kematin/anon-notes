# Архитектура Frontend приложения

## Обзор

Frontend реализован на **React 19 + TypeScript + Vite**. Приложение обеспечивает сквозное шифрование (E2E): пароль и исходный текст заметки никогда не покидают браузер — на сервер отправляется только зашифрованное содержимое.

## Структура проекта

```
frontend/app/src/
├── App.tsx                     # Корневой компонент, RouterProvider
├── main.tsx                    # Точка входа React 19
├── router/
│   └── index.ts                # Lazy-загрузка роутов
├── views/
│   ├── MainView.tsx            # Создание заметки
│   ├── NoteView.tsx            # Просмотр заметки
│   └── Undefined.tsx           # 404 страница
├── services/
│   ├── apiClient.ts            # HTTP клиент с интерцепторами
│   ├── noteService.ts          # Оркестрация операций с заметками
│   ├── cryptoService.ts        # AES-GCM-256 шифрование
│   └── index.ts                # Синглтоны сервисов
├── components/
│   ├── base/
│   │   ├── BaseButton/
│   │   ├── BaseInput/
│   │   ├── BaseModal/          # Portal-based модальное окно
│   │   ├── BaseSelect/
│   │   ├── BaseTextArea/
│   │   └── UrlButton/
│   ├── ActionButton/           # Кнопка отправки
│   ├── PasswordModal/          # Ввод пароля
│   ├── NoteLinkModal/          # Отображение ссылки на заметку
│   ├── NoteTextField/          # Textarea для ввода/отображения заметки
│   ├── NoteStatusMessage/      # Сообщения об ошибках/статусе
│   ├── TimerSelect/            # Выбор таймера уничтожения
│   └── Image/                  # Обёртка для декоративных изображений
├── config/
│   └── api.ts                  # API_CONFIG, API_ENDPOINTS
├── constants/
│   └── timerSelection.tsx      # TimerSelection enum и опции
├── types/
│   ├── common.ts               # UUID, ApiResponse типы
│   ├── note.ts                 # PostCreateNote, GetEncryptedNote
│   └── index.ts
└── utils/
    └── logger.ts               # AppLogger синглтон
```

## Сервисный слой

### HTTP Клиент (`services/apiClient.ts`)

```typescript
class ApiClient {
    private baseURL: string   // VITE_BASE_API_URL + /api/v1
    private timeout: number   // 10 секунд (AbortController)

    async get<T>(url, options): Promise<T>
    async post<T>(url, data, options): Promise<T>
    async put<T>(url, data, options): Promise<T>
    async delete<T>(url, options): Promise<T>
    async patch<T>(url, data, options): Promise<T>

    addRequestInterceptor(interceptor)  // хук перед запросом
    addErrorInterceptor(interceptor)    // хук при ошибке
}
```

- Автоматическая JSON сериализация (кроме FormData)
- Ошибки оборачиваются в `HttpError` со статусом и данными
- Экспортируется единственный инстанс из `services/index.ts`

### Crypto Service (`services/cryptoService.ts`)

Использует **Web Crypto API** браузера (`crypto.subtle`).

```typescript
class CryptoService {
    async encryptNote(content: string, password: string): Promise<string>
    // Возвращает: base64(salt[16] + iv[12] + ciphertext)

    async decryptNote(encryptedNote: string, password: string): Promise<string>
    // Разбирает base64, извлекает salt/iv/ciphertext, расшифровывает

    private async deriveKey(password: string, salt: Uint8Array): Promise<CryptoKey>
    // PBKDF2-SHA-256, 100 000 итераций → AES-GCM-256 ключ
}
```

**Схема шифрования**:
- Алгоритм: AES-GCM 256-bit
- KDF: PBKDF2-SHA-256, 100 000 итераций
- IV: 12 случайных байт (на каждое шифрование)
- Salt: 16 случайных байт (на каждое шифрование)
- Формат payload: `base64(salt[0:16] + iv[16:28] + ciphertext[28:])`

### Note Service (`services/noteService.ts`)

Оркестрирует шифрование и HTTP запросы.

```typescript
class NoteService {
    private encryptedContentCache: Map<UUID, string>

    async createNote(note: string, timer: TimerSelectionType, password: string): Promise<UUID>
    // 1. CryptoService.encryptNote(note, password)
    // 2. POST /api/v1/notes с зашифрованным payload
    // 3. Возвращает created_id

    async fetchNote(noteId: UUID): Promise<TimerSelectionType>
    // GET /api/v1/notes/{noteId}, кеширует encrypted_content
    // Возвращает тип таймера уничтожения

    async decryptNote(noteId: UUID, password: string): Promise<string>
    // CryptoService.decryptNote(cached, password) → plaintext
    // Очищает кеш

    async deleteNote(noteId: UUID): Promise<void>
    // DELETE /api/v1/notes/{noteId}
}
```

## Роутинг

```typescript
// router/index.ts
createBrowserRouter([
    { path: "/",               lazy: () => import("MainView") },
    { path: "/note/:note_id",  lazy: () => import("NoteView") },
    { path: "*",               lazy: () => import("Undefined") },
])
```

Все роуты загружаются **lazy** — код вью подгружается только при переходе.

## Views (Страницы)

### MainView — создание заметки

```
Состояние:
  noteText: string
  selectedTimer: TimerSelectionType
  isPasswordModalOpen: boolean
  createdNoteId: UUID | null

Флоу:
  1. Пользователь вводит текст → NoteTextField
  2. Выбирает таймер → TimerSelect
  3. Нажимает «Отправить» → открывается PasswordModal
  4. Вводит пароль → NoteService.createNote()
  5. Получает createdNoteId → открывается NoteLinkModal
```

### NoteView — просмотр заметки

Использует **discriminated union** для типобезопасного state machine:

```typescript
type NoteViewState =
    | { status: "loading" }
    | { status: "awaiting_password"; timer: TimerSelectionType }
    | { status: "decrypted"; content: string; timer: TimerSelectionType }
    | { status: "invalid_password" }
    | { status: "not_found" }
    | { status: "error" }
```

```
Флоу:
  1. Монтирование страницы → NoteService.fetchNote(noteId)
  2. Зашифрованный контент кешируется → status: "awaiting_password"
  3. Пользователь вводит пароль → NoteService.decryptNote()
  4. Успех → NoteService.deleteNote() (fire-and-forget) → status: "decrypted"
  5. Отображается plaintext с подсказкой о таймере уничтожения
```

## Компоненты

### Base компоненты (`components/base/`)

Переиспользуемые UI примитивы без бизнес-логики:

| Компонент | Назначение |
|-----------|-----------|
| `BaseButton` | Кнопка с label, onClick, disabled |
| `BaseInput` | Инпут (text/password/email) |
| `BaseModal` | Portal-based модальное окно, закрытие по оверлею |
| `BaseSelect` | Кастомный дропдаун с локальным состоянием |
| `BaseTextArea` | Textarea с onKeyDown поддержкой |
| `UrlButton` | Ссылка, стилизованная под кнопку |

### Feature компоненты

Компонуются из base компонентов, содержат доменную логику:

| Компонент | Назначение |
|-----------|-----------|
| `NoteTextField` | Textarea для заметки; Ctrl/Cmd+Enter для отправки |
| `TimerSelect` | Выбор таймера уничтожения |
| `PasswordModal` | Ввод пароля; Enter подтверждает, Escape закрывает |
| `NoteLinkModal` | Отображение ссылки, копирование в буфер |
| `ActionButton` | Кнопка «Отправить» |
| `NoteStatusMessage` | Сообщение об ошибке со ссылкой на главную |

## Типы и константы

### Типы (`types/note.ts`)

```typescript
interface PostCreateNote {
    encrypted_content: string
    destroy_after_read?: boolean
    timing_for_destroy?: TimerSelectionType
}

interface GetEncryptedNote {
    id: UUID
    encrypted_content: string
    destroy_after_read?: boolean
    timing_for_destroy?: TimerSelectionType
}

interface PostCreatedNoteId {
    created_id: UUID
}
```

### Константы (`constants/timerSelection.tsx`)

```typescript
const TimerSelection = {
    Momentum: "momentum",  // уничтожить после прочтения
    Minute:   "minute",
    Hour:     "hour",
    Day:      "day",
    Week:     "week",
}

const TimerDestroyLabel: Record<TimerSelectionType, string> = {
    momentum: "после закрытия страницы",
    minute:   "через 1 минуту",
    hour:     "через 1 час",
    day:      "через 1 день",
    week:     "через 1 неделю",
}
```

## Конфигурация

```typescript
// config/api.ts
API_CONFIG = {
    PREFIX:          "/api/v1",
    BASE_URL:        import.meta.env.VITE_BASE_API_URL,
    TIMEOUT:         10000,
    DEFAULT_HEADERS: { "Content-Type": "application/json" },
}
```

Переменные окружения (`.env.prod`):
```
VITE_BASE_API_URL=https://example.com
VITE_API_HOST=example.com
VITE_DEV_MODE=false
```

## Стилизация

- **Tailwind CSS v4** — утилитарные классы
- **CSS Modules** (`.module.css`) — скопированные стили компонентов
- **Глобальные стили** — `assets/styles/index.css`, `App.css`

## Управление состоянием

Глобальных state-менеджеров нет. Используются:
- `useState` / `useEffect` — локальное состояние вью
- Сервис-синглтоны — `apiClient`, `noteService` создаются один раз
- Фабричные функции — `buildNoteService()` для dependency injection

## Поток данных

### Создание заметки

```
MainView (text, timer)
    ↓
PasswordModal (password)
    ↓
NoteService.createNote(text, timer, password)
    ├─ CryptoService.encryptNote(text, password) → encrypted
    └─ ApiClient.post("/notes", { encrypted_content, ... })
           ↓
    Backend → created_id
           ↓
NoteLinkModal (ссылка /note/{created_id})
```

### Просмотр заметки

```
NoteView (note_id из route params)
    ↓
NoteService.fetchNote(note_id)
    └─ ApiClient.get("/notes/{note_id}") → encrypted_content (кешируется)
           ↓
PasswordModal (password)
    ↓
NoteService.decryptNote(note_id, password)
    └─ CryptoService.decryptNote(cached, password) → plaintext
           ↓
NoteService.deleteNote(note_id) [fire-and-forget]
    └─ ApiClient.delete("/notes/{note_id}")
           ↓
Отображение plaintext
```

## Ключевые паттерны

- **E2E шифрование**: пароль и plaintext не покидают браузер
- **Discriminated Union State**: типобезопасный state machine в NoteView
- **Lazy Route Loading**: code-split по страницам
- **Interceptor Pattern**: ApiClient расширяем для auth/retry/logging
- **Factory Functions**: фабрики сервисов для гибкого DI
- **Portal Modals**: `createPortal` для корректного z-index
