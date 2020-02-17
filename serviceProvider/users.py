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
        print(request.data)
        if request.data['password'] != request.data['cpassword']:
            title = 'Try again!'
            message = ErrorMessages._meta.get_field('error_confirm_password').get_default()
            icon = 'error'
            return render(request, 'serviceProvider/registration.html',{'title':title,'message': message, 'icon': icon} )
        else:   
            serializer = SPSerializer(data = request.data)

            if serializer.is_valid():
                title = 'Good Job!'
                message = SuccessMessages._meta.get_field('success_registered').get_default()
                icon = 'success'
                serializer.save()
                return render(request, 'serviceProvider/registration.html',{'title':title,'message': message, 'icon': icon} )

            title = 'Try again!'
            message = ErrorMessages._meta.get_field('error_email_exists').get_default()
            icon = 'warning'
            return render(request, 'serviceProvider/registration.html',{'title':title,'message': message, 'icon': icon})
            # return Response(
            #     serializer.errors,
            #     status=status.HTTP_400_BAD_REQUEST
            #     )        
        

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

                    request.session['token'] = token.key
                    data = {
                        'title':'Good Job!',
                        'message': SuccessMessages._meta.get_field('success_login').get_default(),
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
                        'message': SuccessMessages._meta.get_field('sucess_already_login').get_default(),
                        'icon':'success',
                        'url': '/serviceprovider/addservice/',
                    }
                    # return redirect('/serviceprovider/addservice/')
                    return render(request, 'serviceProvider/blank.html', data)
                    # return Response({'message': 'You are already LoggedIn...'})
            except ObjectDoesNotExist:
                title = 'Try again!'
                message = ErrorMessages._meta.get_field('error_password_credentials').get_default()
                icon = 'error'
                return render(request, 'serviceProvider/login.html',{'title':title,'message': message, 'icon': icon})

        except ObjectDoesNotExist:
            data = {
                'title': 'Try again!',
                'message': ErrorMessages._meta.get_field('error_email_credentials').get_default(),
                'icon': 'error',
            }
            return render(request, 'serviceProvider/login.html',data)
            # return Response({'message': 'Email not found...'})

@api_view(['GET'])
def sprlogout(request):
    if request.method == 'GET':
        try:
            token = request.session['token']
            try:
                
                servicePR = Serviceprovider.objects.get(token_id = token)
                servicePR.token_id = None
                servicePR.save()
                del request.session['token']
                return redirect('/serviceprovider/login/')
                # return Response({'message': 'Logged out...'})
            except ObjectDoesNotExist:
                title = 'Try again!'
                message = ErrorMessages._meta.get_field('error_record_not_found').get_default()
                icon = 'error'
                return render(request, 'serviceProvider/login.html',{'title':title,'message': message, 'icon': icon})
                # return Response({'message': 'Record not found...'})

        except KeyError:
            data = {
                'title': 'Try again!',
                'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                'url': '/serviceprovider/login/',
                'icon': 'error',
                
            }
            return render(request, 'serviceProvider/blank.html', data)
        
   

@api_view(['PUT'])
def updatepass(request):
    if request.method == 'PUT':
        try:
            token = request.session['token']
            try:
                spobj = Serviceprovider.objects.get(token_id = token)
                
                if spobj.password == request.POST['old_password']:
                    spobj.password = request.POST['new_password']
                    spobj.save()
                # return Response("Passwword Updated")
                data = {
                    'title': 'Good Job!',
                    'message': SuccessMessages._meta.get_field('success_update_password').get_default(),
                    'icon': 'success',
                }
                return render(request, 'serviceProvider/updatepassword.html',data)
            except ObjectDoesNotExist:
                # return Response({'message': 'Record not found'})
                data = {
                    'title': 'Try again!!!',
                    'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                    'url': '/serviceprovider/updatepass/',
                    'icon': 'error',
                }
                return render(request, 'serviceProvider/blank.html',data)
        except KeyError:
            data = {
                'title': 'Try again!!!',
                'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                'url': '/serviceprovider/login/',
                'icon': 'error', 
            }
            return render(request, 'serviceProvider/blank.html',data)
