from django.urls import path
from . import views

urlpatterns = [
    path('followers/', views.FollowersListView.as_view()),
    path('followers/<int:pk>', views.FollowerDetailView.as_view()),

]
