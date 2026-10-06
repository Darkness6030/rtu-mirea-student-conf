"""Наследование, полиморфизм, staticmethod и пользовательский декоратор."""

from functools import wraps


def traced(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"Вызов {function.__name__}")
        return function(*args, **kwargs)

    return wrapper


class Notification:
    @staticmethod
    def channel():
        return "консоль"

    def render(self):
        return "Получена заявка на доклад"


class CancellationNotification(Notification):
    def render(self):
        return "Доклад отменён"


@traced
def show(notification):
    print(notification.render())


if __name__ == "__main__":
    for notice in (Notification(), CancellationNotification()):
        show(notice)
