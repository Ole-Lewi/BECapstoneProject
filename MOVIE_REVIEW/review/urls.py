from django.urls import path
from . import views
from .views import MovieListCreateView, MovieDetailView, ReviewListCreateView, ReviewDetailView
from .views import home

urlpatterns= [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('movies/',MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('', home, name='home') #Map root URL to home view
]