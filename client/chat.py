from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from serviceProvider.models import *

@api_view(['GET', 'POST'])
def client_chat(request, srpr_id, service_id):
        
    if request.method == 'GET':
        try:
            
            token = request.session['token']
            
            clientObj = Customer.objects.get(token_id = token)
            
            # messages = Appsercomment.objects.filter(user_id = clientObj.id)

            srprObj = Serviceprovider.objects.get(id = srpr_id)

            # services = ServiceList.objects.get(sid=service_id)

            ch = 0
            for apsr in srprObj.applied_service:
                
                # if apsr.chat == []:
                #     data = {
                #         'message': 'No chat found...!',
                #         'token':token,
                #     }
                #     return render(request, 'chat.html', data)
                    # return Response({'message': 'No chat found..'})

                if apsr.customer_id == clientObj and service_id == apsr.service_id.sid and apsr.is_deleted == False and apsr.status == "Accepted":
                    print("Chat ", apsr.chat)
                    
                    # data = []
                    
                    # for chats in apsr.chat:
                                               
                    #     data.append({
                    #         'user_type': chats.user_type,
                    #         'user_id': chats.user_id,
                    #         'text':chats.text
                    #         },)
                    data = {'message':apsr.chat, 'token':token, 'chat_found': True, 'errors': False}
                    return render(request, 'chat.html', data)
                    # return Response(data)
                    
                else:
                    ch = ch+1
                    
            if ch != 0:
                data = {
                    
                    'message': 'No chat found...!',
                    'token':token,
                }
                return render(request, 'chat.html', data)
                # return Response({'message': 'No chat found..'})
            
        except ObjectDoesNotExist:
            return Response({'message': 'Record not found...'})

    elif request.method == 'POST':
        try:
            token = request.session['token']
            clientObj = Customer.objects.get(token_id = token)
            print("clientObj", clientObj)
            srprObj = Serviceprovider.objects.get(id = srpr_id)
            print("Sprid", srprObj)
            # services = ServiceList.objects.get(sid=service_id)
            
            ch = 0
            for apsr in srprObj.applied_service:
                print("serviceid", apsr.service_id.sid)
                print("cid", apsr.customer_id.id)
                try:
                    appliedSR = Appliedservice.objects.get(service_id=apsr.service_id.sid,
                    spid = srprObj,
                    customer_id = apsr.customer_id,
                    is_deleted = False,
                    status = "Accepted")
                except:
                    pass
                print("appl", appliedSR)
                if apsr.status == 'Accepted' and appliedSR.status == 'Accepted':
                    print("Accepted")
                    appserCommentObj = Appsercomment.objects.create(
                        user_type = "Client",
                        user_id = clientObj.id,
                        text = request.data['message']
                    )
                    
                    if apsr.customer_id == clientObj and service_id == apsr.service_id.sid and apsr.is_deleted == False:
                        print("in if append")
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
                        #         'text':chats.text
                        #         },)
                        # return redirect('/cleint/chat/{{}}/{{}}/')
                        data = {'message':apsr.chat, 'token':token, 'chat_found': True, 'errors': False}
                        return render(request, 'chat.html', data)
                        # return Response(data)
                    
                    elif service_id == apsr.service_id:
                        ch = ch + 1
                        
            if ch != 0:
                return Response({'message': 'No applied services found..!'})

            return Response({'message': 'Your request is not accepted...'})
        except:
            return Response({'message': 'Record not found...'})    