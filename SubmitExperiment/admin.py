from django.contrib import admin

from .models import PredefinedConfiguration
from .models import AccessCode

# Register your models here.
admin.site.register(PredefinedConfiguration)
admin.site.register(AccessCode)
