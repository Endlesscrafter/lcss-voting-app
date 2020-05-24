from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(PartyVote)
admin.site.register(CandidateVote)
admin.site.register(Voter)
admin.site.register(ElectionPartyList)
admin.site.register(ElectionCandidateList)
admin.site.register(Constituency)
admin.site.register(ElectionArea)

# Test
