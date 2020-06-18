from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import *
from django.utils.timezone import now

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

    certificate = cert_obj.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value

    elections = electionmodels.Election.objects.filter(endDateTime__gte=now())

    output_dict = {"elections": elections, "certificate": certificate, "name": subject}
    rendered = render_to_string("index.html", output_dict)
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

    output_dict = {"name": subject}
    rendered = render_to_string("abstimmung.html", output_dict)
    return HttpResponse(rendered)

def abgeschlossen(request):
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

    output_dict = {"name": subject}
    rendered = render_to_string("abgeschlosseneWahl.html", output_dict)
    return HttpResponse(rendered)