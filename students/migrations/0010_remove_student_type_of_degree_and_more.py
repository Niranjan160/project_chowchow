# Generated by Django 4.2 on 2024-07-31 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_student_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='type_of_degree',
        ),
        migrations.RemoveField(
            model_name='student',
            name='type_of_department',
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.CharField(choices=[('MSC CSE', 'Master of Science Computer Science and Engineering'), ('MSC DS', 'Master of Science Data Science'), ('MSC AI', 'Master of Science Artificial Intelligence'), ('MCA', 'Master of Computer Application'), ('MTECH', 'Master of Technology')], default='MAC', max_length=50),
            preserve_default=False,
        ),
    ]
