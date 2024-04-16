from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_admin = (True,)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


genderchoice = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True, null=True, blank=True
    )
    name = models.CharField(max_length=100,null=True, blank=True)
    Gender = models.CharField(
        max_length=100, choices=genderchoice, null=True, blank=True
    )
    phonenumber = models.IntegerField(null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.username = self.email
        super(MyUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.email}{self.id}"


class Friendship(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="from_friends",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="to_friends",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("from_user", "to_user")
