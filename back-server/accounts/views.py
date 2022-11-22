from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# from movies.models import Movie
from movies.serializers import ReviewSerializer, MovieTitleSerializer


# Create your views here.

@api_view(['DELETE'])
def user_delete(request):
    request.delete()     # 탈퇴 후 로그아웃
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    reviews = person.review_set.all()
    favorites = person.like_movies.all()
    watchlist = person.watch_list.all()
    watched = person.watched_movies.all()

    if person.follower.filter(pk=request.user.pk).exists():
        is_followed = True
    else:
        is_followed = False

    context = {
        'user_id': person.id,
        'username': person.username,
        'reviews': ReviewSerializer(reviews, many=True).data,
        'favorites': MovieTitleSerializer(favorites, many=True).data,
        'is_followed': is_followed,
        'following_count': person.following.count(),
        'follower_count': person.follower.count(),
        'watch_list': MovieTitleSerializer(watchlist, many=True).data,
        'watched_movies': MovieTitleSerializer(watched, many=True).data,
    }
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    person = get_object_or_404(User, pk=user_pk)
    if person != request.user:
        if person.follower.filter(pk=request.user.pk).exists():
            person.follower.remove(request.user)
            is_followed = False

        else:
            person.follower.add(request.user)
            is_followed = True
        
        context = {
            'is_followed': is_followed,
            'follow_count': person.follower.count(),
            'following_count': person.following.count()
        }
        
        return JsonResponse(context)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watched_list(request, movie_id):
    User = get_user_model()
    person = get_object_or_404(User, pk=user_pk)

    person.watch_list.remove(movie_id)
    person.watched_movies.add(movie_id)

    serializer = MovieTitleSerializer(person.watched_movies.all(), many=True)

    return Response(serializer.data)