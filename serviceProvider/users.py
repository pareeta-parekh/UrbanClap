from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from random import sample

@api_view(['GET', 'POST'])
def spregister(request):
    if request.method == 'GET':
        listdata = Serviceprovider.objects.all()
        print(listdata.values())
        serializer = SPSerializer(listdata, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SPSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['POST'])
def sprlogin(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        try:
            servicePR = Serviceprovider.objects.get(email=email, password=password)
            
            if servicePR.token_id == None:
                sequence = [i for i in range(100)]
                smple = sample(sequence, 5)
                user_token = ''.join(map(str, smple))

                token, created = Token.objects.get_or_create(user_id = user_token)

                if not created:
                    token.created = user_token
                    token.save()

                servicePR.token_id = token.key
                servicePR.save()

                return Response({'message': 'You are LoggedIn...'})

            else:
                return Response({'message': 'You are already LoggedIn...'})

        except ObjectDoesNotExist:
            return Response({'message': 'Email not found...'})

@api_view(['GET'])
def sprlogout(request):
    try:
        token = request.headers['token']
        servicePR = Serviceprovider.objects.get(token_id = token)
        servicePR.token_id = None
        servicePR.save()
        return Response({'message': 'Logged out...'})
    except ObjectDoesNotExist:
        return Response({'message': 'Record not found...'})

@api_view(['PUT'])
def updatepass(request):
    if request.method == 'PUT':
        try:
            spobj = Serviceprovider.objects.get(token_id = request.headers['token'])
            print(request.headers['token'])
            if spobj.password == request.POST['old_password']:
                spobj.password = request.POST['new_password']
                spobj.save()
            return Response("Passwword Updated")
        except:
            return Response({'message': 'Record not found'})