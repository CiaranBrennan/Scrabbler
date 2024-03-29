# Generated by Django 4.1.7 on 2023-02-14 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrabbler_app', '0010_remove_profile_name_profile_forename_profile_surname'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.SmallIntegerField(verbose_name='Points')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forename', models.CharField(max_length=16, verbose_name='Forename')),
                ('surname', models.CharField(max_length=16, verbose_name='Surname')),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='match',
        ),
        migrations.RemoveField(
            model_name='score',
            name='player',
        ),
        migrations.RemoveField(
            model_name='match',
            name='noOfPlayers',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner',
        ),
        migrations.AddField(
            model_name='match',
            name='comments',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Player Comments'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.AddField(
            model_name='matchscore',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrabbler_app.match'),
        ),
        migrations.AddField(
            model_name='matchscore',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrabbler_app.player'),
        ),
    ]
