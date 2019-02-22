from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.serializers import CustomUserSerializer, PostSerializer
from core.models import CustomUser, Post
from core.utils import generate_token, like_or_dislike_post


class CustomSignUpView(CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')

        try:
            validate_email(email)
        except ValidationError:
            raise APIException(detail='Wrong email format {}'.format(email),
                               code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = User.objects.create_user(
            email=email,
            password=password,
            username=name,
        )

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid()

        CustomUser.objects.create(**serializer.validated_data,
                                  basic_user=user)
        token = generate_token(user)
        return Response(data={'token': token}, status=status.HTTP_201_CREATED)


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(basic_user=request.user)
        serialized.is_valid()
        new_post = Post.objects.create(**serialized.validated_data, user_id=user.id)
        return Response(data=self.serializer_class(new_post).data,
                        status=status.HTTP_201_CREATED)


class LikePostView(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = request.user
        try:
            post = Post.objects.get(id=request.data.get('post_id'))
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        post = like_or_dislike_post(post, user)
        return Response(data=self.serializer_class(post).data,
                        status=status.HTTP_200_OK)
