from django.db import models
from django.db import models
from djongo.models import EmbeddedModelField, ArrayModelField


class CustComments(models.Model):
    sid = models.IntegerField(blank=False, null=False)
    spid = models.IntegerField(blank=False, null=False)
    cid = models.IntegerField(blank=False, null=False)
    comment_desc = models.CharField(max_length=255, blank=False, null=False)
    rating = models.IntegerField(blank=False, null=False)


class Address(models.Model):
    addline_1 = models.CharField(max_length=255, blank=False, null=False)
    addline_2 = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=30, blank=False, null=False)
    state = models.CharField(max_length=30, blank=False, null=False)
    city = models.CharField(max_length=30, blank=False, null=False)
    zipcode = models.IntegerField()


class CustService(models.Model):
    cust_id = models.IntegerField(null=False, blank=False)
    service_name = models.CharField(max_length=255, blank=False, null=False)
    service_price = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=30, blank=False, null=False)
    service_id = models.CharField(max_length=30, blank=False, null=False)
    service_provider = models.CharField(max_length=30, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Customer(models.Model):
    token_id = models.CharField(max_length=255, null=True)
    user_name = models.CharField(max_length=30, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone = models.IntegerField(null=False, blank=False)
    address = EmbeddedModelField(model_container=Address)
    services_requested = ArrayModelField(model_container=CustService)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class ServiceList(models.Model):
    sid = models.IntegerField(null=False, blank=False)
    spid = models.IntegerField(null=False, blank=False)
    service_category = models.CharField(
        max_length=120, null=False, blank=False)
    service_name = models.CharField(max_length=120, null=False, blank=False)
    service_desc = models.CharField(max_length=255, null=False, blank=False)
    service_cost = models.IntegerField(null=False, blank=False)
    comments = ArrayModelField(model_container=CustComments)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)


class Appsercomment(models.Model):
    user_type = models.CharField(max_length=30, null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=False)
    text = models.CharField(max_length=255)


class Appliedservice(models.Model):
    asid = models.IntegerField(null=False, blank=False)
    spid = models.IntegerField(null=False, blank=False)
    customer_id = models.IntegerField(null=False, blank=False)
    service_id = models.IntegerField(null=False, blank=False)
    chat = ArrayModelField(model_container=Appsercomment)
    status = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)


class Serviceprovider(models.Model):
    token_id = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=25, null=False, blank=False)
    email = models.EmailField(
        max_length=30, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    mobile = models.IntegerField(null=False, blank=False)
    services = ArrayModelField(model_container=ServiceList)
    applied_service = ArrayModelField(model_container=Appliedservice)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
