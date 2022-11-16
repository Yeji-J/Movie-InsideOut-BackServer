from rest_framework import serializers
from .models import Actor, Genre, Movie, Review

# class MovieSerializer(serializers.Modelserializer):

#     class Meta:
#         model = Movie
#         fields = '__all__'
#         read_only_fields = ['like_users', 'actors']


class MovieListSerializer(serializers.Modelserializer):
    
    class Meta:
        model = Movie
        fields = ('title', 'genres', 'release_date', 'vote_average', 'poster_path', 'backdrop_path')
        read_only_fields = ('like_users', 'genres','actors')


class MovieDetailSerializer(serializers.Modelserializer):
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_users', 'genres','actors')


class MoviePopularListSerializer(serializers.Modelserializer):

    class Meta:
        model = Movie
        fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')

class UpcomingListSerializer(serializers.Modelserializer):
    
    class Meta:
        model = Movie
        fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')


class RecentListSerializer(serializers.Modelserializer):

    class Meta:
        model = Movie
        fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')
