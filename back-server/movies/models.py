from django.db import models
from django.conf import settings

# 장르 모델
class Genre(models.Model):
    gerne_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 배우 모델
class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Movie 모델
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField(null=True)
    poster_path = models.TextField(null=True)
    release_date = models.DateField()
    adult = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    backdrop_path = models.TextField(null=True)
    runtime = models.IntegerField(null=True)
    movie_id = models.IntegerField(primary_key=True)

    # ManyToManyField
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="actors")

    def __str__(self):
        return self.title


# 특정 Movie에 대한 Review
class Review(models.Model):
    content = models.CharField(max_length=500)
    vote = models.FloatField()      # 평점
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKey
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.content



