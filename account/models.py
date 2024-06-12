from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class Role(models.Model):
    """
    Model for determining the type of client. For example, a wholesaler or a regular.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Role {self.name}"


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Error with email!!!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, unique=False, verbose_name="first name")
    age = models.IntegerField(null=True)

    GENDERS = (
        (1, 'male'),
        (2, 'female')
    )
    gender = models.IntegerField(choices=GENDERS, null=True)

    # role = 1 if male, 2 if female.
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
    )

    date_of_create = models.DateField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=20, verbose_name="phone number")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'phone'
    ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
