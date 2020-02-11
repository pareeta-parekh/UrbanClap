from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


@api_view(['GET', 'POST'])
def addservice(request , pk):
    if request.method == "GET":
        return Response("All data here")
    
    if request.method == "POST":
        condata = []
        spobj = Serviceprovider.objects.get(pk = pk)
        condata.append(spobj)
        if spobj.services == []:
            sid = 1
        else:
            sid = spobj.services[len(spobj.services) - 1].sid + 1
        condata.append(sid)
        condata.append(pk)
        service = AddServiceSerializer(data = request.data, context = condata)
        if service.is_valid():
            service.save()
            print(service)
            return Response(service.data)
            # spobj.save()
        return Response(service.errors)