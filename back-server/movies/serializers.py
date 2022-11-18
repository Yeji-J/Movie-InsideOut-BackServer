from rest_framework import serializers
from .models import Actor, Genre, Movie, Review


class GenreNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name']


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreNameSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ('title', 'genres', 'release_date', 'vote_average', 'poster_path', 'backdrop_path', 'movie_id')
        read_only_fields = ('like_users', 'actors')


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user')


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreNameSerializer(many=True, read_only=True)
    review_set = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_users', 'actors')



# class UpcomingListSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Movie
#         fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')

