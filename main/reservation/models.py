from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import uuid

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    user_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="custom_user_groups",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="custom_user_permissions",
        related_query_name="custom_user",
    )

    class Meta(AbstractUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')

class OfferType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Offer class to represent different types of tickets
class Offer(models.Model):
    offer_type = models.ForeignKey(OfferType, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    availability = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='offers/', blank=True, null=True)

    def __str__(self):
        return f"{self.offer_type.name} - {self.price}€"

# Ticket class
class Ticket(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    purchase_key = models.CharField(max_length=100, unique=True, blank=True, null=True)  
    ticket_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    use_date = models.DateTimeField(blank=True, null=True)
    event_location = models.CharField(max_length=255, blank=True, null=True)
    seat_info = models.CharField(max_length=100, blank=True, null=True)

def __str__(self):
    return f"Ticket {self.offer.offer_type} - Key: {self.ticket_key}"



def default_expires_at():
    return timezone.now() + timedelta(days=1)

# Cart class
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    created_at = models.DateTimeField(auto_now_add=True) 
    expires_at = models.DateTimeField(default=default_expires_at)

    def __str__(self):
        return f"Cart of {self.user.username}"

# Transaction class for managing purchases
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    total_amount = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    transaction_status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Transaction by {self.user.username} on {self.transaction_date}"
