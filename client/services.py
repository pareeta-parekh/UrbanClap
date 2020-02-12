from serviceProvider.models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
def showServices(request):
    if request.method == 'GET':
        try:
            token = request.GET['token']
            print(token)
            cust = Customer.objects.get(token_id= token)
            id = cust.id
            print("-------- in show service get-----------")
            try:
                sid = request.GET['service_id']
                pk = request.GET['provider_id']
                print("sid", sid)
                ser = Serviceprovider.objects.get(id=pk)
                if ser.applied_service == []:
                    asid = 1
                else:
                    asid = ser.applied_service[len(ser.applied_service) - 1].asid + 1

                aplser = Appliedservice.objects.create(
                    asid = asid,
                    customer_id=int(id),
                    service_id=int(sid),
                    comments=[],
                    status="Pending"
                )
                print("aplser " , aplser)
                ser.applied_service.append(aplser)
                ser.save()
                obj = ServiceList.objects.get(sid = sid , spid = pk)
                print("--------------obj---------" , obj)
                serObj = CustService.objects.create(
                        cust_id = int(id),
                        service_name = obj.service_name,
                        service_price = obj.service_cost,
                        status = "Pending",
                        service_provider = obj.spid
                        )
                cust = Customer.objects.get(id = id)
                cust.services_requested.append(serObj)
                cust.save()
            except Exception as e:
                print(e)
                print("unchecked")
        except ObjectDoesNotExist:
            return render(request, "category.html",{'context':'You are not LoggedIn...'})
        
    # return Response("checked")


@api_view(['GET', 'POST'])
def categoryShow(request, token):

    if request.method == 'GET':
        try:
            cust = Customer.objects.get(token_id = token)
            return render(request, "category.html")
        except ObjectDoesNotExist:
            return Response({'message': 'Record not found...'})
            

    print("-------in function---------")
    if request.method == 'POST':
        try:
            cust = Customer.objects.get(token_id = token)

            print("-------in post----------")
            # print(request.POST['Salon'])
            # print(request.POST['Carpenter'])
            # print(request.POST['Plumber'])
            try:
                if request.POST['Salon'] == 'Salon':
                    type_name = request.POST['Salon']
                    print(type_name)
                    obj = ServiceList.objects.filter(service_category=type_name)
                    print(obj)
                    context = {"obj": obj, 'token':token}
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
                    print(obj)
                    context = {"obj": obj, 'token':token}
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
                    print(obj)
                    context = {"obj": obj,'token':token}
                    return render(request, "plumber.html", context)
            except Exception as e:
                # print(e)
                # return render(request , "category.html")
                pass

            # return render(request, "category.html")
        except ObjectDoesNotExist:
            return Response({'Message': 'Record not found...'})
    
    return render(request, "category.html")
    


def deleteService(request):
    name = ""
    delObj = CustService.objects.get(service_name = name)
    if delObj.status == "Pending":
        delObj.is_deleted = True
        return Response("Deleted!")
    else:
        return Response("Invalid Request")

