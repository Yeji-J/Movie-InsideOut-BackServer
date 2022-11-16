from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieDetailSerializer, MovieListSerializer, MoviePopularListSerializer, RecentListSerializer
from .models import Movie


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all().order_by('?')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# Create your views here.
@api_view(['POST', 'GET'])
def movie_detail(request, movie_id):
    if request.method == 'POST':
        serializer = MovieDetailSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        movie = Movie.objects.get(movie_id=movie_id)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)



@api_view(['GET'])
def movie_popular(request):
    movies = Movie.objects.all().order_by('-vote_count')[:10]
    serializer = MoviePopularListSerializer(movies, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def movie_recent(request):
    movies = Movie.objects.all().order_by('-release_date')[:10]
    serializer = RecentListSerializer(movies, many=True)
    return Response(serializer.data)