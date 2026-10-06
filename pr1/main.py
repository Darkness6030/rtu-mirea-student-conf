"""Проверка подачи доклада в секцию студенческой конференции."""

from datetime import date


def has_free_slot(capacity: int, submitted: int) -> bool:
    """Проверить наличие места до добавления нового доклада."""
    return capacity > 0 and 0 <= submitted < capacity


def is_submission_open(deadline: date, today: date | None = None) -> bool:
    """Последний день приёма включается в допустимый интервал."""
    return (today or date.today()) <= deadline


def submission_status(available: bool, open_now: bool) -> str:
    return "Доклад можно подать" if available and open_now else "Подача недоступна"


def main() -> None:
    try:
        submitted = int(input("Количество докладов в секции (всего 10 мест): "))
        deadline = date.fromisoformat(input("Приём до (ГГГГ-ММ-ДД): "))
        if submitted < 0:
            raise ValueError("Количество не может быть отрицательным")
        print(submission_status(has_free_slot(10, submitted), is_submission_open(deadline)))
    except ValueError as error:
        print(f"Ошибка ввода: {error}")


if __name__ == "__main__":
    main()
