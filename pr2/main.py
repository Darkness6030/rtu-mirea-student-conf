"""Запуск: python -m pr2.main."""

from console import run
from json_store import load_json, save_json
from pr2 import service

if __name__ == "__main__":
    run(service, load_json, save_json, "runtime-pr2.json")
