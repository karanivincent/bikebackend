from django.db import models
from django.core.files import File
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import get_hasher, identify_hasher
import uuid


from django.contrib.auth.base_user import BaseUserManager
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

            
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,db_index=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    facebookId = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    android = models.BooleanField(blank=True, default=False)
    ios = models.NullBooleanField(blank=True, default=False, null=True)
    acceptPush = models.BooleanField(default=False)
    pushToken = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(('staff'), default=True)
    valid = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')
class Bike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100,db_index=True)
    qrCode = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    picture = models.ImageField(upload_to="media/%Y/%m/%d",null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    available = models.BooleanField(default=True)
    valid = models.BooleanField(default=True)
    class Meta:
        verbose_name = ('Bike')
        verbose_name_plural = ('Bikes')