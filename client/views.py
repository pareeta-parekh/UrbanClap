from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *

# Create your views here.

@api_view(['GET'])
def comments(request):
    if request.method == 'GET':
        print("in comments")
        cid = request.GET['customer_id']
        sid = request.GET['service_id']
        sname = request.GET['service_name']
        spid = request.GET['service_provider']
        desc = request.GET['desc']
        rating = request.GET['rate']

        cdesc = CustComments.objects.create(
            sid = sid,
            spid = spid,
            cid = cid,
            comment_desc = desc,
            rating = rating
        )
        custService = ServiceList.objects.get(sid = sid , spid = spid)
        print("custService " , custService)
        print()
        custService.comments.append(cdesc)
        custService.save()
        return Response("commented")

