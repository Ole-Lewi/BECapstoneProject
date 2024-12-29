from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy


def signup_view(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') #redirects to login after sign up
        else:
            form=UserCreationForm()
            return render(request, 'auth/signup.html', {'form':form})
    return redirect('movie_list.html')

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib import messages

def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password) #authenticate user

        if user is not None:
            login(request, user) #log in the user
            return redirect ('movie_list.html') #this redirects to the home page
        else:
            messages.error(request, 'Invalid username or password') #displays this error message
            return render(request, 'login.html') #returns user to the login page
        
def logout_view(request):
    logout(request) #logs out the user
    return redirect('login')    

class SignupView(CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('login')
    template_name='signup.html'

from django.shortcuts import get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required #protects review submission
from django.http import HttpResponse
from rest_framework import permissions
from .serializers import MovieSerializer, ReviewSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

#pagination setup
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10 #number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

#permission setup
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CustomPermission(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj): #only allow the owner to edit and delete
        return request.user == obj.user
    
#CRUD operations for Movies
# Movie ListView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        try:
            return get_object_or_404(Movie, id=self.kwargs['pk'])
        except:
            raise NotFound(detail="The requested movie is not available.")

#Retrieve, Update, and Delete Movies
class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

#CRUD operations for Reviews
#ListCreateViews
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


#adding a review
@login_required #ensures the user is logged in first
def add_review(request, movie_id):
    movie=get_object_or_404(Movie, id=movie_id)

    if request.method=='POST':
        rating=request.POST['rating']
        comment=request.POST['comment']
        Review.objects.create(movie=movie, user=request.user, rating=rating, comment=comment) #creates and saves the reviews to the database.
        permission_classes = [permissions.IsAuthenticated]
        return redirect('movie_detail',movie_id=movie_id) # redirects back to the movie_detail
    
    return render(request, 'movies/add_review.html', {'movie':movie})

#creating a homepage view
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Movie Review App")