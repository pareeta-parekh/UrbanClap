from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from serviceProvider.models import *


@api_view(['GET', 'POST'])
def srpr_chat(request, cust_id, service_id):
        
    if request.method == 'GET':
        try:
            token = request.session['token']
            srprObj = Serviceprovider.objects.get(token_id = token)
            
            # messages = Appsercomment.objects.filter(user_id = srprObj.id)

            clientObj = Customer.objects.get(id=cust_id)
            
            ch = 0
            for apsr in srprObj.applied_service:
                # if apsr.chat == []:
                #     return Response({'message': 'No chat found..'})
                if apsr.customer_id == clientObj and service_id == apsr.service_id.sid and apsr.is_deleted == False:
                    # data = []

                    # for chats in apsr.chat:

                    #     data.append({
                    #         'user_type': chats.user_type,
                    #         'user_id': chats.user_id,
                    #         'text': chats.text
                    #     },)
                    # return Response(data)
                    print("chat",apsr.chat)
                    data = {'message':apsr.chat, 'token':token, 'chat_found': True, 'errors': False}
                    return render(request, 'serviceProvider/chat.html', data)

                else:
                    ch = ch + 1

            if ch != 0:
                return render(request, 'serviceProvider/chat.html', {'chat_found': False, 'errors': False})
                # return Response({'message': 'No chat found..'})

        except ObjectDoesNotExist:
            return Response({'message': 'Record not found...'})

    elif request.method == 'POST':
        try:  
            token = request.session['token']         
            srprObj = Serviceprovider.objects.get(token_id = token)

            clientObj = Customer.objects.get(id=cust_id)
            # services = ServiceList.objects.get(sid=service_id)
            
            ch = 0
            for apsr in srprObj.applied_service:
                appliedSR = Appliedservice.objects.get(service_id=apsr.service_id.sid, spid = srprObj, customer_id = apsr.customer_id, is_deleted = False)
                print("applSR", appliedSR.status)

                if apsr.status == 'Accepted' and appliedSR.status == 'Accepted':
                    appserCommentObj = Appsercomment.objects.create(
                        user_type="Service Provider",
                        user_id=srprObj.id,
                        text=request.data['message']
                    )

                    if apsr.customer_id == clientObj and service_id == apsr.service_id.sid:

                        apsr.chat.append(appserCommentObj)
                        appliedSR.chat.append(appserCommentObj)
                        appliedSR.save()
                        appserCommentObj.save()
                        srprObj.save()

                        # data = []

                        # for chats in apsr.chat:

                        #     data.append({
                        #         'user_type': chats.user_type,
                        #         'user_id': chats.user_id,
                        #         'text': chats.text
                        #     },)
                        # return Response(data)
                        data = {'message':apsr.chat, 'token':token, 'chat_found': True, 'errors': False}
                        return render(request, 'serviceProvider/chat.html', data)

                    elif service_id == apsr.service_id:
                        ch = ch + 1

            if ch != 0:
                return Response({'message': 'No applied services found..!'})

            return Response({'message': 'You cannot write message until services not accepted...'})
        except ObjectDoesNotExist:
            return Response({'message': 'Record not found...'})
