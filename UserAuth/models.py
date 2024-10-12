from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User


# Create your models here.

# Custom User Manager 
class UserManager(BaseUserManager):
    def create_user(self, email, name, role, password=None):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email), name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
          user = self.create_user(email, name, password)
          user.is_staff = True
          user.is_admin = True
          user.is_superuser = True
          user.save(using=self._db)
          return user


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    ROLES_CHOICES = (
    ("Superuser", "Superuser"),
    ("Admin", "Admin"),
    ("Staff", "Staff"),
    ("Customer", "Customer")
    )
    
    email = models.CharField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.IntegerField(null=True,blank=True)
    role = models.CharField(max_length=250, choices=ROLES_CHOICES)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email