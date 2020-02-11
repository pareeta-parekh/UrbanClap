from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *


@api_view(['GET', 'POST'])
def addservice(request, pk):
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


@api_view(['GET', 'PUT'])
def updateservice(request, asid, spid):
    if request.method == "PUT":
        spobj = Serviceprovider.objects.get(id = spid)
        if request.POST['status'] == "Reject":
            for obj in spobj.applied_service:
                if obj.asid == int(asid) and obj.status != "Accepted":
                    obj.status = request.POST['status']
                    spobj.save()
                    return Response("Status Updated")
                else:
                    return Response("Service is Accepted. Can't reject it.")
        else:
            for obj in spobj.applied_service:
                if obj.asid == int(asid):
                    print("In if")
                    obj.status = request.POST['status']
                    #obj.save()
            spobj.save()
            return Response("Status Updated")


@api_view(['GET', 'DELETE'])
def deleteservice(request, sid, spid):
    if request.method == 'DELETE':
        spobj = Serviceprovider.objects.get(id = spid)
        count = 0
        for obj in spobj.applied_service:
            if obj.service_id == int(sid) and obj.status == "Reject":
                count = count + 1
        if count == 0:
            sobj = ServiceList.objects.get(sid = sid)
            for obj in spobj.services:
                if obj.sid == int(sid):
                    obj.is_deleted = True
                    spobj.save()
            sobj.is_deleted = True
            sobj.save()
            return Response("Deleted successfully")
        else:
            return Response("Inavlid Function")