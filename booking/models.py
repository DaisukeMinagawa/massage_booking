from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    COURSE_CHOICES = (
        (60, '60分コース'),
        (90, '90分コース'),
        (120, '120分コース'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    course = models.IntegerField(choices=COURSE_CHOICES)

    def __str__(self):
        return f"{self.customer.user.username} - {self.start_time}"