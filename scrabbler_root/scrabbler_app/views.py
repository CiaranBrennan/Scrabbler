from datetime import date

import matplotlib.pyplot as plt
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from scrabbler_app.models import Match, MatchScore, Player

from .forms import MatchPlayerForm, CreateForm, EditForm, MatchPlayerForm, MatchModelForm
from .models import MatchScore, Match


# Create your views here.
def index(request):
	# Get all players and scores
	players = Player.objects.all()
	results = MatchScore.objects.order_by("score")
	playerList = []
	# print(results.filter(player = players[3]), players[3].forename)

	# Get average score of each player
	for player in players:
		playerScore = results.filter(player = player)
		avgScore = playerScore.aggregate(Avg("score"))
		playerList.append([player,
			round(avgScore["score__avg"])
		])
	playerList = sorted(playerList, key = lambda player: player[1], reverse=True)

	# Get info about the games with the highest and lowest scores
	worstScore = results[0]
	bestScore = results[len(results) - 1]
	bestOpponent = MatchScore.objects.filter(match = bestScore.match).exclude(player = bestScore.player).first()
	worstOpponent = MatchScore.objects.filter(match = worstScore.match).exclude(player = worstScore.player).first()
	bestMatch = [bestScore.score,
		bestScore.player,
		bestOpponent.player,
		bestScore.match.datePlayed
	]
	worstMatch = [worstScore.score,
		worstScore.player,
		worstOpponent.player,
		worstScore.match.datePlayed
	]

	# Serve all the stuff to the webpage
	return render(request, "index.html", {"users":playerList,
		"bestMatch":bestMatch,
		"worstMatch":worstMatch
	})
	return render(request, "index.html")

def playerProfile(request, userID):
	# Get player record and all of their score records
	player = Player.objects.filter(pk = userID).first()
	results = MatchScore.objects.filter(player = player).order_by("score")

	# Get a load of info about the player's scores
	scoreStats = results.aggregate(Sum("score"), Avg("score"))
	bestScore = results[len(results) - 1]
	totalScore = scoreStats["score__sum"]
	wins = results.filter(won = True).count()

	bestOpponent = MatchScore.objects.filter(match = bestScore.match).exclude(player = player).first()
	bestMatch = [bestScore.score, bestOpponent.player, bestScore.match.datePlayed]

	# TODO: Add graph of average scores each year

	# Serve
	return render(request, "profile.html", {"user":player,
		"wins":wins,
		"losses":results.count() - wins,
		"avgScore":round(scoreStats["score__avg"]),
		"bestMatch":bestMatch
	})

def addMatch(request):
	playerFormset = formset_factory(MatchPlayerForm, extra=0, min_num=2, max_num=4, can_delete=True)
	matchModel = Match
	matchForm = MatchModelForm

	if request.method == 'POST':
			playerInfoForm = playerFormset(request.POST, request.FILES)
			matchInfoForm = matchForm(request.POST, request.FILES)
			if playerInfoForm.is_valid() and matchInfoForm.is_valid():
				playerInfo = playerInfoForm.cleaned_data
				matchInfo = matchInfoForm.cleaned_data
				print(playerInfo)
				print(matchInfo)
				pass
			else:
				playerInfoForm = playerFormset()
	return render(request, "addmatch.html", { 'playerFormset': playerFormset, "matchForm": matchForm })