# Generated by Django 3.0.4 on 2021-05-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrabbler_app', '0008_match_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='comments',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Player Comments'),
        ),
    ]
