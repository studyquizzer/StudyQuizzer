# Generated by Django 3.0.8 on 2020-11-01 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('profiled', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('is_reader', models.BooleanField(default=True)),
                ('is_resolver', models.BooleanField(default=True)),
                ('is_advanced', models.BooleanField(default=False)),
                ('book_category', models.CharField(blank=True, choices=[('art', 'Art'), ('arc', 'Architecture'), ('aut', 'Autobiography'), ('bus', 'Business/economics'), ('chi', "Children's"), ('fic', 'Fiction'), ('hea', 'Health/fitness'), ('his', 'History'), ('nov', 'Novel'), ('jou', 'Journal'), ('poe', 'Poetry'), ('rel', 'Religion/spirituality'), ('sci', 'Science'), ('spo', 'Sports_and_leisure'), ('tex', 'Textbook'), ('tra', 'Travel')], max_length=3, null=True)),
                ('book_title', models.CharField(blank=True, max_length=200, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('read_only', 'read_only_users'), ('resolver', 'read, ask, comment, answer'), ('staff', 'advanced users')),
            },
        ),
    ]