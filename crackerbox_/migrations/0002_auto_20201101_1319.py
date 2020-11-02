# Generated by Django 3.0.8 on 2020-11-01 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crackerbox_', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzerrecord',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='crackerbox_.Document'),
        ),
        migrations.AddField(
            model_name='pdf',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdf_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='quizzerrecord',
            unique_together={('document', 'owner')},
        ),
    ]