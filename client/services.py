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
                serObj = CustService.objects.create(
                service_name = request.POST[obj.service_name],
                service_price = obj.service_cost,
                status = "Pending",
                service_provider = "1"
                )
                id = 1
                cust = Customer.objects.get(id = id)
                cust.services_requested.append(serObj)
                cust.save()

                aplser = Appliedservice.objects.create(
                    customer_id = id,
                    service_id = obj.sid,
                    comments = [],
                    status = "Pending"
                )

                ser = Serviceprovider.objects.get(id = 1)
                ser.applied_service.append(aplser)
                ser.save()
            except:
                print("unchecked")

           
            
    return Response("checked")
