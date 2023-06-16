from requests.exceptions import RequestException

from src.models import Post

'''
raw_post из примера на главной страницы. На нем и будем тестировать.
Но endpoint возвращает код 201, если ему отправить любые данные, видимо в силу того, что
это тестовый endpoint с ограниченным функционалом

'''

raw_post = {
    'title': 'foo',
    'body': 'bar',
    'userId': 1,
}


def test_post_request_single_post(send_post_request, send_delete_request):
    '''Тест запроса из примера на сайте {'title': 'foo', 'body': 'bar', 'userId': 1,}'''
    response = send_post_request(raw_post)
    if response.status_code != 201:
        raise RequestException()
    # Валидируем правильность ответа парсингом в объект Post
    post = Post.parse_obj(response.body)
    post_dict = post.dict(by_alias=True)
    # Удаляем созданный пост (хоть данный endpoint его и не сохранил, но за собой нужно
    # прибираться).
    send_delete_request(post.id)
    assert all((raw_post[key] == post_dict[key] for key in raw_post.keys()))
