from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.

def garments_list(request: HttpRequest) -> HttpResponse:
