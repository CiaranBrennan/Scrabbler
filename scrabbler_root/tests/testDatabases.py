from django.test import TestCase
from django.core.exceptions import ValidationError
from scrabbler_app.models import Match, Player, MatchScore
import datetime

class MatchTestCase(TestCase):
    def setUp(self):
        Match.objects.create (
            datePlayed = datetime.date(2023, 4, 13),
            comments = "Test match"
        )
    
    def testValidMatch(self):
        testMatch = Match.objects.get(datePlayed = datetime.date(2023, 4, 13))
        self.assertEqual(testMatch.datePlayed, datetime.date(2023, 4, 13))
        self.assertEqual(testMatch.comments, "Test match")
        
    def testInvalidMatch(self):
        with self.assertRaises(ValidationError):
            Match.objects.create(
                datePlayed = datetime.date.today() + datetime.timedelta(days = 1),
                comments = "Test invalid match"
            )

class PlayerTestCase(TestCase):
    def setUp(self):
        self.duplicatePlayer = Player(
            forename = "test",
            surname = "user"
        )
        self.duplicatePlayer.save()
    
    def testDuplicateUser(self):
        with self.assertRaises(ValidationError):
            self.duplicatePlayer.save()
    
    def testRecordOutputFormat(self):
        testUser = Player.objects.first()
        self.assertEqual(str(testUser), "test user")
            
class MatchScoreTestCase(TestCase):
    
    def setUp(self):
        self.testMatch = Match(
            datePlayed = datetime.date(2023, 4, 13),
            comments = "Test match"
        )
        self.testPlayer = Player(
            forename = "test",
            surname = "user"
        )
        self.testMatch.save()
        self.testPlayer.save()
    
    def testInvalidScore(self):
        with self.assertRaises(ValidationError):
            MatchScore.objects.create(
                match = self.testMatch,
                player = self.testPlayer,
                score = -1,
                won = False
            )