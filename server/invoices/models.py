from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email,name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)

    is_staff = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Invoice(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=20)
    billing_address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    total_price = models.FloatField(blank=True, null=True)
    number = models.CharField(max_length=6)

    def __str__(self) -> str:
        return self.number


class Product(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name
    
    @property
    def total_price(self):
        return self.count * self.price
    
    def save(self, *args, **kwargs) -> None:
        invoice = self.invoice
        all_products = invoice.product_set.all()
        invoice.total_price = 0
        for product in all_products:
            invoice.total_price += product.total_price
        invoice.save()
        return super().save(*args, **kwargs)
