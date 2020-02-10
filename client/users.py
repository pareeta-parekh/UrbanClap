from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *
from .serializers import *

@api_view(['GET', 'POST'])
def register(request):

    if request.method == 'GET':
        client = Customer.objects.all()
        print(client.values())
        serializers = CustomerSerializer(client, many=True)
        return Response(serializers.data)

    if request.method == 'POST':
        addressline_1 = request.data['addline_1']
        addressline_2 = request.data['addline_2']
        country = request.data['country']
        state = request.data['state']
        city = request.data['city']
        zipcode = request.data['zipcode']

        address = Address.objects.create(
            addline_1=addressline_1,
            addline_2=addressline_2,
            country=country,
            state=state,
            city=city,
            zipcode=zipcode
        )

        serializers = CustomerSerializer(data=request.data, context=address)
        if serializers.is_valid():
            serializers.save()
            return Response("done!")
        return Response(serializers.errors)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        logclient = Customer.objects.get(email=email, password=password)
        if logclient != "":
            return Response("logged In!")
        return Response("Error!!!")
