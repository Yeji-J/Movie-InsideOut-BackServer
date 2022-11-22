from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list),

    path('<int:post_pk>', views.post_detail)

    path('comments/', views.comment_list),

    path('comments/<int:comment_pk>/', views.comment_detail),
    
    path('<int:post_pk>/comments/', views.comment_create),

]