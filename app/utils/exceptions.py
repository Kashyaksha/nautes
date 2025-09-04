class AppError(Exception):
    """Базовое приложение исключение"""
    pass

class ConfigError(AppError):
    """Ошибка конфигурации (например, отсутствует TELEGRAM_TOKEN)"""
    pass

class DatabaseError(AppError):
    """Ошибка взаимодействия с БД"""
    pass
