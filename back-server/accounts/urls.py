from django.urls import path
from . import views

urlpatterns = [
    # path('profile/', include('accounts.urls')),
    path('delete/', views.user_delete),
    path('<int:user_pk>/follow/', views.follow),    # 수정
    path('watched/<int:movie_id>/', views.watched_list),   # 수정
    path('<str:username>/', views.profile),
]