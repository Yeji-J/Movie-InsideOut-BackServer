# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from movies.serializers import 


# class Profile(serializers.ModelSerializer):
#     following_count = serializers.IntegerField(source='following.count', read_only=True)
#     followers_count = serializers.IntegerField(source='follower.count', read_only=True)
#     like_movies = 

#     class Meta:
#         model = get_user_model()
#         fields = ('username')