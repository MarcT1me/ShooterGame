from glm import *
from functools import wraps
from typing import Any, Self, Optional
from Engine.data.config import MainData
from Engine.app import App


def increment_creator():
    value = 0
    while True:
        yield value
        value += 1


def devOnly(decorate: bool = True, *, _default: Any = None):
    """ Outer decorator taking the _default parameter. """
    
    def empty_func(*args, **kwargs):
        """ Placeholder function returning default value. """
        return _default
    
    def inner_deco(func):
        """ Inner decorator altering wrapped function behavior based on the global flag. """
        
        @wraps(func)  # Preserve metadata for debugging and introspection
        def inner(*args, **kwargs):
            """ the final function """
            if decorate and MainData.IS_RELEASE:
                return empty_func(*args, **kwargs)  # Return a placeholder function
            return func(*args, **kwargs)  # Normal function execution
        
        return inner
    
    return inner_deco


class Catch:
    def try_func(self, *args, func, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as exc:
            self.__exit__(type(exc), exc, None)
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc_val, _) -> True:
        if exc_type is not None:
            # Проверяем, является ли исключение экземпляром класса Exception или его подкласса
            if issubclass(exc_type, Exception):
                App.failures.append(exc_val)
            else:
                # Если исключение не является экземпляром класса Exception или его подкласса,
                # то создаем новое исключение и добавляем его в список
                App.failures.append(Exception(f"Неожиданное исключение: {exc_val}"))
        return True  # Возвращаем True, чтобы исключение не было пере-выброшено
