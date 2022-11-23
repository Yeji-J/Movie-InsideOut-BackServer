from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import MovieDetailSerializer, MovieListSerializer, ReviewSerializer
from .models import Movie, Genre, Actor, Review

import requests


def YouTube(movie_title):
    API_KEY = 'AIzaSyBB6id-z5CSBNoyVx_BFv6Tz-VyFPd0k1o',
    API_URL = 'https://www.googleapis.com/youtube/v3/search',
    pass



@api_view(['GET'])
def movie_create(request):
    print('create')

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
    # 인기영화('popular), 상영중(upcoming)인 영화 한번에 받기
    url_name = [['popular', 5], ['now_playing', 1]]
    page_num = [i for i in range(1, 6)]


    for name, max_num in url_name:
        
        for num in range(max_num):
            
            url = 'https://api.themoviedb.org/3/movie/' + name
            params = {
                'api_key': api_key,
                # 'language': 'KO',
                'page': page_num[num],
                'region': 'KR'
            }

            response = requests.get(url, params).json()['results']

            for data in response:
                movie_id = data['id']
                actor_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
                
                params = {
                    'api_key': api_key,
                    # 'language': 'KO',
                }

                # 출연진 : cast, 연출진: crew
                res = requests.get(actor_url, params).json()['cast']

                actors = []
                if len(res):
                    if len(res) < 5:
                        for idx in range(len(res)):
                            actor = Actor(actor_id = res[idx]['id'], name = res[idx]['name'])
                            actor.save()

                            actors.append(res[idx]['id'])
                    
                    else:
                        for idx in range(5):
                            actor = Actor(actor_id = res[idx]['id'], name = res[idx]['name'])
                            actor.save()

                            actors.append(res[idx]['id'])
                    
                    
                    data['movie_id'] = data['id']
                    serializer = MovieDetailSerializer(data = data)
                    
                    if serializer.is_valid():
                        serializer.save(genres=data['genre_ids'], actors=actors)

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
    
    is_liked = False

    if request.user.pk:
        if movie.like_users.filter(pk=request.user.pk).exists():
            is_liked = True
        else:
            is_liked = False

    context = {
        'data': serializer.data,
        'is_liked': is_liked
    }

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if movie.like_users.filter(pk=request.user.pk).exists():
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



@api_view(['GET'])
def review_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review = movie.reviews.all()
    serializer = ReviewSerializer(review, many=True)
    return Response(serializer.data)


# 댓글 생성 -> 저장하기
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def watchlist(request):
    
    movie = Movie.objects.filter(title=request.data['movie'].get('title'))

    if not movie:
        movie_id = request.data['movie']['id']

        api_key = '3cd8e0319cee80069c4b85f6cf42fded'

        actor_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'

        params = {
            'api_key': api_key,
            # 'language': 'KO',
        }

        
        res = requests.get(actor_url, params).json()
        
        actors = []
        if len(res) < 5:
            for idx in range(len(res)):
                actor = Actor(actor_id = res[idx]['id'], name = res[idx]['name'])
                actor.save()

                actors.append(res[idx]['id'])
        
        else:
            for idx in range(5):
                actor = Actor(actor_id = res[idx]['id'], name = res[idx]['name'])
                actor.save()

                actors.append(res[idx]['id'])
        
        serializer = MovieDetailSerializer(data = request.data['movie'])
        
        if serializer.is_valid():
            movie = serializer.save(genres=request.data['movie']['genre_ids'], actors=actors)

    movie.user_picks.add(request.user)

    return Response(movie)

