from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    
    def create_user(self, firstname, email, password=None):
        if firstname is None:
            raise TypeError('Users must have a username.')

        user = self.model(firstname=firstname, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, firstname, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(firstname, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(verbose_name='firstname', max_length=255, blank=True)
    lastname = models.CharField(verbose_name='lastname', max_length=255, blank=True)
    email = models.EmailField(verbose_name='email', db_index=True, unique=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    is_staff = models.BooleanField(verbose_name='is_staff', default=False)
    phone = models.PositiveIntegerField(verbose_name='phone', default=None, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('auth:profile', kwargs={'pk': self.id})

    get_absolute_url.short_description = 'absolute url'

    def get_full_name(self):
        return self.firstname

    def get_short_name(self):
        return self.firstname
    