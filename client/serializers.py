from rest_framework import serializers
from serviceProvider.models import *

class CustomerSerializer(serializers.ModelSerializer):
    address = []
    services_requested = "null"
    class Meta:
        model = Customer
        fields = ['user_name' , 'password' , 'email' , 'phone']
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {'input_type' : 'password'}
            }
        }

    def create(self , validated_data):
        # print("--------------------------------")
        # print("context =" , self.context)
        # print("validated_data = " , validated_data)
        client = Customer.objects.create(
            user_name = validated_data['user_name'],
            password = validated_data['password'],
            email = validated_data['email'],
            phone = validated_data['phone'],
            address = self.context,
            services_requested = []
        )
        return client


