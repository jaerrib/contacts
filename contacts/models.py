from django.db import models
from django.urls import reverse


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    creator = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self.pk})
