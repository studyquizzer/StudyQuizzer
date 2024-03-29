# Generated by Django 3.0.8 on 2020-11-01 12:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=180)),
                ('created_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10)),
                ('question', models.CharField(max_length=160)),
                ('option1', models.CharField(max_length=64)),
                ('option2', models.CharField(max_length=64)),
                ('option3', models.CharField(max_length=64)),
                ('option4', models.CharField(max_length=64)),
                ('ans', models.CharField(max_length=1)),
                ('docfile', models.FileField(blank=True, null=True, upload_to='documents/MChoice/')),
                ('created_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('edited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField()),
            ],
        ),
    ]
