# Generated by Django 4.2 on 2024-07-25 16:02

import django.core.validators
from django.db import migrations, models
import students.models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_fees_detail_fees_amount_alter_student_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees_detail',
            name='fees_receipt',
            field=models.FileField(default=None, null=True, upload_to=students.models.student_fees_directory),
        ),
        migrations.AddField(
            model_name='fees_detail',
            name='semester_number',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
    ]