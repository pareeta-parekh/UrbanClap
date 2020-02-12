from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from serviceProvider.models import *

@api_view(['GET', 'POST'])
def srpr_chat(request, token, cust_id, service_id):
        
    if request.method == 'GET':
        try:
            srprObj = Serviceprovider.objects.get(token_id = token)
            
            # messages = Appsercomment.objects.filter(user_id = srprObj.id)
            
            clientObj = Customer.objects.get(id = cust_id)
            ch = 0
        
            for apsr in srprObj.applied_service:
                
                if apsr.comments == []:
                    return Response({'message': 'No chat found..'})

                if apsr.customer_id == clientObj.id and service_id == apsr.service_id:
                    
                    data = []
                    
                    for chats in apsr.comments:

                        data.append({
                            'user_type': chats.user_type,
                            'user_id': chats.user_id,
                            'text':chats.text
                            },)
                    return Response(data)
    
                else:
                    ch = ch + 1

            if ch != 0:
                return Response({'message': 'No chat found..'})
            
        except ObjectDoesNotExist:
            return Response({'message': 'Record not found...'})

    elif request.method == 'POST':
        try:           
            srprObj = Serviceprovider.objects.get(token_id = token)

            clientObj = Customer.objects.get(id = cust_id)
            # services = ServiceList.objects.get(sid=service_id)

            ch=0
            for apsr in srprObj.applied_service:
                
                if apsr.status == 'Accepted':
                    appserCommentObj = Appsercomment.objects.create(
                        user_type = "Service Provider",
                        user_id = srprObj.id,
                        text = request.data['message']
                    )

                    if apsr.customer_id == clientObj.id and service_id == apsr.service_id:
                        
                        apsr.comments.append(appserCommentObj)

                        appserCommentObj.save()
                        srprObj.save()

                        data = []
                    
                        for chats in apsr.comments:
                            
                            data.append({
                                'user_type': chats.user_type,
                                'user_id': chats.user_id,
                                'text':chats.text
                                },)
                        return Response(data)
                    
                    elif service_id == apsr.service_id:
                        ch = ch + 1
                        
            if ch != 0:
                return Response({'message': 'No applied services found..!'})
                
            return Response({'message': 'You cannot write message until services not accepted...'})
        except ObjectDoesNotExist:
            return Response({'message': 'Record not found...'})    