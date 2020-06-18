from django.db import models
from django.utils.timezone import now

# Create your models here.
class Party (models.Model):
    party_name = models.CharField(max_length=128)
    def __str__(self):
        return "{}".format(self.party_name)

class Candidate (models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    party_affiliation = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return "{} {} | {}".format(self.first_name,self.last_name,self.party_affiliation)

class Constituency (models.Model):
    postal_code = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    def __str__(self):
        return "{} {}".format(self.postal_code,self.name)

class Election (models.Model):
    title = models.CharField(max_length=128)
    startDateTime  = models.DateTimeField(default=now, editable=True)
    endDateTime = models.DateTimeField(default=now, editable=True)
    def __str__(self):
        return "{}".format(self.title)

class ElectionPartyList (models.Model):
    election = models.ForeignKey(Election,on_delete=models.PROTECT)
    party = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return "{} in {}".format(self.party,self.election)

class ElectionCandidateList (models.Model):
    election = models.ForeignKey(Election,on_delete=models.PROTECT)
    candidate = models.ForeignKey(Candidate,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return "{} in {}".format(self.candidate,self.election)

class ElectionArea (models.Model):
    election = models.ForeignKey(Election,on_delete=models.PROTECT)
    constituency = models.ForeignKey(Constituency,on_delete=models.PROTECT)
    def __str__(self):
        return "{} is eligible for {}".format(self.constituency,self.election)

class PartyVote (models.Model):
    elected_party = models.ForeignKey(ElectionPartyList,on_delete=models.CASCADE)
    number_of_votes = models.PositiveIntegerField(default=0)

class CandidateVote (models.Model):
    elected_candidate = models.ForeignKey(ElectionCandidateList,on_delete=models.CASCADE)
    number_of_votes = models.PositiveIntegerField(default=0)

class Voter (models.Model):
    voter_hash = models.CharField(max_length=512)
    election = models.ForeignKey(Election,on_delete=models.PROTECT)

