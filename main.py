"""Консольная версия ПР3. Запуск: python main.py."""

import services
from console import run
from storage import load_state, save_state

if __name__ == "__main__":
    run(services, load_state, save_state)
