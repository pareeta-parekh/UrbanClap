from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *


@api_view(['GET', 'POST'])
def addservice(request):
    if request.method == "GET":
        return Response("All data here")
    
    if request.method == "POST":
        spid = 1
        condata = []
        spobj = Serviceprovider.objects.get(id = spid)
        condata.append(spobj)
        if spobj.services == []:
            sid = 1
        else:
            sid = spobj.services[len(spobj.services) - 1].sid + 1
        condata.append(sid)
        service = AddServiceSerializer(data = request.data, context = condata)
        if service.is_valid():
            service.save()
            print(service)
            return Response(service.data)
            # spobj.save()
        return Response(service.errors)