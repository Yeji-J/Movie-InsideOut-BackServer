from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['DELETE'])
def user_delete(request):
    request.delete()     # 탈퇴 후 로그아웃
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def profile(request, username):
    pass


@api_view(['GET'])
def follow(request, user_pk):
    pass