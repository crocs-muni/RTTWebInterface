from django.db import models
from django.utils import timezone


# Create your models here.
class PredefinedConfiguration(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True)
    required_bytes = models.BigIntegerField()
    description = models.CharField(
        max_length=1000)
    cfg_file = models.FileField(
        "configuration file",
        upload_to='predefined_configurations')

    def __str__(self):
        return self.name


class AccessCode(models.Model):
    description = models.CharField(
        max_length=150)
    access_code = models.CharField(
        max_length=64,
        unique=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return "Code valid until {} ({})".format(self.valid_until,
                                                 self.description)

    def is_valid(self):
        return timezone.now() <= self.valid_until
