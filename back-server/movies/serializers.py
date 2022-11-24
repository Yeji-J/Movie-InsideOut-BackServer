from rest_framework import serializers
from .models import Actor, Genre, Movie, Review


class GenreNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name']


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ['name']


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreNameSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_users', 'actors', 'user_picks', 'watched_users', 'user')


class MovieTitleSerializer(serializers.ModelSerializer):
    genres = GenreNameSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'poster_path', 'genres', 'watched_users')


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    movie = MovieTitleSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user',)


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreNameSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    # reviews = ReviewSerializer(many=True, read_only=True)
    # review_count = serializers.IntegerField(source='reviews.count', read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_users', 'user_picks', 'watched_users', 'reviews')



# class UpcomingListSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Movie
#         fields = ('title', 'genres','vote_average', 'poster_path', 'backdrop_path')

