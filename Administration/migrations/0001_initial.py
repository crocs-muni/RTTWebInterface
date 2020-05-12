import os
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
    ] # can also be emtpy if it's your first migration

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_DB_NAME = os.environ.get('DJANGO_DB_NAME', "default")
        DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME', "admin")
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', "admin@localhost")
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', "admin")

        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
