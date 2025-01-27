# Generated by Django 4.2 on 2024-07-25 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees_detail',
            name='fees_amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='Student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='register_no',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
