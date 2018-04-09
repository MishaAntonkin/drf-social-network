from rest_framework import serializers
from rest_framework import validators
from .models import *


class PostSerializer(serializers.HyperlinkedModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='user-api:users-detail', many=False, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='user-api:posts-detail')

    class Meta:
        model = Post
        fields = ('url', 'user', 'text', 'title', 'likes')

    def get_likes(self, obj):
        print(obj.likes.count())
        return obj.likes.count()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=25, write_only=True)
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='user-api:posts-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='user-api:users-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'posts')

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=False, view_name='user-api:users-detail', queryset=User.objects.all())
    post = serializers.HyperlinkedRelatedField(many=False, view_name='user-api:posts-detail', queryset=Post.objects.all())
    url = serializers.HyperlinkedIdentityField(view_name='user-api:likes-detail')

    class Meta:
        model = UserLike
        fields = ('url', 'user', 'post', 'active')

