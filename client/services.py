from serviceProvider.models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def showServices(request):
    if request.method == 'GET':
        id = 1
        print("-------- in show service get-----------")
        try:
            sid = request.GET['service_id']
            pk = request.GET['provider_id']
            print("sid", sid)
            ser = Serviceprovider.objects.get(id=1)
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
    return Response("checked")


@api_view(['GET', 'POST'])
def categoryShow(request):
    print("-------in function---------")
    if request.method == 'POST':
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
                context = {"obj": obj}
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
                context = {"obj": obj}
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
                context = {"obj": obj}
                return render(request, "plumber.html", context)
        except Exception as e:
            # print(e)
            # return render(request , "category.html")
            pass
    return render(request, "category.html")


def deleteService(request):
    name = ""
    delObj = CustService.objects.get(service_name = name)
    if delObj.status == "Pending":
        delObj.is_deleted = True
        return Response("Deleted!")
    else:
        return Response("Invalid Request")

