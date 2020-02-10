from serviceProvider.models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def showServices(request):
    services = ServiceList.objects.all()
    if request.method == 'GET':
        context = {"services": services}
        return render(request, "showlist.html", context)

    if request.method == 'POST':
        for obj in services:
            try:
                print(request.POST[obj.service_name])
                print(obj.service_cost)
                ser = Serviceprovider.objects.get(id = 1)
                if ser.applied_service == []:
                    asid = 1
                else:
                    asid = ser.applied_service[len((ser.applied_service))].asid + 1
                print(ser)
                aplser = Appliedservice.objects.create(
                    asid = asid,
                    customer_id = 1,
                    service_id = obj.sid,
                    comments = [],
                    status = "Pending"
                )                
                ser.applied_service.append(aplser)
                ser.save()
            except:
                print("unchecked")

           
            
    return Response("checked")
