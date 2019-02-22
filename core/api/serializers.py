from rest_framework import serializers

from core.models import CustomUser, Post


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('sex', 'basic_user', 'id')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'liked_by', 'body', 'user_id')
        read_only_fields = ('liked_by', )
