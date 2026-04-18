/**
 * Конфигурация API эндпоинтов.
 */

const API_PREFIX = "/api/v1";
const API_BASE_URL = import.meta.env.VITE_BASE_API_URL;

export const API_CONFIG = {
  PREFIX: API_PREFIX,
  BASE_URL: API_BASE_URL,

  // Таймаут для HTTP запросов в миллисекундах
  TIMEOUT: 10000,

  // Заголовки по умолчанию
  DEFAULT_HEADERS: {
    "Content-Type": "application/json",
  },
} as const;

export const API_ENDPOINTS = {
  NOTES: "/notes",
} as const;
