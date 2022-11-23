from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import PostListSerializer, CommentSerializer, PostSerializer
from .models import Post, Comment
from movies.models import Movie


# Create your views here.
@api_view(['GET'])
def post_list(request):
    posts = get_list_or_404(Post)
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    serializer = PostListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'DELETE', 'PUT'])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
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
