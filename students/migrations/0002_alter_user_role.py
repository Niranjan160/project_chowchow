# Generated by Django 4.2 on 2024-07-25 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('OA', 'Office Administrator'), ('S', 'Student')], default='Student', max_length=5),
        ),
    ]