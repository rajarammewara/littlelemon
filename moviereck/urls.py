from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.CategoryList.as_view(), name=''),
    path('movielist/', views.MovieList.as_view(), name=''),
    path('movielist/<int:pk>', views.SingleMovieView.as_view(), name=''),
    # path('', views.index, name='index'),
    path('userauth', views.userauth, name='userauth'),
    path('api-token-auth/', obtain_auth_token),

    path('manager_view', views.manager_view, name='manager_view'),
    path('throttle_check', views.throttle_check, name='throttle_check'),
    path('throttle_check_auth', views.throttle_check_auth, name='throttle_check_auth'),
]