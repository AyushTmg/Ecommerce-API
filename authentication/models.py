from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    username=models.CharField(max_length=150,unique=True)
    email=models.EmailField(unique=True)

    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=CustomUserManager()


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']

    def __str__(self) -> str:
        return f"{self.username}"
    

    # ! Custom method for deleting a use account 
    def delete_user_account(self):
        """
        Custom method for deleting a user account
        completely
        """
        return self.delete()
    





