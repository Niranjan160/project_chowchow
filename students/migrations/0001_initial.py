# Generated by Django 4.2 on 2024-07-24 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('role', models.CharField(choices=[('OA', 'Office Administrator'), ('S', 'Student')], max_length=5)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('register_no', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.IntegerField()),
                ('type_of_degree', models.CharField(choices=[('MSC', 'Master of Science'), ('MCA', 'Master of Computer Application'), ('MTECH', 'Master of Technology')], max_length=5)),
                ('type_of_department', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('DS', 'Data Science'), ('AI', 'Artificial Intelligence')], max_length=5)),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fees_detail',
            fields=[
                ('reference_id', models.IntegerField(primary_key=True, serialize=False)),
                ('type_of_fees', models.CharField(choices=[('SF', 'Semester Fees'), ('EF', 'Exam Fees')], max_length=5)),
                ('paid_date', models.DateField()),
                ('receipt_submitted_date', models.DateField(auto_now_add=True)),
                ('receipt_status', models.CharField(choices=[('PEN', 'Pending'), ('ACC', 'Accepted'), ('REJ', 'Rejected')], max_length=5)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
    ]