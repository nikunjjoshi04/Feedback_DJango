# Generated by Django 2.2.3 on 2019-09-21 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_questions_que_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_id', models.IntegerField()),
                ('csv', models.CharField(max_length=225)),
            ],
        ),
        migrations.AlterField(
            model_name='questions',
            name='que_id',
            field=models.IntegerField(),
        ),
    ]
