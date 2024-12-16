import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django_otp.plugins.otp_email.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError("The Email field is required")
        if not phone:
            raise ValueError("The Phone field is required")
        if not name:
            raise ValueError("The Name field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(email, name, phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
    ]

    SEATING_CHOICES = [
        (5, '5 Seats'),
        (6, '6 Seats'),
        (7, '7 Seats'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    rent_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(max_digits=12, decimal_places=2)
    engine_specs = models.CharField(max_length=255)
    mileage = models.DecimalField(max_digits=5, decimal_places=2)
    transmission = models.CharField(choices=TRANSMISSION_CHOICES, max_length=10)
    fuel_type = models.CharField(choices=FUEL_CHOICES, max_length=10)
    seating_capacity = models.IntegerField(choices=SEATING_CHOICES)
    image_url = models.URLField(max_length=1000)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.brand} {self.model}'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.name}'s Wishlist"

    class Meta:
        unique_together = ('user', 'car')

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    start_time = models.TimeField()
    hours = models.IntegerField()
    address = models.TextField()
    driver_needed = models.BooleanField(default=False)
    total_price = models.FloatField()
    payment_status = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name} {self.car.brand}'

class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    start_time = models.TimeField()
    hours = models.IntegerField()
    address = models.TextField()
    driver_needed = models.BooleanField(default=False)
    total_price = models.FloatField()
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} {self.car.brand}'