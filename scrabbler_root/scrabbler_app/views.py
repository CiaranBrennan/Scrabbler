from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from scrabbler_app.models import Profile, Match, Score
from .forms import EditForm, CreateForm
from django.http import HttpResponseRedirect
from django.db.models import Avg, Max, Min, Sum
from django.contrib import messages
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
	# Get all players and scores
	players = Profile.objects.all()
	results = Score.objects.order_by("points")
	playerList = []

	# Get average score of each player
	for player in players:
		playerScore = results.filter(player = player)
		avgScore = playerScore.aggregate(Avg("points"))
		playerList.append([player,
			round(avgScore["points__avg"])
		])
	playerList = sorted(playerList, key = lambda player: player[1], reverse=True)

	# Get info about the games with the highest and lowest scores
	worstScore = results[0]
	bestScore = results[len(results) - 1]
	bestOpponent = Score.objects.filter(match = bestScore.match).exclude(player = bestScore.player).first()
	worstOpponent = Score.objects.filter(match = worstScore.match).exclude(player = worstScore.player).first()
	bestMatch = [bestScore.points,
		bestScore.player,
		bestOpponent.player,
		bestScore.match.datePlayed
	]
	worstMatch = [worstScore.points,
		worstScore.player,
		worstOpponent.player,
		worstScore.match.datePlayed
	]

	# Serve all the stuff to the webpage
	return render(request, "index.html", {"users":playerList,
		"bestMatch":bestMatch,
		"worstMatch":worstMatch
	})

def userProfile(request, userID):
	# Get player record and all of their score records
	player = Profile.objects.filter(pk = userID).first()
	results = Score.objects.filter(player = player).order_by("points")

	# print(results[0].match)
	# Get a load of info about the player's scores
	scoreStats = results.aggregate(Sum("points"), Avg("points"))
	bestScore = results[len(results) - 1]
	totalScore = scoreStats["points__sum"]
	wins = 0
	for result in results:
		if result.match.winner == player.name:
			wins += 1

	bestOpponent = Score.objects.filter(match = bestScore.match).exclude(player = player).first()
	bestMatch = [bestScore.points, bestOpponent.player, bestScore.match.datePlayed]

	# TODO: Add graph of average scores each year

	# Serve
	return render(request, "profile.html", {"user":player,
		"wins":wins,
		"losses":results.count() - wins,
		"avgScore":round(scoreStats["points__avg"]),
		"bestMatch":bestMatch
	})

def NewMatch(request):
	return render(request, "match.html")