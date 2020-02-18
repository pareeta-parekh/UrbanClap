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
        csid = request.GET['csid']

        print(cid)
        print(sid)
        print(spid)
        print(desc)
        print(rating)
        print(csid)

        try:
            print("in try")
            abc = CustComments.objects.get(csid = csid, cid = cid , sid = sid , spid = spid)
            print("abc" , abc)
            return Response("Already Commented")
        except:
            print("in except")
            cdesc = CustComments.objects.create(
                sid = sid,
                spid = spid,
                csid = csid,
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
            return Response("Comment Successfull")

