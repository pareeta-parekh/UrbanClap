from .models import *
from .serializers import *
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET', 'POST'])
def addservice(request):
    if request.method == "GET":
        try:
            token = request.session['token']
            print(token)
            try:

                spobj = Serviceprovider.objects.get(token_id = token)
                serviceLS = ServiceList.objects.filter(spid=spobj)
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
                # print("Service Cat", request.POST['service_category'])
                # return render(request, 'serviceProvider/services.html')
                # category = request.POST['category']
                condata = []
                
                spobj = Serviceprovider.objects.get(token_id = token)
                if spobj.services != []:
                    for obj in spobj.services:
                        if obj.service_name == request.POST['service_name'] and obj.service_category == request.POST['service_category']:
                            data = {
                                'title':'Try Again!',
                                'message':ErrorMessages._meta.get_field('error_service_exists').get_default(),
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
                condata.append(spobj)
                service = AddServiceSerializer(data = request.data, context = condata)
                if service.is_valid():
                    service.save()
                    spobj.save()
                    # print(service)
                    data = {
                        'title':'Good Job!',
                        'message':SuccessMessages._meta.get_field('success_add_service').get_default(),
                        'icon':'success',
                        'url': '/serviceprovider/addservice/',
                        'token':token,
                        'data': service.data,
                    }
                    return render(request, 'serviceProvider/services.html', data)
                    # return Response(service.data)
                for err_key in service.errors:
                    title = err_key
                    msg = service.errors[err_key][0]
                    # print("\nError",service.errors[err_key][0])
                
                # return Response(service.errors)
                data = {
                    'title':title,
                    'message':msg,
                    'icon':'error',
                    'url': '/serviceprovider/addservice/',
                    'token':token,
                    'data': service.data,
                }
                return render(request, 'serviceProvider/services.html', data)

            except ObjectDoesNotExist:
                # return Response({'message': 'You are not Logged In...'})
                return redirect('/serviceprovider/login/')
        except KeyError:
            return redirect('/serviceprovider/login/')



@api_view(['POST'])
def updateservice(request):
    if request.method == "POST":
        try:
            token = request.session['token']
            try:
                asid = request.POST['asid']
                spobj = Serviceprovider.objects.get(token_id = token)

                if request.POST['status'] == "Reject":
                    for obj in spobj.applied_service:
                        if obj.asid == int(asid) and obj.status != "Accepted":
                            cusobj = Customer.objects.get(id = obj.customer_id.id)
                            for services in cusobj.services_requested:
                                if services.service_id == obj.service_id and services.service_provider == spobj:
                                    apobj = Appliedservice.objects.get(spid = spobj, asid = int(asid))
                                    apobj.status = request.POST['status']
                                    apobj.save()
                                    services.status = request.POST['status']
                                    cusobj.save()
                                    print("here",services.service_name)
                            obj.status = request.POST['status']
                            spobj.save()
                            return Response(SuccessMessages._meta.get_field('success_service_status').get_default())
                    return Response("Service is Accepted, Can't reject it or no such service present")
                else:
                    print(request.POST['status'])
                    for obj in spobj.applied_service:
                        print("For", obj.asid)
                        if obj.asid == int(asid):
                            cusobj = Customer.objects.get(id = obj.customer_id.id)
                            for services in cusobj.services_requested:
                                if services.service_id == obj.service_id and services.service_provider == spobj:
                                    apobj = Appliedservice.objects.get(spid = spobj, asid = int(asid))
                                    apobj.status = request.POST['status']
                                    apobj.save()
                                    services.status = request.POST['status']
                                    cusobj.save()
                                    print("here",services.service_name)
                            obj.status = request.POST['status']
                            spobj.save()
                            return Response(SuccessMessages._meta.get_field('success_service_status').get_default())
                    return Response("No such service present")
            except ObjectDoesNotExist:
                data = {
                    'title': 'Try again!!!',
                    'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                    'url': '/serviceprovider/addservice/',
                    'icon': 'error',
                }
                return render(request, 'serviceProvider/services.html',data)
                # return Response('You are not Logged In...')
        except KeyError:
            return redirect('/serviceprovider/login/')

@api_view(['GET'])
def deleteservice(request,sid):
    if request.method == 'GET':
        # print("sid", request.GET['sid'])
        # print("spid", request.GET['spid'])
        # print("cid", request.GET['cid'])
        try:
            token = request.session['token']
            try:
                spobj = Serviceprovider.objects.get(token_id = token)                    
                count = 0
                for obj in spobj.applied_service:
                    if obj.service_id.id == int(sid) and (obj.status == "Reject" or obj.status == "Pending"):
                        count = count + 1
                if count == 0:
                    sobj = ServiceList.objects.get(sid = sid)
                    for obj in spobj.services:
                        if obj.sid == int(sid):
                            obj.is_deleted = True
                            spobj.save()
                    sobj.is_deleted = True
                    sobj.save()
                    # spobj = Serviceprovider.objects.get(token_id = token)
                    # serviceLS = ServiceList.objects.filter(spid=spobj)
                    # return render(request, 'serviceProvider/services.html', {'token':token,'services':serviceLS})
                    # return Response("Deleted successfully")
                    data = {
                        'token':token,
                        'title': 'Good Job!',
                        'message': SuccessMessages._meta.get_field('success_delete_request').get_default(),
                        'url': '/serviceprovider/addservice/',
                        'icon': 'success',
                    }
                    return render(request, 'serviceProvider/services.html',data)
                else:
                    return Response("Inavlid Function")

            except ObjectDoesNotExist:
                # return Response({'message': 'You are not Logged In...'})
                data = {
                    'title': 'Try again!!!',
                    'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                    'url': '/serviceprovider/addservice/',
                    'icon': 'error',
                }
                return render(request, 'serviceProvider/services.html',data)
        except KeyError:
            return redirect('/serviceprovider/login/')

@api_view(['GET'])
def appliedservices(request):
    try:
        token = request.session['token']
        spobj = Serviceprovider.objects.get(token_id = token)
        print(len(spobj.applied_service)==0)
        return render(request, 'serviceProvider/appliedService.html', {'token':token, 'services':spobj.applied_service})
    except KeyError:
        return redirect('/serviceprovider/login/')