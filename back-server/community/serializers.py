from rest_framework import serializers
from movies.serializers import MovieTitleSerializer
from .models import Post, Comment


class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    movie = MovieTitleSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'like_users', )


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post', 'user')


class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    movie = MovieTitleSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'like_users')

