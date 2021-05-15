from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from scrabbler_app.models import Profile, Match, Score
from .forms import EditForm, CreateForm
from django.http import HttpResponseRedirect
from django.db.models import Avg, Max, Min, Sum
from django.contrib import messages

# Create your views here.
def index(request):
	players = Profile.objects.all()
	results = Score.objects.order_by("score")
	playerList = []

	for player in players:
		playerScore = results.filter(player = player)
		if playerScore.count() >= 10:
			avgScore = playerScore.aggregate(Avg("score"))
			playerList.append([player,
				round(avgScore["score__avg"])
			])
	playerList = sorted(playerList, key = lambda player: player[1], reverse=True)

	worstScore = results[0]
	bestScore = results[len(results) - 1]
	bestOpponent = Score.objects.filter(match = bestScore.match).exclude(player = bestScore.player).first()
	worstOpponent = Score.objects.filter(match = worstScore.match).exclude(player = worstScore.player).first()
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
	return render(request, "index.html", {"users":playerList[:10],
		"bestMatch":bestMatch,
		"worstMatch":worstMatch
	})

def userProfile(request, userID):
	user = Profile.objects.filter(pk = userID).first()
	results = Score.objects.filter(player = user).order_by("score")
	scoreStats = results.aggregate(Sum("score"), Avg("score"))
	bestScore = results[len(results) - 1]
	totalScore = scoreStats["score__sum"]
	bestOpponent = Score.objects.filter(match = bestScore.match).exclude(player = user).first()
	bestMatch = [bestScore.score, bestOpponent.player, bestScore.match.datePlayed]
	return render(request, "profile.html", {"user":user,
		"wins":results.filter(won = True).count(),
		"losses":results.filter(won = False).count(),
		"avgScore":round(scoreStats["score__avg"]),
		"bestMatch":bestMatch
	})

def editProfile(request, userID):
	user = Profile.objects.filter(pk = userID).first()
	if request.method == 'POST':
		form = EditForm(request.POST)
		if form.is_valid():
			user.firstName = form.cleaned_data["firstName"]
			user.surname = form.cleaned_data["surname"]
			user.email = form.cleaned_data["email"]
			user.save()
			return HttpResponseRedirect('../../')
	else:
		form = EditForm(initial={"firstName":user.firstName,
			"surname":user.surname,
			"email":user.email
		})
	return render(request, "edit.html", {"user": user, "form": form})

def createProfile(request):
	if request.method == 'POST':
		form = CreateForm(request.POST)
		if form.is_valid():
			firstName = form.cleaned_data["firstName"]
			surname = form.cleaned_data["surname"]
			email = form.cleaned_data["email"]
			dateJoined = form.cleaned_data["dateJoined"]
			testUnique = Profile.objects.filter(Q(firstName = firstName, surname = surname) |Q(email = email))
			print(testUnique)
			if len(testUnique) == 0:
				user = Profile.objects.create(
				firstName = firstName,
				surname = surname,
				email = email,
				dateJoined = dateJoined
				)
				user.save()
				return HttpResponseRedirect('../../')
			else:
				messages.error(request, "An account with that name or email address already exists. Please log in or try again.")
	else:
		form = CreateForm(initial={"dateJoined": "YYYY-MM-DD"})
	return render(request, "create.html", {"form": form})
