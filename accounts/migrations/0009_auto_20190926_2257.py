# Generated by Django 2.2.3 on 2019-09-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190921_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='img',
            field=models.ImageField(default='None', upload_to='pics/'),
        ),
    ]
