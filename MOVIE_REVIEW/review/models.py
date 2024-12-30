from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#Custom user to handle user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError ("The Email field is required")
        email = self.normalize_email(email) #normalize email(convert to lowercase, remove spaces,etc)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # save user in database
        return user
    
    #method to create a superuser
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True) #can login if active
    is_staff = models.BooleanField(default=False) # determines admins access

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' #login in with email instead of username
    REQUIRED_FIELDS = ['first_name', 'last_name'] #Additional required fields when creating superuser

    def _str_(self):
        return self.email 

    
class Movie(models.Model):
    title=models.CharField( max_length=50)
    description=models.TextField()
    release_date=models.DateField(auto_now_add=True)
    duration=models.IntegerField()
    Poster=models.ImageField(upload_to="poster/")

    def _str_(self):
        return (self.title)
    
class Review(models.Model):
    Movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    CustomUser=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.TextField()
    date_created=models.DateField(auto_now_add=True)

    def _str_(self):
        return(f"Review by {self.user.name} on {self.title}")

#Adding Like and Comment Features on Reviews
from django.conf import settings 

class Like(models.Model):
    review=models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    CustomUser=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('review', 'CustomUser') #this prevents multiple likes from the same user

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
