import enum

import requests

from src.models import Response

URL = 'https://jsonplaceholder.typicode.com/posts'


class Method(enum.Enum):
    GET = 'get'
    GET_BY_PATH = 'get by path id'
    POST = 'post'
    DELETE = 'delete'


def _send_request(
    method: Method,
    payload: dict[str, str | int] | int,
) -> Response | None:
    match method:
        case Method.GET:
            response = requests.get(URL, params=payload)
        case Method.GET_BY_PATH:
            response = requests.get(f'{URL}/{payload}')
        case Method.POST:
            response = requests.post(URL, json=payload)
        case Method.DELETE:
            response = requests.delete(f'{URL}/{payload}')
        case _:
            raise requests.exceptions.RequestException(
                'Unknow method (use Method instance GET, POST, DELETE).'
            )
    try:
        return Response(status_code=response.status_code, body=response.json())
    # Собрал возможные исключения в кортеж, а не обрабатываю отдельно т.к. разработка
    # клиента к api не основная задача
    except (
        requests.exceptions.JSONDecodeError,
        ConnectionError,
        ValueError,
        NameError,
    ):
        raise requests.RequestException()


def send_get_request(payload: dict):
    return _send_request(Method.GET, payload)


def send_get_by_path_request(payload: dict):
    return _send_request(Method.GET_BY_PATH, payload)


def send_post_request(payload: dict):
    return _send_request(Method.POST, payload)


def send_delete_request(payload: int):
    return _send_request(Method.DELETE, payload)
