# Generated by Django 2.2.8 on 2019-12-09 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20191209_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]