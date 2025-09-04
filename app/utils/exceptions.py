class AppError(Exception):
    pass

class ConfigError(AppError):
    pass

class DatabaseError(AppError):
    pass