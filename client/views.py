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
        desc = request.GET['desc']

        custService = CustService.objects.filter(cust_id = int(cid) , service_id = sid)
        print("custService " , custService)
        for ser in custService:
            print("comments" , ser.comments)
            ser.comments = desc
            print("comments" , ser.comments)
            ser.save()
        return Response("commented")

