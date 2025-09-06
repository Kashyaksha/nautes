class AppError(Exception):
    """Базовое исключение приложения"""
    pass

class ConfigError(AppError):
    """Ошибка конфигурации (например, отсутствует TELEGRAM_TOKEN)"""
    pass

class DatabaseError(AppError):
    """Ошибка взаимодействия с БД"""
    pass
