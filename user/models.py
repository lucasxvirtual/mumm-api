from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, name, password=None):
        if not email:
            raise ValueError('Users must have an email')

        if not nickname:
            raise ValueError('Users must have an nickname')

        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            email=email,
            nickname=nickname,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nickname, name, password):
        user = self.create_user(
            email,
            nickname,
            name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)
    forgot_password_expiration = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(null=True)
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    biography = models.CharField(max_length=240, null=True)
    cell_phone = models.CharField(max_length=25, null=True)
    is_deleted = models.BooleanField(default=False)
    feed_updated = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'nickname']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
