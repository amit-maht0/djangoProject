from django.db import models

# Create your models here.

'''
User Model Schema
'''
class UserModel(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    followers = models.BigIntegerField(default=0)
    following = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

'''
User Posr Schema
'''

class PostModel(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)