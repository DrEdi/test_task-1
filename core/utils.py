from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler

from core.models import CustomUser, Post


def generate_token(user):
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def like_or_dislike_post(post, user):
    user = CustomUser.objects.get(basic_user=user)

    if user in post.liked_by.all():
        post.liked_by.remove(user)
    else:
        post.liked_by.add(user)
    post.save()
    return post
