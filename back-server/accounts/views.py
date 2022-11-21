from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from movies.models import Movie
# from movies.serializers import ReviewSerializer


# Create your views here.

@api_view(['DELETE'])
def user_delete(request):
    request.delete()     # 탈퇴 후 로그아웃
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    reviews = person.review_set.all().values()
    favorites = person.like_movies.all().values('title', 'poster_path')

    review_lst = []
    for review in reviews:
        movie_id = review['movie_id']
        movie_title = get_object_or_404(Movie, pk=movie_id).title
        review_lst.append({'data': review, 'movie_title': movie_title})

    context = {
        'user_id': person.id,
        'username': person.username,
        'reviews': review_lst,
        'favorites': favorites,
        'following_count': person.following.count(),
        'follower_count': person.follower.count()
    }
    return Response(context)


@api_view(['GET'])
def follow(request, user_pk):
    pass