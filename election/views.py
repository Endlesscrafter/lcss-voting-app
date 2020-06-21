from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import *
from django.utils.timezone import now
from django.db.models import Q
import hashlib

# url decode
from urllib.parse import unquote

# decode cert
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat._oid import ObjectIdentifier
from cryptography.hazmat.backends import default_backend

# Database Models Import
import election.models as electionmodels
from election.models import *

# Create your views here.
def index(request):
    try:
        cert_urlencoded = request.headers["X-Client-Certificate"]
    except KeyError:
        cert_urlencoded = None
    certificate = ""
    if (cert_urlencoded != None):
        cert_pem = unquote(cert_urlencoded)
        cert_bytes = cert_pem.encode('utf-8')
        cert_obj = x509.load_pem_x509_certificate(cert_bytes, default_backend())
        certificate = str(cert_obj.subject)

    # Get the name of the person
    subject = cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    # Get the postal code of the person
    postal_code = cert_obj.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value

    # Filter elections by date (only show those, where the time to vote is not over)
    elections = electionmodels.Election.objects.filter(endDateTime__gte=now())

    # Filter constituencies by postal code
    constituency = electionmodels.Constituency.objects.filter(postal_code=postal_code)[0]

    # get the election area (all elections taking place in a constituency), filter by constituency
    elections_area = electionmodels.ElectionArea.objects.filter(constituency=constituency)

    elections_result = []
    for area in elections_area:
        if(area.election in elections):
            elections_result.append(area.election)

    # compute cert hash
    digest = hashlib.sha256()
    # Hash the certificate
    digest.update(cert_bytes)
    votehash = digest.hexdigest()

    # Get all votes of this person for every election
    already_voted_elections = []
    for election in elections:
        voters = electionmodels.Voter.objects.filter(voter_hash=votehash,election=election)
        # Check if at least one vote was cast
        if(voters):
            already_voted_elections.append(election)

    # remove already voted election from list
    eligible_elections = [i for i in elections_result if i not in already_voted_elections ]

    output_dict = {"elections": eligible_elections, "certificate": "", "name": subject}
    rendered = render_to_string("index.html", output_dict, request=request)
    return HttpResponse(rendered)

def election(request, wahl="empty"):
    try:
        cert_urlencoded = request.headers["X-Client-Certificate"]
    except KeyError:
        cert_urlencoded = None
    certificate = ""
    if (cert_urlencoded != None):
        cert_pem = unquote(cert_urlencoded)
        cert_bytes = cert_pem.encode('utf-8')
        cert_obj = x509.load_pem_x509_certificate(cert_bytes, default_backend())
        certificate = str(cert_obj.subject)

    # Get the name of the person
    subject = cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    election = electionmodels.Election.objects.filter(title=wahl)

    election_parties = electionmodels.ElectionPartyList.objects.filter(election=election[0])
    election_candidates = electionmodels.ElectionCandidateList.objects.filter(election=election[0])

    party_result = []
    for eparty in election_parties:
        party_result.append(eparty.party)

    candidate_result = []
    for ecandidate in election_candidates:
        candidate_result.append(ecandidate.candidate)

    output_dict = {"name": subject, "parties": party_result, "candidates" : candidate_result, "wahl": wahl}
    rendered = render_to_string("abstimmung.html", output_dict, request=request)
    return HttpResponse(rendered)

def abgeschlossen(request):
    try:
        cert_urlencoded = request.headers["X-Client-Certificate"]
        request_method = request.method
    except KeyError:
        cert_urlencoded = None
    certificate = ""
    if (cert_urlencoded != None):
        cert_pem = unquote(cert_urlencoded)
        cert_bytes = cert_pem.encode('utf-8')
        cert_obj = x509.load_pem_x509_certificate(cert_bytes, default_backend())
        certificate = str(cert_obj.subject)

    # Get the name of the person
    subject = cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    if(request_method == "POST"):
        form = request.POST
    
        party = None
        if("PARTY" in form.keys()):
                party = form["PARTY"]
        
        candidate = None
        if("CANDIDATE" in form.keys()):
                candidate = form["CANDIDATE"]

        wahl = "ERROR"
        if("WAHL" in form.keys()):
                wahl = form["WAHL"]

        digest = hashlib.sha256()
        # Hash the certificate
        digest.update(cert_bytes)
        votehash = digest.hexdigest()

        # get election
        election = electionmodels.Election.objects.filter(title=wahl)

        # Save vote
        v = Voter(voter_hash=votehash,election=election[0]) 
        v.save()

        # increment party vote
        if(party != None):
                party_id = electionmodels.Party.objects.filter(party_name=party)
                election_party = electionmodels.ElectionPartyList.objects.filter(party=party_id[0],election=election[0])[0]
                # check if party_vote object already exists
                pv = electionmodels.PartyVote.objects.filter(elected_party=election_party)
                
                if not pv:
                # empty list, create object
                        partyvote = PartyVote(elected_party=election_party,number_of_votes=1)
                        partyvote.save()
                else:
                        partyvote = pv[0]
                        partyvote.number_of_votes += 1
                        partyvote.save()

        # incremet candidate vote
        if(candidate != None):
                candidate_parts = candidate.split("|")
                candidate_name_parts = candidate_parts[0].split(" ")
                candidate_first_name = candidate_name_parts[0]
                candidate_last_name = candidate_name_parts[1]

                candidate_id = electionmodels.Candidate.objects.filter(first_name=candidate_first_name,last_name=candidate_last_name)
                election_candidate = electionmodels.ElectionCandidateList.objects.filter(candidate=candidate_id[0],election=election[0])[0]
                # check if party_vote object already exists
                cv = electionmodels.CandidateVote.objects.filter(elected_candidate=election_candidate)
                
                if not cv:
                # empty list, create object
                        candidatevote = CandidateVote(elected_candidate=election_candidate,number_of_votes=1)
                        candidatevote.save()
                else:
                        candidatevote = cv[0]
                        candidatevote.number_of_votes += 1
                        candidatevote.save()


    output_dict = {"name": subject, "method": ""}
    rendered = render_to_string("abgeschlosseneWahl.html", output_dict, request=request)
    return HttpResponse(rendered)