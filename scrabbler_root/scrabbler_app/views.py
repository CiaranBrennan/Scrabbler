from datetime import date

import matplotlib.pyplot as plt
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import MatchPlayerForm, MatchPlayerForm, MatchModelForm, CreatePlayerForm
from .models import MatchScore, Match, Player


# Create your views here.
def index(request):
    # Get all players and scores
    players = Player.objects.all()
    results = MatchScore.objects.order_by("score")
    if len(players) > 0 and len(results) > 0:
        playerList = []

        # Get average score of each player
        for player in players:
            playerScore = results.filter(player=player)
            if len(playerScore) > 0:
                avgScore = playerScore.aggregate(Avg("score"))
                playerList.append({
                    "name": player,
                    "averageScore": round(avgScore["score__avg"])
                })
        # Sort players by their average score
        playerList = sorted(
            playerList, key=lambda player: player["averageScore"], reverse=True)
        
        # Get info about the games with the highest and lowest scores
        worstScore = results[0]
        bestScore = results[len(results)-1]

        bestMatch = {
            "score": bestScore.score,
            "name": bestScore.player,
            "datePlayed": bestScore.match.datePlayed
        }
        worstMatch = {
            "score": worstScore.score,
            "name": worstScore.player,
            "datePlayed": worstScore.match.datePlayed
        }

        # Serve all the information
        return render(request, "index.html", {
            "data": True,
            "players": playerList,
            "bestMatch": bestMatch,
            "worstMatch": worstMatch
        })
    return render(request, "index.html", {
        "data": False
    })


def playerProfile(request, userID):
    # Get player record and all of their score records
    player = Player.objects.filter(pk=userID).first()
    results = MatchScore.objects.filter(player=player).order_by("score")

    # Get a load of info about the player's scores
    scoreStats = results.aggregate(Sum("score"), Avg("score"))
    bestScore = results[len(results) - 1]
    totalScore = scoreStats["score__sum"]
    wins = results.filter(won=True).count()

    bestOpponent = MatchScore.objects.filter(
        match = bestScore.match).exclude(player=player).first()
    bestMatch = [
        bestScore.score,
        bestOpponent.player,
        bestScore.match.datePlayed
    ]

    # TODO: Add graph of average scores each year

    # Serve
    return render(request, "profile.html", {
        "player": player,
        "wins": wins,
        "losses": results.count() - wins,
        "averageScore": round(scoreStats["score__avg"]),
        "bestMatch": bestMatch,
        "totalScore": totalScore
    })

def match(request, matchID):
    # Get player record and all of their score records
    matchQuery = Match.objects.filter(pk=matchID).first()
    playersQuery = MatchScore.objects.filter(match=matchQuery).order_by("-score")

    players = []
    winners = []
    winnersQuery = playersQuery.filter(won=True)

    for player in playersQuery:
        players.append(
            {
                "id": player.player.pk,
                "name": player.player,
                "score": player.score
            }
        )
        if player.won:
            winners.append("{}".format(player.player))

    if len(winners) < 3:
        winners =  ' and '.join(winners)
    else:
        winners = ', '.join(winners[:-1]) + ', and ' + winners[-1]
    
    winners

    return render(request, "match.html", {
        "matchInfo": matchQuery,
        "playerInfo": players,
        "winners": winners
    })

def addPlayer (request):
    errors = ""
    playerForm = CreatePlayerForm(request.POST, request.FILES)
    if request.method == 'POST':
        if playerForm.is_valid():
            playerInfo = playerForm.cleaned_data
            newPlayer = Player(
                forename = playerInfo["forename"],
                surname  = playerInfo["surname"]
            )
            newPlayer.save()
            print(playerInfo)
        else:
            errors = playerForm.errors
    return render(request, "addplayer.html", {
        "playerForm": playerForm,
        "errors": errors
    })

def addMatch(request):
    playerFormset = formset_factory(
        MatchPlayerForm,
        extra = 0,
        min_num = 2,
        max_num = 4,
        can_delete = True
    )
    matchForm = MatchModelForm
    error = ""

    if request.method == 'POST':
        playerInfoForm = playerFormset(request.POST, request.FILES)
        matchInfoForm = matchForm(request.POST, request.FILES)
        if playerInfoForm.is_valid() and matchInfoForm.is_valid():
            # Store the data in a useable form
            playerInfo = playerInfoForm.cleaned_data
            matchInfo = matchInfoForm.cleaned_data

            # Determine the winner of the match and get the records of each player
            topScore = 0
            playerRecords = []
            winners = []
            for player in playerInfo:
                playerRecords.append(player)
                if player["score"] > topScore:
                    winners = [player]
                    topScore = player["score"]
                elif player["score"] == topScore:
                    winners.append(player)

            # Add the match record to the database
            newMatch = Match(
                datePlayed = matchInfo["datePlayed"],
                comments = matchInfo["comments"]
            )
            newMatch.save()

            # Add each match score record to the database
            for i in range(0, len(playerInfo)):
                newMatchScore = MatchScore(
                    match = newMatch,
                    player = playerRecords[i]["name"],
                    score = playerInfo[i]["score"],
                    won = True if playerRecords[i] in winners else False
                )
                newMatchScore.save()
        else:
            error = "Please make sure that all fields are filled out!"
    return render(request, "addmatch.html", {
        "playerFormset": playerFormset,
        "matchForm": matchForm,
        "error": error
    })
