from django.db import models

# Create your models here.
class Match(models.Model):
	datePlayed = models.DateField("Date Played")

class Profile(models.Model):
	firstName = models.CharField("First Name", max_length = 30)
	surname = models.CharField("Surname", max_length = 30)
	email = models.EmailField("Email")
	dateJoined = models.DateField("Date Joined")

	def __str__(self):
		return '{} {}'.format(self.firstName, self.surname) 

class Score(models.Model):
	player = models.ForeignKey(Profile, on_delete=models.CASCADE)
	won = models.BooleanField("Did they win?")
	score = models.SmallIntegerField("Score")
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
