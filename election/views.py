from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import *
from django.utils.timezone import now


# Database Models Import
import election.models as electionmodels

# Create your views here.
def index(request):
    elections = electionmodels.Election.objects.filter(endDateTime__gte=now())
    output_dict = {"elections": elections}
    rendered = render_to_string("index.html", output_dict)
    return HttpResponse(rendered)
