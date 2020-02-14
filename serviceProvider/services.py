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
            token = request.session['token']
            print(token)
            try:

                spobj = Serviceprovider.objects.get(token_id = token)
                serviceLS = ServiceList.objects.filter(spid=spobj.id)
                return render(request, 'serviceProvider/services.html', {'token':token,'services':serviceLS})
                # return Response("All data here")

            except ObjectDoesNotExist:
                return redirect('/serviceprovider/login/')
                # return Response({'message': 'You are not Logged In...'})
        except KeyError:
            return redirect('/serviceprovider/login/')
    
    if request.method == "POST":
        try:
            token = request.session['token']
            try:    
                
                condata = []
                
                spobj = Serviceprovider.objects.get(token_id = token)
                if spobj.services != []:
                    for obj in spobj.services:
                        if obj.service_name == request.POST['service_name'] and obj.service_category == request.POST['service_category']:
                            data = {
                                'title':'Try Again!',
                                'message':'Service Already Exists...',
                                'icon':'warning',
                                'url': '/serviceprovider/addservice/',
                                'token':token,
                            }
                            # return redirect('/serviceprovider/addservice/')
                            return render(request, 'serviceProvider/services.html', data)
                            # return Response("Service Already Exists")

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
                    spobj.save()
                    # print(service)
                    data = {
                        'title':'Good Job!',
                        'message':'Service Added Successfully...',
                        'icon':'success',
                        'url': '/serviceprovider/addservice/',
                        'token':token,
                        'data': service.data,
                    }
                    return render(request, 'serviceProvider/services.html', data)
                    # return Response(service.data)
                    
                return Response(service.errors)

            except ObjectDoesNotExist:
                # return Response({'message': 'You are not Logged In...'})
                return redirect('/serviceprovider/login/')
        except KeyError:
            return redirect('/serviceprovider/login/')


@api_view(['PUT'])
def updateservice(request, asid):
    
    if request.method == "PUT":
        try:
            token = request.session['token']
            spobj = Serviceprovider.objects.get(token_id = token)
            if request.POST['status'] == "Reject":
                for obj in spobj.applied_service:
                    if obj.asid == int(asid) and obj.status != "Accepted":
                        cusobj = Customer.objects.get(id = obj.customer_id)
                        for services in cusobj.services_requested:
                            if int(services.service_id) == int(obj.service_id) and int(services.service_provider) == int(spobj.id):
                                apobj = Appliedservice.objects.get(spid = spobj.id, asid = int(asid))
                                apobj.status = request.POST['status']
                                apobj.save()
                                services.status = request.POST['status']
                                cusobj.save()
                                print("here",services.service_name)
                        obj.status = request.POST['status']
                        spobj.save()
                        return Response("Status Updated")
                return Response("Service is Accepted, Can't reject it or no such service present")
            else:
                print(request.POST['status'])
                for obj in spobj.applied_service:
                    print("For", obj.asid)
                    if obj.asid == int(asid):
                        cusobj = Customer.objects.get(id = obj.customer_id)
                        for services in cusobj.services_requested:
                            if int(services.service_id) == int(obj.service_id) and int(services.service_provider) == int(spobj.id):
                                apobj = Appliedservice.objects.get(spid = spobj.id, asid = int(asid))
                                apobj.status = request.POST['status']
                                apobj.save()
                                services.status = request.POST['status']
                                cusobj.save()
                                print("here",services.service_name)
                        obj.status = request.POST['status']
                        spobj.save()
                        return Response("Status Updated")
                return Response("No such service present")
        except ObjectDoesNotExist:
            return Response({'message': 'You are not Logged In...'})

@api_view(['DELETE'])
def deleteservice(request, sid):
    if request.method == 'DELETE':
        # if request.method == "GET":
        try:
            token = request.session['token']
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

@api_view(['GET'])
def appliedservices(request):
    if request.method == 'GET':
        token = request.session['token']
        srprObj = Serviceprovider.objects.get(token_id = token)
        

        serviceLS = ServiceList.objects.filter(spid=srprObj.id)        
        return render(request, 'serviceProvider/appliedService.html', {'token':token,'srprObj':srprObj,'serviceLS':serviceLS})

        