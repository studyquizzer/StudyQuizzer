# Generated by Django 3.0.8 on 2020-11-01 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MultiChoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vote',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MultiChoice.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MultiChoice.Category'),
        ),
        migrations.AddField(
            model_name='question',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_question', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MultiChoice.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('creator', 'question')},
        ),
    ]
