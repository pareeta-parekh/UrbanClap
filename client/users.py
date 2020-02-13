#users
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serviceProvider.models import *
from .serializers import *

from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from random import sample

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

        try:
            cust = Customer.objects.get(email=email, password=password)
            
            if cust.token_id == None:
                sequence = [i for i in range(100)]
                smple = sample(sequence, 5)
                user_token = ''.join(map(str, smple))

                token, created = Token.objects.get_or_create(user_id = user_token)

                if not created:
                    token.created = user_token
                    token.save()

                cust.token_id = token.key
                cust.save()

                return Response({'message': 'You are LoggedIn...'})

            else:
                return Response({'message': 'You are already LoggedIn...'})

        except ObjectDoesNotExist:
            return Response({'message': 'Email not found...'})

@api_view(['GET'])
def logout(request, token):
    try:
        cust = Customer.objects.get(token_id = token)
        cust.token_id = None
        cust.save()
        return Response({'message': 'Logged out...'})
    except ObjectDoesNotExist:
        return Response({'message': 'Record not found...'})


@api_view(['PUT'])
def updatepass(request, token):
    if request.method == 'PUT':
        try:
            cobj = Customer.objects.get(token_id = token)
            if cobj.password == request.POST['old_password']:
                cobj.password = request.POST['new_password']
                cobj.save()
                return Response("Passwword Updated")
        except:
            return Response({'message': 'Record not found'})