from .models import *
from .serializers import *
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET', 'POST'])
def addservice(request):
    if request.method == "GET":
        try:
            tkn = request.session['token']
            print(tkn)
            try:
                # spobj = Serviceprovider.objects.get(token_id = token)
                return render(request, 'serviceProvider/services.html', {'tkn':tkn})
                # return Response("All data here")

            except ObjectDoesNotExist:
                return Response({'message': 'You are not Logged In...'})
        except KeyError:
            return redirect('/serviceprovider/login/')

        
    
    if request.method == "POST":
        try:
            spobj = Serviceprovider.objects.get(token_id = token)

            condata = []
            spobj = Serviceprovider.objects.get(token_id = token)
            # if spobj.services != []:
            #     for obj in spobj.services:
            #         if obj.service_name != request.POST['service_name']:
            #             if obj.service_category != request.POST['service_category']:
            #                 print(obj.service_name)
            #         else:
            #             return Response("Already exists service name")
            # return Response()

            condata.append(spobj)
            if spobj.services == []:
                sid = 1
            else:
                sid = spobj.services[len(spobj.services) - 1].sid + 1
            condata.append(sid)
            condata.append(spobj.id)
            service = AddServiceSerializer(data = request.data, context = condata)
            if service.is_valid():
                service.save()
                print(service)
                return Response(service.data)
                spobj.save()
            return Response(service.errors)

        except ObjectDoesNotExist:
            return Response({'message': 'You are not Logged In...'})



@api_view(['PUT'])
def updateservice(request, asid, token):
    if request.method == "PUT":
        try:
            spobj = Serviceprovider.objects.get(token_id = token)
            if request.POST['status'] == "Reject":
                for obj in spobj.applied_service:
                    if obj.asid == int(asid) and obj.status != "Accepted":
                        obj.status = request.POST['status']
                        spobj.save()
                        return Response("Status Updated")
                return Response("Service is Accepted, Can't reject it or no such service present")
            else:
                print(request.POST['status'])
                for obj in spobj.applied_service:
                    print("For", obj.asid)
                    if obj.asid == int(asid):
                        print("In if")
                        obj.status = request.POST['status']
                        #obj.save()
                        spobj.save()
                        return Response("Status Updated")

                    
                return Response("No such service present")

               


        except ObjectDoesNotExist:
            return Response({'message': 'You are not Logged In...'})

@api_view(['DELETE'])
def deleteservice(request, sid, token):
    if request.method == 'DELETE':
        # if request.method == "GET":
        try:
            spobj = Serviceprovider.objects.get(token_id = token)                    
            count = 0
            for obj in spobj.applied_service:
                if obj.service_id == int(sid) and (obj.status == "Reject" or obj.status == "Pending"):
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

        except ObjectDoesNotExist:
            return Response({'message': 'You are not Logged In...'})