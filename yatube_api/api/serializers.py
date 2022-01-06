from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Follow, Group, User

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(many=True, required=False)
    
    class Meta:
        fields = '__all__'
        model = Post

    class Meta:
        fields = '__all__'
        model = Comment

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
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

        if Follow.objectsfilter(user=follower, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.'
            )

        if follower == following:
            raise serializers.ValidationError(
                'Подписка на самого себя невозможна.'
            )

        return data

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow