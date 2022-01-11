from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Follow, Group, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer

    class Meta:
        fields = '__all__'
        model = Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name',)
        model = User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        follower = self.context['request'].user
        following = data['following']

        if follower == following:
            raise serializers.ValidationError(
                'Подписка на самого себя невозможна.'
            )

        return data

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['follower', 'following'],
                message='Вы уже подписаны на этого автора.'
            )
        ]