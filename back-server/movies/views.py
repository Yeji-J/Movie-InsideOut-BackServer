from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieDetailSerializer, MovieListSerializer, MoviePopularListSerializer, RecentListSerializer, GenreSerializer
from .models import Movie, Genre

import requests


@api_view(['GET'])
def movie_create(request):

    # 장르 API -> 데이터 불러오기
    api_key = '3cd8e0319cee80069c4b85f6cf42fded'

    url = 'https://api.themoviedb.org/3/genre/movie/list'
    
    params = {
        'api_key': api_key,
        # 'language': 'KO',
    }

    response = requests.get(url, params).json()

    
    for data in response['genres']:
        genre = Genre(gerne_id = data['id'], name=data['name'])
        genre.save()


    # Movie API -> 데이터 불러오기
    page_num = [i for i in range(1, 6)]

    for num in range(5):
        
        url = 'https://api.themoviedb.org/3/movie/popular'
        
        params = {
            'api_key': api_key,
            # 'language': 'ko',
            'page': page_num[num],
            'region': 'KR'
        }

        response = requests.get(url, params).json()["results"]

        for data in response:
            data['movie_id'] = data['id']   # movie_id를 pk로 했기 때문에 중복되지 않음
            serializer = MovieDetailSerializer(data=data)
            if serializer.is_valid():                       
                
                # raise_exception=True 중복되면, 에러 발생... 제거함.

                serializer.save(genres = data['genre_ids'])
            
            else:
                continue
    
    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all().order_by('?')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# Create your views here.
@api_view(['POST', 'GET'])
def movie_detail(request, movie_id):
    # if request.method == 'POST':
    #     serializer = MovieDetailSerializer(data=request.data)
    #     if serializer.is_valid():
    #         movie = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    # else:
    movie = Movie.objects.get(movie_id=movie_id)
    serializer = MovieDetailSerializer(movie)

    genre_lst = []
    for genre_id in serializer.data['genres']:
        genre = Genre.objects.get(pk=genre_id)
        genre_lst.append(genre)

    serializer.data['genres'] = genre_lst

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