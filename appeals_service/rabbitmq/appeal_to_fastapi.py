import requests
from typing import NoReturn


def post_appeal_to_fastapi(appeal_data: bytes) -> NoReturn:
    """
    Функция отправляет POST-запрос на сервер FastAPI
    для записи обращения в базу данных.
    """
    url = "http://localhost:8000"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        requests.post(url, data=appeal_data, headers=headers)
    except Exception as e:
        print(f"Не удалось отправить запрос на запись в базу данных: {e}")
