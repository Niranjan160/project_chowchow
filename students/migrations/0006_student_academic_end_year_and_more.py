# Generated by Django 4.2 on 2024-07-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_student_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='academic_end_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='academic_start_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fees_detail',
            name='receipt_status',
            field=models.CharField(choices=[('PEN', 'Pending'), ('ACC', 'Accepted'), ('REJ', 'Rejected')], default='PEN', max_length=5),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('OA', 'Office Administrator'), ('S', 'Student')], default='S', max_length=5),
        ),
    ]