import pytest
from django.contrib.auth.models import User
from model_mommy import mommy

from core.models import CustomUser, Post
from core.utils import like_or_dislike_post


@pytest.fixture
def create_data():
    post = mommy.make(Post)
    system_user = mommy.make(User)
    custom_user = mommy.make(CustomUser, basic_user=system_user)

    return post, system_user, custom_user


@pytest.mark.django_db
def test_like_or_dislike_post(create_data):
    post, system_user, custom_user = create_data

    post = like_or_dislike_post(post, system_user)

    assert list(post.liked_by.all()) == [custom_user]


@pytest.mark.django_db
def test_like_or_dislike_post_twice(create_data):
    post, system_user, custom_user = create_data

    like_or_dislike_post(post, system_user)
    post = like_or_dislike_post(post, system_user)
    assert list(post.liked_by.all()) == []
