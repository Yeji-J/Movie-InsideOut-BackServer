from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import PostListSerializer, CommentSerializer, PostSerializer
from .models import Post, Comment
from movies.models import Movie
from movies.views import db_create
from accounts.serializers import UserNameSerializer


# Create your views here.
@api_view(['GET'])
def post_list(request):
    User = get_user_model()
    hot_follower = User.objects.all().order_by('-follower')[:5]
    recent_post = Post.objects.all().order_by('-created_at')[:5]
    hot_post = Post.objects.all().distinct().order_by('-like_users')[:5]
    
    context = {
        'hot_follower': UserNameSerializer(hot_follower, many=True).data,
        'recent_post': PostListSerializer(recent_post, many=True).data,
        'hot_post': PostListSerializer(hot_post, many=True).data,
    }

    return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request, movie_id):
    movie = Movie.objects.filter(movie_id=movie_id)

    if not movie:
        db_create(request.data['movie'])
    
    movie = get_object_or_404(Movie, pk=movie_id)

    serializer = PostListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)

        if post.like_users.filter(pk=request.user.pk).exists():
            is_liked = True
    
        else:
            is_liked = False

        context = {
            'data': serializer.data,
            'is_liked': is_liked,
        }

        return Response(context)
    
    elif request.method == 'DELETE':
        if request.user == post.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        if request.user == post.user:
            serializer = PostListSerializer(post, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
        is_liked = False
    
    else:
        post.like_users.add(request.user)
        is_liked = True
        
    context = {
        'is_liked': is_liked,
        'like_count' : post.like_users.count()
    }

    return JsonResponse(context)



@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        comments = get_list_or_404(Comment)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'DELETE':
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        if request.user == comment.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
