from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _  # Fixed the import name here

class User(AbstractUser):
    """
    Custom User model where email is unique.
    """
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    registration_method = models.CharField(
        max_length=20, 
        choices=[('email', 'Email'), ('google', 'Google'), ('apple', 'Apple')],
        default='email'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"