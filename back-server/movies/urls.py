from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.movie_list),

    path('create/', views.movie_create),

    path('popular/', views.movie_popular),
    path('recent/', views.movie_recent),
    # path('movies')

    path('<int:movie_id>/', views.movie_detail),
]
