from django.db import models
from .apps import user_directory_path

class Contact(models.Model):
    name = models.CharField(max_length=50,unique=False,blank=False)
    email=models.CharField(max_length=50)
    subject = models.CharField(max_length=80)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=64,blank=False)
    image = models.ImageField(upload_to=user_directory_path) 

class Useraddress(models.Model):
    username = models.CharField(max_length=50)
    add = models.CharField(max_length=500)

#CUSTOM USER
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, username,email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=50,blank=True, null=True)
    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True
    