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
            try:
                sid = request.GET['service_id']
                pk = request.GET['provider_id']
                print("sid", sid)
                print("pk", pk)
                ser = Serviceprovider.objects.get(id=pk)
                if ser.applied_service == []:
                    asid = 1
                else:
                    asid = ser.applied_service[len(
                        ser.applied_service) - 1].asid + 1

                aplser = Appliedservice.objects.create(
                    asid=asid,
                    spid = ser,
                    customer_id=cust,
                    service_id = ServiceList.objects.get(sid = int(sid), spid = ser),
                    chat=[],
                    status="Pending"
                )
                print("aplser ", aplser)
                ser.applied_service.append(aplser)
                ser.save()
                obj = ServiceList.objects.get(sid=sid, spid=ser)
                print("--------------obj---------", obj)
                cust = Customer.objects.get(id=id)
                if cust.services_requested == []:
                    csid = 1
                else:
                    csid = cust.services_requested[len(cust.services_requested) - 1].csid + 1
                serObj = CustService.objects.create(
                    csid = csid,
                    cust_id=cust,
                    service_name=obj.service_name,
                    service_price=obj.service_cost,
                    status="Pending",
                    service_provider=obj.spid,
                    service_id=obj,
                )
                
                cust.services_requested.append(serObj)
                cust.save()
            except Exception as e:
                print(e)
                print("unchecked")
        except ObjectDoesNotExist:
            return render(request, "category.html", {'context': 'You are not LoggedIn...'})

@api_view(['GET' , 'POST'])
def categoryShow(request):
    print("-------in function---------")
    if request.method == 'GET':
        try:
            token = request.session['token']
            try:
                
                cust = Customer.objects.get(token_id = token)
                return render(request, "category.html", {'token':token})
            except ObjectDoesNotExist:
                title = 'Try again!'
                message = ErrorMessages._meta.get_field('error_record_not_found').get_default()
                icon = 'error'
                return render(request, 'login.html',{'title':title,'message': message, 'icon': icon})
                # return Response("Plz Login..")
        except KeyError:
            return redirect('/client/login/')
    if request.method == 'POST':
        try:
            token = request.session['token']
            cust = Customer.objects.get(token_id = token)
            print(cust)
            print("-------in post----------")
            try:
                if request.POST['Salon'] == 'Salon':
                    type_name = request.POST['Salon']
                    print(type_name)
                    obj = ServiceList.objects.filter(service_category=type_name)
                    ratdictionary = {}
                    sum = 0
                    comments = CustComments.objects.all()
                    for sl in obj:
                        desc = CustComments.objects.filter(sid = sl, spid = sl.spid)
                        print("desc",desc)
                        for des in desc:
                            sum = (sum + int(des.rating))
                        print("----" , desc.count())
                        if int(desc.count()) == 0:
                            desclen = 1
                        else:
                            desclen = int(desc.count())
                        ratdictionary[str(sl.sid)+'_'+str(sl.spid.id)] = sum / desclen
                        sum = 0
                    print(ratdictionary)
                    objduplicate = obj
                    for cusapp in cust.services_requested:
                        for objs in obj:
                            print("objs", objs.id)
                            print("cusappserid", cusapp.service_id.id)
                            print("cussp", cusapp.service_provider.id)
                            print("objspid", objs.spid.id)
                            if cusapp.status != "Completed" and cusapp.status != "Reject":
                                if cusapp.service_id == objs and cusapp.service_provider == objs.spid and cusapp.is_deleted == False:
                                    objduplicate = objduplicate.exclude(sid = objs.sid, spid = objs.spid)
                                    print("status", cusapp.status)
                                    print(objs.service_name)
                            else:
                                print("else---------")
                                print(objs.service_name)
                                
                                # context = {"desc" : desc }
                    print("objduplicate",objduplicate)
                    context = {"obj": objduplicate , 'token': token , "desc" : comments, "ratings" : ratdictionary}
                    return render(request, "salon.html", context)
            except Exception as e:
                # print(e)
                # return render(request , "category.html")
                pass

            try:
                if request.POST['Carpenter'] == 'Carpenter':
                    type_name = request.POST['Carpenter']
                    print("type_name",type_name)
                    desc = CustComments.objects.all()
                    obj = ServiceList.objects.filter(service_category=type_name)
                    ratdictionary = {}
                    sum = 0
                    comments = CustComments.objects.all()
                    for sl in obj:
                        desc = CustComments.objects.filter(sid = sl, spid = sl.spid)
                        print("desc",desc)
                        for des in desc:
                            sum = (sum + int(des.rating))
                        print("----" , desc.count())
                        if int(desc.count()) == 0:
                            desclen = 1
                        else:
                            desclen = int(desc.count())
                        ratdictionary[str(sl.sid)+'_'+str(sl.spid.id)] = sum / desclen
                        sum = 0
                    print(ratdictionary)
                    objduplicate = obj
                    print("objduplicate",objduplicate)
                    for cusapp in cust.services_requested:
                        for objs in obj:
                            if cusapp.status != "Completed" and cusapp.status != "Reject":
                                if cusapp.service_id == objs and cusapp.service_provider == objs.spid and cusapp.is_deleted == False:
                                    objduplicate = objduplicate.exclude(sid = objs.sid, spid = objs.spid)
                                    print("status", cusapp.status)
                                    print(objs.service_name)
                            else:
                                print("else---------")
                                print(objs.service_name)
                    print("objduplicate",objduplicate)
                    context = {"obj": objduplicate, 'token': token , "desc" : comments , "ratings" : ratdictionary}
                    return render(request, "carpenter.html", context)
            except Exception as e:
                # print(e)
                # return render(request , "category.html")
                pass

            try:
                if request.POST['Plumber'] == 'Plumber':
                    type_name = request.POST['Plumber']
                    print(type_name)
                    desc = CustComments.objects.all()
                    obj = ServiceList.objects.filter(service_category=type_name)
                    ratdictionary = {}
                    sum = 0
                    comments = CustComments.objects.all()
                    for sl in obj:
                        desc = CustComments.objects.filter(sid = sl, spid = sl.spid)
                        print("desc",desc)
                        for des in desc:
                            sum = (sum + int(des.rating))
                        print("----" , desc.count())
                        if int(desc.count()) == 0:
                            desclen = 1
                        else:
                            desclen = int(desc.count())
                        ratdictionary[str(sl.sid)+'_'+str(sl.spid.id)] = sum / desclen
                        sum = 0
                    print(ratdictionary)
                    objduplicate = obj
                    for cusapp in cust.services_requested:
                        for objs in obj:
                            if cusapp.status != "Completed" and cusapp.status != "Reject":
                                if cusapp.service_id == objs and cusapp.service_provider == objs.spid and cusapp.is_deleted == False:
                                    objduplicate = objduplicate.exclude(sid = objs.sid, spid = objs.spid)
                                    print("status", cusapp.status)
                                    print(objs.service_name)
                            else:
                                print("else---------")
                                print(objs.service_name)
                    print("duplicate",objduplicate)
                    context = {"obj": objduplicate, 'token': token , "desc" : comments ,"ratings" : ratdictionary}
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
        print("sid-----------------", request.GET['service_id'])
        print("cid-----------------", request.GET['customer_id'])
        print("spid----------------", request.GET['service_provider'])
        ids = request.GET['service_id']
        cust_id = request.GET['customer_id']
        print(cust_id)
        print("-----------------------service id", ids)
        delObj = CustService.objects.filter(service_id = ServiceList.objects.get(id = int(request.GET['service_id'])),
                                        cust_id = Customer.objects.get(id = int(request.GET['customer_id'])),
                                        service_provider = Serviceprovider.objects.get(id = int(request.GET['service_provider'])))
        print("delObj--------------",delObj)
        for obj in delObj:
            if obj.status == "Pending" and obj.is_deleted != True:
                obj.is_deleted = True
                obj.save()
        delappObj = Appliedservice.objects.filter(service_id = ServiceList.objects.get(id = int(request.GET['service_id'])),
                                        customer_id = Customer.objects.get(id = int(request.GET['customer_id'])),
                                        spid = Serviceprovider.objects.get(id = int(request.GET['service_provider'])))
        print("delappObj--------------",delappObj)
        for obja in delappObj:
            if obja.status == "Pending" and obja.is_deleted != True:
                obja.is_deleted = True
                print(obja.is_deleted)
                obja.save()
        # if delObj.status == "Pending":
        #     delObj.is_deleted = True
        #     delObj.save()
        custObj = Customer.objects.get(id = int(request.GET['customer_id']))
        print(custObj)
        for i in custObj.services_requested:
            print(i.status)
            print("service id ", i.service_id)
            print("upper service id ", ids)
            if i.status == "Pending" and i.service_id == ServiceList.objects.get(id = int(ids)):
                print("in if")
                print(i.is_deleted)
                i.is_deleted = True
                print(i.is_deleted)
                custObj.save()
        spobj = Serviceprovider.objects.get(id = int(request.GET['service_provider']))
        for sp in spobj.applied_service:
            if sp.status == "Pending" and sp.service_id == ServiceList.objects.get(id = int(ids)):
                print("in if")
                print(sp.is_deleted)
                sp.is_deleted = True
                print(sp.is_deleted)
                spobj.save()
    return render(request, "showReqService.html")


@api_view(['GET'])
def req_service(request):
    # print("req service")
    try:
        token = request.session['token']
        cust_id = Customer.objects.get(token_id=token)
        print(cust_id)
        if request.method == 'GET':
            print("in method get")
            cust = []
            for obj in cust_id.services_requested:
                sobj = ServiceList.objects.filter(spid = obj.service_provider, sid = obj.service_id.sid)
                for objs in sobj:
                    if obj.is_deleted == False and objs.is_deleted == False:
                        cust.append(obj)
                print(obj.is_deleted)
            print(cust_id.services_requested)
            context = {"c_req": cust, 'token':token}
            return render(request, "showReqService.html", context)
    except KeyError:
        return redirect('/client/login/')

    # if request.method == 'POST':
    #     print("in method POST")
    #     print(cust_id.services_requested)
    #     context = {"c_req" : cust_id.services_requested}
    #     return render(request , "showReqService.html" , context)