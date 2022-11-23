from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),

    path('create/', views.movie_create),

    path('<int:movie_id>/', views.movie_detail),

    path('<int:movie_id>/like/', views.like),

    path('<int:movie_id>/reviews/', views.review_list),

    path('<int:movie_id>/review_create/', views.review_create),

    path('reviews/<int:review_pk>/', views.review_detail),

    path('watchlist/', views.watchlist),

    path('recommend/', views.movie_recommend),
]
