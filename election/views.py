from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import *
from django.utils.timezone import now

# url decode
from urllib.parse import unquote

# decode cert
from cryptography import x509
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

    elections = electionmodels.Election.objects.filter(endDateTime__gte=now())
    output_dict = {"elections": elections, "certificate": certificate}
    rendered = render_to_string("index.html", output_dict)
    return HttpResponse(rendered)
