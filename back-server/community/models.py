from django.db import models
from django.conf import settings
from movies.models import Movie, Review

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField()

    # ForeignKey
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="like_reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="posts")

    # ManyToManyField
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts")

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=500)

    # ForeignKey
    post = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 대댓글
    origin_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)