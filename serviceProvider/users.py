from .models import *
from .serializers import *
from django.shortcuts import render,redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from random import sample

from rest_framework import status

@api_view(['GET', 'POST'])
def spregister(request):
    if request.method == 'GET':
        # listdata = Serviceprovider.objects.all()
        # print(listdata.values())
        # serializer = SPSerializer(listdata, many=True)
        # return Response(serializer.data)

        return render(request, 'serviceProvider/registration.html')

    if request.method == 'POST':
        serializer = SPSerializer(data = request.data)

        if serializer.is_valid():
            title = 'Good Job!'
            message = 'Registation Successfully...!'
            icon = 'success'
            serializer.save()
            return render(request, 'serviceProvider/registration.html',{'title':title,'message': message, 'icon': icon} )

        # title = 'Try again!'
        # message = serializer.errors
        # icon = 'warning'
        # return render(request, 'serviceProvider/registration.html',{'title':title,'message': message, 'icon': icon})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )        
        

@api_view(['GET','POST'])
def sprlogin(request):
    if request.method == 'GET':
        return render(request, 'serviceProvider/login.html')

    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        try:
            servicePR = Serviceprovider.objects.get(email=email)
            
            try:
                servicePR = Serviceprovider.objects.get(password=password)
                
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

                    request.session['token'] = token.key
                    data = {
                        'title':'Good Job!',
                        'message':'You are LoggedIn...',
                        'icon':'success',
                        'url': '/serviceprovider/addservice/',
                    }
                    # return redirect('/serviceprovider/addservice/')
                    return render(request, 'serviceProvider/blank.html', data)
                    # return Response({'message': 'You are LoggedIn...'})

                else:

                    request.session['token'] = servicePR.token_id
                    data = {
                        'title':'Good Job!',
                        'message':'You are already LoggedIn...',
                        'icon':'success',
                        'url': '/serviceprovider/addservice/',
                    }
                    # return redirect('/serviceprovider/addservice/')
                    return render(request, 'serviceProvider/blank.html', data)
                    # return Response({'message': 'You are already LoggedIn...'})
            except ObjectDoesNotExist:
                title = 'Try again!'
                message = 'Password does not match...'
                icon = 'error'
                return render(request, 'serviceProvider/login.html',{'title':title,'message': message, 'icon': icon})

        except ObjectDoesNotExist:
            title = 'Try again!'
            message = 'Email not found...'
            icon = 'error'
            return render(request, 'serviceProvider/login.html',{'title':title,'message': message, 'icon': icon})
            # return Response({'message': 'Email not found...'})

@api_view(['GET'])
def sprlogout(request):
    del request.session['token']
    return redirect('/serviceprovider/login/')
    # try:
    #     servicePR = Serviceprovider.objects.get(token_id = token)
    #     servicePR.token_id = None
    #     servicePR.save()
    #     return Response({'message': 'Logged out...'})
    # except ObjectDoesNotExist:
    #     return Response({'message': 'Record not found...'})