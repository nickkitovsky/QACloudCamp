import pytest

from src.models import Post

'''
Если считать что endpoint работает верно, тест будет именно такой.
Учитывая что DELETE запрос не влияет на хранимые данные изменяет данные, его 
тестирование усложняется. Можно получать с помощью GET запроса список всех id постов, 
и уже сравнивать допустимость передаваемого post_id с ним, но endpoint должен возвращать
более вразумительный ответ. При любом запросе в теле возвращается  {}, поэтому проверять
его нет смысла.
'''


@pytest.mark.parametrize(
    'post_id, status_code',
    ((1, 200), (9999, 200), ('q', 200), (-1, 200), (0, 200), ('', 404)),
    ids=str,
)
def test_selective_delete_request(post_id, status_code, send_delete_request):
    '''Endpoint при передаче любого параметра отдает ответ 200.
    Только при передаче пустого параметра возвращается 404.
    '''
    response = send_delete_request(post_id)
    assert response.status_code == status_code


def test_delete_request_created_post(send_delete_request, send_post_request):
    '''Создание записи с помощью POST запроса, и последующее его удаление.'''
    raw_post = {
        'title': 'foo',
        'body': 'bar',
        'userId': 1,
    }
    created_post = send_post_request(payload=raw_post)
    post = Post.parse_obj(created_post.body)
    response = send_delete_request(post.id)
    assert response.status_code == 200
