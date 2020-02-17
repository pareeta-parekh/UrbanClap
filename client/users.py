#users
from django.shortcuts import render,redirect
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
        # client = Customer.objects.all()
        # print(client.values())
        # serializers = CustomerSerializer(client, many=True)
        # return Response(serializers.data)
        return render(request, 'registration.html')

    if request.method == 'POST':
        if request.data['password'] != request.data['cpassword']:
            data = {
                'title' :'Try again!',
                'message' : ErrorMessages._meta.get_field('error_confirm_password').get_default(),
                'icon' : 'error',
            }
            return Response(data)
            # return render(request, 'registration.html',{'title':title,'message': message, 'icon': icon} )
        else:   
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
                data = {
                    'title' : 'Good Job!',
                    'message' : SuccessMessages._meta.get_field('success_registered').get_default(),
                    'url':'/client/login/',
                    'icon' : 'success',
                }
                return Response(data)
                
                # return render(request, 'registration.html',{'title':title,'message': message, 'icon': icon} )
                # serializer.save()
                # return Response("done!")
            
            data = {
                'title' : 'Try again!',
                'message' : ErrorMessages._meta.get_field('error_email_exists').get_default(),
                'icon' : 'warning',
            }
            return Response(data)
            # return render(request, 'registration.html',{'title':title,'message': message, 'icon': icon})
            # return Response(
            #     serializer.errors,
            #     status=status.HTTP_400_BAD_REQUEST
            #     )


@api_view(['GET','POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        try:
            cust = Customer.objects.get(email=email)
            try:
                cust = Customer.objects.get(email=email,password=password)
            
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

                    request.session['token'] = token.key
                    data = {
                        'token':token,
                        'title':'Good Job!',
                        'message': SuccessMessages._meta.get_field('success_login').get_default(),
                        'icon':'success',
                        'url': '/client/category/',
                    }
                    return Response(data)
                    # return redirect('/serviceprovider/addservice/')
                    # return render(request, 'blank.html', data)
                    # return Response({'message': 'You are LoggedIn...'})

                else:
                    request.session['token'] = cust.token_id
                    data = {
                        'token':servicePR.token_id,
                        'title':'Good Job!',
                        'message': SuccessMessages._meta.get_field('sucess_already_login').get_default(),
                        'icon':'success',
                        'url': '/client/category/',
                    }
                    return Response(data)
                    # return redirect('/serviceprovider/addservice/')
                    # return render(request, 'blank.html', data)
                    # return Response({'message': 'You are already LoggedIn...'})

            except ObjectDoesNotExist:
                data = {
                    'title': 'Try again!',
                    'message' : ErrorMessages._meta.get_field('error_password_credentials').get_default(),
                    'icon' : 'error',
                }
                return Response(data)
                # return render(request, 'login.html',{'title':title,'message': message, 'icon': icon})
        except ObjectDoesNotExist:
            data = {
                'title': 'Try again!',
                'message': ErrorMessages._meta.get_field('error_email_credentials').get_default(),
                'icon': 'error',
            }
            return Response(data)
            # return render(request, 'login.html',data)

@api_view(['GET'])
def logout(request):
    try:
        token = request.session['token']
        try:
            cust = Customer.objects.get(token_id = token)
            cust.token_id = None
            cust.save()
            del request.session['token']
            return redirect('/client/login/')
            # return Response({'message': 'Logged out...'})
        except ObjectDoesNotExist:
            title = 'Try again!'
            message = ErrorMessages._meta.get_field('error_record_not_found').get_default()
            icon = 'error'
            return render(request, 'login.html',{'title':title,'message': message, 'icon': icon})
            # return Response({'message': 'Record not found...'})
    except KeyError:
        data = {
            'title': 'Try again!',
            'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
            'url': '/client/login/',
            'icon': 'error',  
        }
        return render(request, 'blank.html', data)


@api_view(['GET','POST'])
def updatepass(request):
    if request.method == 'GET':
        try:
            token = request.session['token']
            try:
                cobj = Customer.objects.get(token_id = token)
                return render(request, 'updatePassword.html', {'token':token})
            except ObjectDoesNotExist:
                data = {
                    'title': 'Try again!!!',
                    'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                    'url': '/client/login/',
                    'icon': 'error',
                }
                return render(request, 'blank.html',data)
        except KeyError:
            return redirect('/client/login/')

    if request.method == 'POST':
        try:
            token = request.session['token']
            try:
                cobj = Customer.objects.get(token_id = token)
                if cobj.password == request.POST['old_password']:
                    cobj.password = request.POST['new_password']
                    cobj.save()
                    # return Response("Passwword Updated")
                    data = {
                        'token':token,
                        'title': 'Good Job!',
                        'message': SuccessMessages._meta.get_field('success_update_password').get_default(),
                        'url': '/client/login/',
                        'icon': 'success',
                    }
                    return Response(data)
                    # return render(request, 'blank.html',data)
                else:
                    data = {
                        'token':token,
                        'title': 'Try again!',
                        'message': 'Old Pasword invalid...',
                        'icon': 'warning',
                    }
                    return Response(data)
                    # return render(request, 'updatePassword.html',data)
            except ObjectDoesNotExist:
                # return Response({'message': 'Record not found'})
                data = {
                    'token':token,
                    'title': 'Try again!!!',
                    'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                    'icon': 'error',
                }
                return Response(data)
        except KeyError:
            data = {
                'title': 'Try again!!!',
                'message': ErrorMessages._meta.get_field('error_record_not_found').get_default(),
                'url': '/client/login/',
                'icon': 'error', 
            }
            return render(request, 'blank.html',data)

    # if request.method == 'POST':
    #     try:
    #         cobj = Customer.objects.get(token_id = token)
    #         if cobj.password == request.POST['old_password']:
    #             cobj.password = request.POST['new_password']
    #             cobj.save()
    #             return Response("Passwword Updated")
    #     except:
    #         return Response({'message': 'Record not found'})