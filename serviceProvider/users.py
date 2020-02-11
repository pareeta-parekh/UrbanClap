from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

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