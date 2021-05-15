from django.db import models

# Create your models here.
class Match(models.Model):
	datePlayed = models.DateField("Date Played")
	noOfPlayers = models.IntegerField("Number of Players")
	winner = models.CharField("Match Winner", max_length=30)

class Profile(models.Model):
	name = models.CharField("Name", max_length=30)

class Score(models.Model):
	player = models.ForeignKey(Profile, on_delete=models.CASCADE)
	points = models.SmallIntegerField("Points")
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
	comments = models.CharField("Player Comments", max_length=300, blank=True, null=True)