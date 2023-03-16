from django.db import models

# Create your models here.
class Match(models.Model):
	datePlayed  = models.DateField("Date Played")
	comments 	= models.CharField("Player Comments", max_length=300, blank=True, null=True)

class Player(models.Model):
	forename = models.CharField("Forename", max_length=16)
	surname  = models.CharField("Surname", max_length=16)

	def __str__(self):
		return "{} {}".format(self.forename, self.surname)

class MatchScore(models.Model):
	match 	 = models.ForeignKey(Match, on_delete=models.CASCADE)
	player 	 = models.ForeignKey(Player, on_delete=models.CASCADE)
	score 	 = models.SmallIntegerField("Score")
	won		 = models.BooleanField("Won", default=False)