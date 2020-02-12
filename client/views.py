from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

# @api_view(['GET'])

# def comments(request):
#     if request.method == 'GET':
#         ids = request.GET['service_id']
#         cust_id = request.GET['customer_id']
#         print(cust_id)
#         print("-----------------------service id", ids)
#         delObj = CustService.objects.get(service_id=ids)
#         if delObj.status == "Pending":

