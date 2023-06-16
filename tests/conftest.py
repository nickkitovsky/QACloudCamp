import pytest

import src.client


@pytest.fixture
def send_get_request():
    return src.client.send_get_request


@pytest.fixture
def send_get_by_path_request():
    return src.client.send_get_by_path_request


@pytest.fixture
def send_post_request():
    return src.client.send_post_request


@pytest.fixture
def send_delete_request():
    return src.client.send_delete_request
