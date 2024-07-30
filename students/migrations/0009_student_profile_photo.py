# Generated by Django 4.2 on 2024-07-30 05:24

from django.db import migrations, models
import students.models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_alter_fees_detail_reference_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_photo',
            field=models.FileField(default=None, null=True, upload_to=students.models.student_profile_image_directory),
        ),
    ]