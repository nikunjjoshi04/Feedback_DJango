# Generated by Django 2.2.3 on 2019-09-26 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='std_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]