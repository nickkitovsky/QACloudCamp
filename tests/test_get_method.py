import pytest
from requests.exceptions import RequestException

from src.models import Post


def test_empty_get_request(send_get_request):
    '''Проверка ответа при пустом запросе списка всех записей,
    которые соотвествуют схеме ответа.
    При негативном исходе тест упадет с исключением'''
    posts_response = send_get_request(payload={})
    if posts_response.status_code != 200:
        raise RequestException
    assert all((Post.parse_obj(post) for post in posts_response.body))


@pytest.mark.parametrize(
    'payload',
    (
        {'id': 1},
        {'userId': 1},
        {'title': 'qui est esse'},
        {'id': 1, 'userId': 1},
        {'id': 2, 'title': 'qui est esse'},
        {'userId': 1, 'title': 'qui est esse'},
        {'id': 2, 'userId': 1, 'title': 'qui est esse'},
        {'id': '1'},
        {'userId': '1'},
    ),
    ids=str,
)
def test_selective_get_request(payload, send_get_request):
    '''Проверка ответа, при заспросе с разным количеством передаваемых
    параметров (id, userId, title).'''
    comparison_result = []
    posts_response = send_get_request(payload=payload)
    if posts_response.status_code != 200:
        raise RequestException
    payload_keys = payload.keys()
    for post in posts_response.body:
        # Проверка на валидность полученного json объекта
        Post.parse_obj(post)
        # Проверка что ключи и значения в запросе и ответе равны для каждого поста.
        # Преобразование значений id и userId в int добавлено для последних двух кейсов
        comparison_result.append(
            all(
                (
                    int(payload[key]) == post[key]
                    for key in payload_keys
                    if key in ('id', 'userId')
                )
            )
        )
    assert all(comparison_result)


@pytest.mark.parametrize(
    'payload',
    (
        {'id': ''},
        {'id': 0},
        {'id': 1.0},
        {'id': -1},
        {'id': 999999},
        {'id': 'q'},
        {'userId': ''},
        {'userId': 0},
        {'userId': 1.0},
        {'userId': -1},
        {'userId': 999999},
        {'userId': 'q'},
        {'title': ''},
        {'title': 0},
        {'title': -1},
        {'title': 999999},
        {'title': 'q'},
    ),
    ids=str,
)
def test_negative_get_request(payload, send_get_request):
    '''Проверка ответа при запросе с неверными данными. Должен вернутся пустой список'''
    posts_response = send_get_request(payload=payload)
    if posts_response.status_code != 200:
        raise RequestException
    assert all(
        (
            isinstance(posts_response.body, list),
            len(posts_response.body) == 0,
        )
    )


@pytest.mark.parametrize(
    'post_id, status_code',
    (
        (1, 200),
        (99, 200),
        ('1', 200),
        (999999, 404),
        (0, 404),
        (-1, 404),
        (1.0, 404),
        ('q', 404),
    ),
    ids=str,
)
def test_get_by_id_to_path_request(
    post_id, status_code, send_get_by_path_request
):
    '''Тест для GET запросов через path, вида ../posts/post_id'''
    response = send_get_by_path_request(post_id)
    # Валидация возвращаемого значения для запросов с ответом 200
    if response.status_code == 200:
        Post.parse_obj(response.body)
    assert response.status_code == status_code
