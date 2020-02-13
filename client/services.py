from serviceProvider.models import *
from .serializers import *
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def showServices(request):
    if request.method == 'GET':
        try:
            token = request.GET['token']
            print(token)
            cust = Customer.objects.get(token_id=token)
            id = cust.id
            print("-------- in show service get-----------")
            # try:
            sid = request.GET['service_id']
            pk = request.GET['provider_id']
            print("sid", sid)
            ser = Serviceprovider.objects.get(id=pk)
            if ser.applied_service == []:
                asid = 1
            else:
                asid = ser.applied_service[len(
                    ser.applied_service) - 1].asid + 1

            aplser = Appliedservice.objects.create(
                asid=asid,
                spid=pk,
                customer_id=int(id),
                service_id=int(sid),
                comments=[],
                status="Pending"
            )
            print("aplser ", aplser)
            ser.applied_service.append(aplser)
            ser.save()
            obj = ServiceList.objects.get(sid=sid, spid=pk)
            print("--------------obj---------", obj)
            serObj = CustService.objects.create(
                cust_id=int(id),
                service_name=obj.service_name,
                service_price=obj.service_cost,
                status="Pending",
                service_provider=obj.spid,
                service_id=obj.sid,
                comments = []
            )
            print("Serobj====================",serObj)
            cust = Customer.objects.get(id=id)
            cust.services_requested.append(serObj)
            cust.save()
            # except Exception as e:
            #     print(e)
            #     print("unchecked")
        except ObjectDoesNotExist:
            return render(request, "category.html", {'context': 'You are not LoggedIn...'})

@api_view(['GET' , 'POST'])
def categoryShow(request, token):
    print("-------in function---------")
    if request.method == 'GET':
        try:
            cust = Customer.objects.get(token_id = token)
            return render(request, "category.html", {'token':token})
        except:
            return Response("Plz Login..")
    if request.method == 'POST':
        try:
            cust = Customer.objects.get(token_id = token)
            print(cust)
            print("-------in post----------")
            try:
                if request.POST['Salon'] == 'Salon':
                    type_name = request.POST['Salon']
                    print(type_name)
                    objlist = []
                    obj = ServiceList.objects.filter(service_category=type_name)
                    objduplicate = obj
                    for cusapp in cust.services_requested:
                        for objs in obj:
                            if int(cusapp.service_id) == int(objs.sid) and int(cusapp.service_provider) == int(objs.spid):
                                objduplicate = objduplicate.exclude(sid = objs.sid, spid = objs.spid)
                                print("in if",objduplicate)
                            else:
                                print("else---------")
                                print(objs.service_name)
                    print("objduplicate",objduplicate)
                    context = {"obj": objduplicate, 'token': token}
                    return render(request, "salon.html", context)
            except Exception as e:
                # print(e)
                # return render(request , "category.html")
                pass

            try:
                if request.POST['Carpenter'] == 'Carpenter':
                    type_name = request.POST['Carpenter']
                    print(type_name)
                    obj = ServiceList.objects.filter(service_category=type_name)
                    objduplicate = obj
                    for cusapp in cust.services_requested:
                        for objs in obj:
                            if int(cusapp.service_id) == int(objs.sid) and int(cusapp.service_provider) == int(objs.spid):
                                objduplicate = objduplicate.exclude(sid = objs.sid, spid = objs.spid)
                                print(objs.service_name)
                            else:
                                print("else---------")
                                print(objs.service_name)
                    print(objduplicate)
                    context = {"obj": objduplicate, 'token': token}
                    return render(request, "carpenter.html", context)
            except Exception as e:
                # print(e)
                # return render(request , "category.html")
                pass

            try:
                if request.POST['Plumber'] == 'Plumber':
                    type_name = request.POST['Plumber']
                    print(type_name)
                    obj = ServiceList.objects.filter(service_category=type_name)
                    objduplicate = obj
                    for cusapp in cust.services_requested:
                        for objs in obj:
                            if int(cusapp.service_id) == int(objs.sid) and int(cusapp.service_provider) == int(objs.spid):
                                objduplicate = objduplicate.exclude(sid = objs.sid, spid = objs.spid)
                                print("in if",objs.service_name)
                            else:
                                print("else---------")
                                print(objs.service_name)
                    print("duplicate",objduplicate)
                    context = {"obj": objduplicate, 'token': token}
                    return render(request, "plumber.html", context)
            except Exception as e:
                # print(e)
                # return render(request , "category.html")
                pass
        except ObjectDoesNotExist:
            print("Except")
            return Response({'context': 'Record not found...'})
    return render(request, "category.html", {'token':token})

@api_view(['GET'])
def deleteService(request):
    if request.method == 'GET':
        ids = request.GET['service_id']
        cust_id = request.GET['customer_id']
        print(cust_id)
        print("-----------------------service id", ids)
        delObj = CustService.objects.get(service_id=ids)
        if delObj.status == "Pending":
            delObj.is_deleted = True
            delObj.save()
        custObj = Customer.objects.get(id=cust_id)
        print(custObj)
        for i in custObj.services_requested:
            print(i.status)
            print("service id ", i.service_id)
            print("upper service id ", ids)
            if i.status == "Pending" and i.service_id == ids:
                print("in if")
                print(i.is_deleted)
                i.is_deleted = True
                print(i.is_deleted)
                custObj.save()
    return render(request, "showReqService.html")


@api_view(['GET'])
def req_service(request, token):
    print("req service")
    cust_id = Customer.objects.get(token_id=token)
    print(cust_id)
    if request.method == 'GET':
        print("in method get")
        print(cust_id.services_requested)
        context = {"c_req": cust_id.services_requested}
        return render(request, "showReqService.html", context)

    # if request.method == 'POST':
    #     print("in method POST")
    #     print(cust_id.services_requested)
    #     context = {"c_req" : cust_id.services_requested}
    #     return render(request , "showReqService.html" , context)