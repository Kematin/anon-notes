/**
 * HTTP клиент для работы с API админ-панели
 */

/**
 * HTTP клиент для работы с API админ-панели
 */

import { API_CONFIG } from "@/config/api.ts";

export class HttpError extends Error {
  status: number;
  data: unknown;

  constructor(message: string, status: number, data?: unknown) {
    super(message);
    this.status = status;
    this.name = "HttpError";
    this.data = data;
  }
}

type RequestInterceptor = (url: string, options: RequestInit) => RequestInit | Promise<RequestInit>;
type ErrorInterceptor = (error: Error) => void | Promise<void>;

export class ApiClient {
  private baseURL: string;
  private timeout: number;
  private defaultHeaders: Record<string, string>;
  private requestInterceptors: RequestInterceptor[] = [];
  private errorInterceptors: ErrorInterceptor[] = [];

  constructor() {
    this.baseURL = API_CONFIG.BASE_URL + API_CONFIG.PREFIX;
    this.timeout = API_CONFIG.TIMEOUT;
    this.defaultHeaders = API_CONFIG.DEFAULT_HEADERS;
  }

  // MARK: Public
  /**
   * Добавить перехватчик для обработки запросов
   * @param interceptor Функция-перехватчик
   */
  addRequestInterceptor(interceptor: RequestInterceptor) {
    this.requestInterceptors.push(interceptor);
  }

  /**
   * Добавить перехватчик для обработки ошибок
   * @param interceptor Функция-перехватчик
   */
  addErrorInterceptor(interceptor: ErrorInterceptor) {
    this.errorInterceptors.push(interceptor);
  }

  /**
   * Выполнить HTTP запрос
   *
   * @param {string} url URL запроса
   * @param {RequestInit} options Опции запроса
   * @returns {Promise<T>} Обработанный ответ
   */
  private async request<T>(url: string, options: RequestInit = {}): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      let processedOptions = { ...options };

      // Применяем все перехватчики к опциям запроса
      for (const interceptor of this.requestInterceptors) {
        processedOptions = await interceptor(url, processedOptions);
      }

      // Подготавливаем заголовки
      const finalHeaders: Record<string, string> = {};

      // Добавляем заголовки по умолчанию, если не отправляем FormData - иначе будет некорретно
      // указан формат по умолчанию JSON
      if (!(processedOptions.body instanceof FormData)) {
        Object.assign(finalHeaders, this.defaultHeaders);
      }

      // Добавляем заголовки из перехватчиков и опций
      if (processedOptions.headers) {
        for (const [key, value] of Object.entries(processedOptions.headers)) {
          if (value !== undefined && typeof value === "string") {
            finalHeaders[key] = value;
          }
        }
      }

      const tartgetUrl = `${this.baseURL}${url}`;
      const response = await fetch(tartgetUrl, {
        ...processedOptions,
        headers: finalHeaders,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      return await this.handleResponse<T>(response);
    } catch (error) {
      clearTimeout(timeoutId);

      // Запускаем перехватчики ошибок
      const errorToThrow = error instanceof Error ? error : new HttpError("Неизвестная ошибка", 500);
      this.handleError(errorToThrow);

      if (error instanceof Error) {
        if (error.name === "AbortError") {
          throw new HttpError("Превышено время ожидания запроса", 408);
        }
        throw error;
      }

      throw new HttpError("Неизвестная ошибка", 500);
    }
  }

  /**
   * GET запрос
   *
   * @param {string} url URL запроса
   * @param {RequestInit & { params?: Record<string, string | number | boolean | null | undefined> }} options Опции запроса, включая query-параметры
   * @returns {Promise<T>} Обработанный ответ
   */
  async get<T>(
    url: string,
    options: RequestInit & { params?: Record<string, string | number | boolean | null | undefined> } = {},
  ): Promise<T> {
    const { params, ...restOptions } = options;
    let finalUrl = url;

    if (params) {
      const searchParams = new URLSearchParams();
      for (const key in params) {
        if (Object.prototype.hasOwnProperty.call(params, key)) {
          const value = params[key];
          if (value !== null && value !== undefined) {
            if (Array.isArray(value)) {
              value.forEach((item) => searchParams.append(key, item.toString()));
            } else {
              searchParams.append(key, value.toString());
            }
          }
        }
      }

      const queryString = searchParams.toString();
      if (queryString) {
        finalUrl = `${url}?${queryString}`;
      }
    }

    return this.request<T>(finalUrl, { ...restOptions, method: "GET" });
  }

  /**
   * POST запрос
   *
   * @param {string} url URL запроса
   * @param {unknown} data Данные запроса
   * @param {RequestInit} options Опции запроса
   * @returns {Promise<T>} Обработанный ответ
   */
  async post<T>(url: string, data?: unknown, options?: RequestInit): Promise<T> {
    let body: string | FormData | undefined;

    if (data) {
      // Если данные - это FormData, передаем их как есть
      if (data instanceof FormData) {
        body = data;
      } else {
        // Иначе сериализуем в JSON
        body = JSON.stringify(data);
      }
    }

    return this.request<T>(url, {
      ...options,
      method: "POST",
      body,
    });
  }

  /**
   * PUT запрос
   *
   * @param {string} url URL запроса
   * @param {unknown} data Данные запроса
   * @param {RequestInit} options Опции запроса
   * @returns {Promise<T>} Обработанный ответ
   */
  async put<T>(url: string, data?: unknown, options?: RequestInit): Promise<T> {
    let body: string | FormData | undefined;

    if (data) {
      // Если данные - это FormData, передаем их как есть
      if (data instanceof FormData) {
        body = data;
      } else {
        // Иначе сериализуем в JSON
        body = JSON.stringify(data);
      }
    }

    return this.request<T>(url, {
      ...options,
      method: "PUT",
      body,
    });
  }

  /**
   * DELETE запрос
   *
   * @param {string} url URL запроса
   * @param {RequestInit} options Опции запроса
   * @returns {Promise<T>} Обработанный ответ
   */
  async delete<T>(url: string, options?: RequestInit): Promise<T> {
    return this.request<T>(url, { ...options, method: "DELETE" });
  }

  /**
   * PATCH запрос
   *
   * @param {string} url URL запроса
   * @param {unknown} data Данные запроса
   * @param {RequestInit} options Опции запроса
   * @returns {Promise<T>} Обработанный ответ
   */
  async patch<T>(url: string, data?: unknown, options?: RequestInit): Promise<T> {
    let body: string | FormData | undefined;

    if (data) {
      // Если данные - это FormData, передаем их как есть
      if (data instanceof FormData) {
        body = data;
      } else {
        // Иначе сериализуем в JSON
        body = JSON.stringify(data);
      }
    }

    return this.request<T>(url, {
      ...options,
      method: "PATCH",
      body,
    });
  }

  // MARK: Private
  /**
   * Обработать ответ от сервера
   *
   * @param {Response} response Ответ от сервера
   * @returns {Promise<T>} Обработанный ответ
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let errorData: unknown | null = null;

      try {
        errorData = await response.json();
      } catch {
        // Если не удалось распарсить JSON, используем стандартный текст ошибки
      }

      const error = new HttpError("❌ Непредвиденная ошибка на сервере", response.status, errorData);
      this.handleError(error);
      throw error;
    }

    // Если статус 204 или тело ответа пустое, возвращаем null
    const contentType = response.headers.get("content-type");
    if (response.status === 204 || !contentType || !contentType.includes("application/json")) {
      return Promise.resolve(null as T);
    }

    return response.json();
  }

  /**
   * Вызвать все перехватчики ошибок
   * @param error Ошибка
   */
  private handleError(error: Error): void {
    for (const interceptor of this.errorInterceptors) {
      interceptor(error);
    }
  }
}
