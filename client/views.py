from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *

# Create your views here.

@api_view(['GET'])
def comments(request):
    if request.method == 'GET':
        print("in comments")
        cid = Customer.objects.get(id = request.GET['customer_id'])
        sid = ServiceList.objects.get(id = request.GET['service_id'])
        sname = request.GET['service_name']
        spid = Serviceprovider.objects.get(id = request.GET['service_provider'])
        desc = request.GET['desc']
        rating = request.GET['rate']

        print(cid)
        print(sid)
        print(spid)
        print(sname)
        print(desc)
        print(rating)

        try:
            print("in try")
            abc = CustComments.objects.get(cid = cid , sid = sid , spid = spid)
            print("abc" , abc)
            context = {'context' : "Already Commented!"}
            return render( request , "showReqService.html" , context)
        except:
            print("in except")
            cdesc = CustComments.objects.create(
                sid = sid,
                spid = spid,
                cid = cid,
                comment_desc = desc,
                rating = rating
            )
            custService = ServiceList.objects.get(sid = sid.id , spid = spid)
            print("custService " , custService)
            print()
            custService.comments.append(cdesc)
            custService.save()
            return Response("commented")

