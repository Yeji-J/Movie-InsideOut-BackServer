from rest_framework import serializers
from .models import Actor, Genre, Movie, Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ('gerne_id',)


class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('title', 'genres', 'release_date', 'vote_average', 'poster_path', 'backdrop_path')
        read_only_fields = ('like_users', 'genres','actors')


class MovieDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_users', 'genres', 'actors')


class MoviePopularListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')

class UpcomingListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')


class RecentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')
