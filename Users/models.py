from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from Users.services import *
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'Admin')
        phone_number = check_phone_number(Profile, input('Phone Number: '))
        user = self.create_user(email, password, **extra_fields)
        Profile.objects.create(user=user, phone_number=phone_number)
        return user

class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    institute = models.CharField(max_length=100, null=False, blank=False, default="SSVPS")
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False, blank=False)
    joined_date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'Users Table'

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False, validators=[RegexValidator(regex=r'^\d{10}$')])
    experience = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=False)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, null=False, blank=False, default="Admin Department")

    class Meta:
        db_table = 'Profiles Table'


