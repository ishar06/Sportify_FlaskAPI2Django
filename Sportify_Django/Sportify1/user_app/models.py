from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='HOME')
    is_default = models.BooleanField(default=False)
    house_street = models.CharField(max_length=200)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s {self.address_type} address"

    def get_full_address(self):
        return f"{self.house_street}, {self.landmark}, {self.pincode}, {self.state}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other addresses of this user to non-default
            Address.objects.filter(user=self.user).update(is_default=False)
        elif not Address.objects.filter(user=self.user).exists():
            # If this is the first address, make it default
            self.is_default = True
        super().save(*args, **kwargs)
