/**
 * Логгер для приложения.
 * Логирует сообщения в консоль только в режиме разработки или на localhost.
 * Использует синглтон для обеспечения единого экземпляра логгера.
 */
type LogPayload = string | number | boolean | object | null | undefined | unknown;

interface LoggerConfig {
  developmentMode?: boolean;
}

export class AppLogger {
  private static instance: AppLogger;
  private readonly isDev: boolean;

  private constructor(config: LoggerConfig = {}) {
    this.isDev = config.developmentMode ?? import.meta.env.VITE_DEV_MODE;
  }

  public static getInstance(config?: LoggerConfig): AppLogger {
    if (!AppLogger.instance) {
      AppLogger.instance = new AppLogger(config);
    }
    return AppLogger.instance;
  }

  public info(message: string, data?: Record<string, LogPayload>) {
    if (this.isDev || window.location.hostname === "localhost") {
      console.info(message, data || "");
    }
  }

  public log(message: string, data?: Record<string, LogPayload>) {
    if (this.isDev || window.location.hostname === "localhost") {
      console.log(message, data || "");
    }
  }

  public warn(message: string, data?: Record<string, LogPayload>) {
    if (this.isDev || window.location.hostname === "localhost") {
      console.warn(message, data || "");
    }
  }

  public debug(message: string, data?: Record<string, LogPayload>) {
    if (this.isDev || window.location.hostname === "localhost") {
      console.log(message, data || "");
    }
  }

  public error(message: string, data?: Record<string, LogPayload>) {
    if (this.isDev || window.location.hostname === "localhost") {
      console.error(message, data || "");
    }
  }
}

export const logger = AppLogger.getInstance();
