import pytest
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework.test import APIClient

from core.models import CustomUser


@pytest.fixture
def prepare_data_for_post():
    client = APIClient()
    user = mommy.make(User)
    mommy.make(CustomUser, basic_user=user)
    data = {'title': 'test', 'body': 'test'}
    client.force_authenticate(user=user)
    return client, data


@pytest.mark.django_db
def test_client_signup_email_not_valid():
    client = APIClient()
    invalid_email = 'not_valid_email.com'
    response = client.post('/sign-up/',
                           {'email': invalid_email})
    assert 500 == response.status_code


@pytest.mark.django_db
def test_client_sign_up():
    client = APIClient()
    data = {'email': 'test@gmail.com', 'name': 'Test',
            'password': 'admin', 'sex': 'M'}
    response = client.post('/sign-up/', data)

    assert 201 == response.status_code
    # Not really good idea to put more than 1 assert to test,
    # but let's briefly do it)
    assert response.data.get('token') is not None


@pytest.mark.django_db
def test_post_creation_view_unauthorized():
    client = APIClient()
    data = {'title': 'test', 'body': 'test'}
    response = client.post('/create-post/', data)

    assert ('Authentication credentials were not provided.'
            == response.data.get('detail'))


@pytest.mark.django_db
def test_post_creation_view_code(prepare_data_for_post):
    client, data = prepare_data_for_post
    response = client.post('/create-post/', data)

    assert 201 == response.status_code


@pytest.mark.django_db
def test_post_creation_view_data(prepare_data_for_post):
    client, data = prepare_data_for_post
    response = client.post('/create-post/', data)
    assert 'test' == response.data.get('title')


@pytest.mark.django_db
def test_post_creation_view_data_list(prepare_data_for_post):
    client, data = prepare_data_for_post
    response = client.post('/create-post/', data)

    assert [] == response.data.get('liked_by')


# TODO: end up tests for views :)
