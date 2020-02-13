from rest_framework import serializers
from .models import *

class SPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serviceprovider
        fields = ['full_name', 'email', 'password', 'mobile'] 
        extra_kwargs = {
            'password':{
                'write_only' : True,
                'style':{'input_type' : 'passord'}
            }
        }
    
    def create(self, validated_data):
        spobj = Serviceprovider.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email'],
            password = validated_data['password'],
            mobile = validated_data['mobile'],
            services = [],
            applied_service = []
        )
        return spobj

class AddServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceList
        fields = ['service_category', 'service_name', 'service_desc', 'service_cost']
    
    def create(self, validated_data):
        serviceobj = ServiceList.objects.create(
            sid = self.context[1],
            spid = self.context[2],
            service_category = validated_data['service_category'],
            service_name = validated_data['service_name'],
            service_desc = validated_data['service_desc'],
            service_cost = validated_data['service_cost']
        )
        self.context[0].services.append(serviceobj)
        self.context[0].save()
        return serviceobj

class chatSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Appsercomment
        fields = "__all__"

class APPSRSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliedservice
        fields = '__all__'
        