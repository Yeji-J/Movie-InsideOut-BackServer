from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieDetailSerializer, MovieListSerializer, ReviewSerializer
from .models import Movie, Genre, Review

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
            # if Movie.objects.filter(movie_id=data['id']):
            #     print(">>>>>>>>>>>>>>>>> failure")
            # else:
            #     print(data['title'])
            #     print(">>>>>>>>>>>>>>>>> seccess")
            data['movie_id'] = data['id']   # movie_id를 pk로 했기 때문에 중복되지 않음
            serializer = MovieDetailSerializer(data=data)
            if serializer.is_valid():                                       
                # raise_exception=True 중복되면, 에러 발생... 제거함.
                serializer.save(genres = data['genre_ids'])
            
            else:
                continue


    # Recent      
    url = 'https://api.themoviedb.org/3/movie/now_playing'
    
    params = {
        'api_key': api_key,
        # 'language': 'ko',
        'page': 1,
        'region': 'KR'
    }

    response = requests.get(url, params).json()["results"]

    for data in response:
        data['movie_id'] = data['id']
        serializer = MovieDetailSerializer(data=data)
        if serializer.is_valid():                                       
            serializer.save(genres = data['genre_ids'])
        
        else:
            continue

    # print('>>>>>>>>>>>>>>>>>>>>>', Movie.objects.distinct().values('title').count())

    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
def movie_list(request):
    
    # print('>>>>>>>>>>>>>>>>>>>>', request.GET.get('sorted'))
    # >>>>>>>>>>>>>>>>>>>> None
    # >>>>>>>>>>>>>>>>>>>> popular
    
    # sort_value = request.GET.get('sorted')
    
    if not (sort_value:= request.GET.get('sorted')):
        movies = Movie.objects.all().order_by('?')[:10]

    elif sort_value == 'popular':
        movies = Movie.objects.all().order_by('-vote_count')[:10]

    elif sort_value == 'recent':
        movies = Movie.objects.all().order_by('-release_date')[:10]
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieDetailSerializer(movie)

    return Response(serializer.data)


def like(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if movie.like_users.filter(pk=movie_id).exists():
        movie.like_users.remove(request.user)
        is_liked = False
    
    else:
        movie.like_users.add(request.user)
        is_liked = True
    
    context = {
        'is_liked': is_liked,
        'like_count' : movie.like_users.count()
    }
    return JsonResponse(context)


# 댓글을 모두 출력?
# @api_view(['GET'])
# def review_list(request):
#     if request.method == 'GET':
#         reviews = get_list_or_404(Review)
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)


# 댓글 생성 -> 저장하기
@api_view(['POST'])
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # 개별 조회?
    # if request.method == 'GET':
    #     serializer = ReviewSerializer(review)
    #     return Response(serializer.data)


    # 댓글 삭제
    if request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    # 댓글 수정
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)