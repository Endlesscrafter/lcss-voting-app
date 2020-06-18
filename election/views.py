from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import *
from django.utils.timezone import now
from django.db.models import Q

# url decode
from urllib.parse import unquote

# decode cert
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat._oid import ObjectIdentifier
from cryptography.hazmat.backends import default_backend

# Database Models Import
import election.models as electionmodels

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

    postal_code = cert_obj.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value

    elections = electionmodels.Election.objects.filter(endDateTime__gte=now())

    constituency = electionmodels.Constituency.objects.filter(postal_code=postal_code)[0]

    elections_area = electionmodels.ElectionArea.objects.filter(constituency=constituency)

    elections_result = []
    for area in elections_area:
        if(area.election in elections):
            elections_result.append(area.election)

    output_dict = {"elections": elections_result, "certificate": "", "name": subject}
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

    output_dict = {"name": subject, "parties": party_result, "candidates" : candidate_result}
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
    
    party = ""
    if("PARTY" in form.keys()):
        party = form["PARTY"]
    
    candidate = ""
    if("CANDIDATE" in form.keys()):
        candidate = form["CANDIDATE"]

    

    output_dict = {"name": subject, "method": ""}
    rendered = render_to_string("abgeschlosseneWahl.html", output_dict, request=request)
    return HttpResponse(rendered)