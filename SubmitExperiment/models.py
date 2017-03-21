from django.db import models


# Create your models here.
class PredefinedConfiguration(models.Model):
    name = models.CharField(max_length=100, unique=True)
    required_bytes = models.BigIntegerField()
    description = models.CharField(max_length=1000)
    cfg_file = models.FileField("configuration file",
                                upload_to='predefined_configurations')

    def __str__(self):
        return self.name
