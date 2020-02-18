from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *

# Create your views here.

@api_view(['GET'])
def comments(request):
    if request.method == 'GET':
        print("in comments")
        print(request.GET['customer_id'])
        cid = Customer.objects.get(id = int(request.GET['customer_id']))
        sid = ServiceList.objects.get(id = int(request.GET['service_id']))
        # sname = request.GET['service_name']
        spid = Serviceprovider.objects.get(id = int(request.GET['service_provider']))
        desc = request.GET['desc']
        rating = request.GET['rate']

        print(cid)
        print(sid)
        print(spid)
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
            for appl in spid.services:
                if appl.sid == sid.sid:
                    appl.comments.append(cdesc)
                    spid.save()
            custService = ServiceList.objects.get(sid = sid.sid , spid = spid)
            print("custService " , custService)
            print()
            custService.comments.append(cdesc)
            # print(custService.comments)
            custService.save()
            return Response("commented")

