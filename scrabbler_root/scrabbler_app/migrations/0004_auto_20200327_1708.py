# Generated by Django 3.0.4 on 2020-03-27 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrabbler_app', '0003_auto_20200327_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='players',
        ),
        migrations.RemoveField(
            model_name='match',
            name='scores',
        ),
        migrations.RemoveField(
            model_name='score',
            name='scoreOne',
        ),
        migrations.RemoveField(
            model_name='score',
            name='scoreTwo',
        ),
        migrations.AddField(
            model_name='profile',
            name='scores',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='scrabbler_app.Score'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='match',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='scrabbler_app.Match'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='score',
            field=models.SmallIntegerField(default=3, verbose_name='Score'),
            preserve_default=False,
        ),
    ]
