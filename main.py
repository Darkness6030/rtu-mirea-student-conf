"""Консольное меню сервиса конференций."""

import argparse
from pathlib import Path

import services
from storage import load_state, save_state

ROOT = Path(__file__).resolve().parent


def main() -> None:
    """Сохранять после каждой успешной операции; не затирать повреждённый файл."""
    parser = argparse.ArgumentParser(description="Организация студенческих конференций")
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "runtime.json")
    args = parser.parse_args()
    try:
        state = load_state(args.data if args.data.exists() else ROOT / "data" / "sample.json")
    except (OSError, ValueError) as error:
        print(f"Ошибка загрузки: {error}. Исходный файл не изменён.")
        return
    menu = (
        "\n1 Списки | 2 Конференция | 3 Студент | 4 Секция | 5 Подать доклад"
        "\n6 Отменить доклад | 7 Поиск | 8 Фильтр секций | 9 Сортировка | 0 Выход"
    )
    while True:
        print(menu)
        try:
            action = input("Действие: ").strip()
            if action == "0":
                return
            if action == "1":
                for name, items in state.items():
                    print(name)
                    for item in items:
                        print(item)
                continue
            if action == "2":
                services.add_conference(
                    state,
                    input("Название: "),
                    input("Дата ГГГГ-ММ-ДД: "),
                    input("Приём до ГГГГ-ММ-ДД: "),
                    input("Место: "),
                )
            elif action == "3":
                services.add_student(state, input("ФИО: "), input("Группа: "))
            elif action == "4":
                services.add_section(
                    state,
                    input("Название: "),
                    int(input("ID конференции: ")),
                    int(input("Лимит докладов: ")),
                )
            elif action == "5":
                services.submit_talk(
                    state,
                    input("Тема: "),
                    input("Аннотация: "),
                    int(input("ID студента: ")),
                    int(input("ID секции: ")),
                )
            elif action == "6":
                services.cancel_talk(state, int(input("ID доклада: ")))
            elif action == "7":
                print(*services.search_talks(state, input("Тема содержит: ")), sep="\n")
                continue
            elif action == "8":
                print(*services.filter_sections(state, int(input("Минимум мест: "))), sep="\n")
                continue
            elif action == "9":
                print(*services.sort_sections(state), sep="\n")
                continue
            else:
                print("Неизвестная команда")
                continue
            save_state(state, args.data)
            print("Данные сохранены")
        except ValueError as error:
            print(f"Ошибка: {error}")
        except OSError as error:
            print(f"Не удалось сохранить: {error}. Завершение без дальнейших изменений.")
            return
        except (EOFError, KeyboardInterrupt):
            print("\nРабота завершена")
            return


if __name__ == "__main__":
    main()
