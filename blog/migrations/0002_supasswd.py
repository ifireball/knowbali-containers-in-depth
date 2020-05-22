import os

from django.db import migrations
from django.db.utils import IntegrityError


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME', 'admin')
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', 'admin@example.com')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', 'admin')

        try:
            superuser = User.objects.create_superuser(
                username=DJANGO_SU_NAME,
                email=DJANGO_SU_EMAIL,
                password=DJANGO_SU_PASSWORD)

            superuser.save()
        except IntegrityError:
            pass

    operations = [
        migrations.RunPython(generate_superuser),
    ]
