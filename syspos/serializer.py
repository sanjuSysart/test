from rest_framework import serializers
from.models import tbl_branch, tbl_customer, tbl_product, tbl_supplier, tbl_user, tbl_warehouse
from django.core.validators import EmailValidator
from rest_framework.response import Response

#REGADMIN
class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_user
        fields=(
            'us_name',
            'us_email',
            'us_password',
            'us_phone',
            'us_image'
        )




#customer serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_customer
        fields="__all__"
    # def create(self,request):

    #     data=self.request.data
    #     cus_name=data['cus_name']
    #     cus_email=data['cus_email']
    #     cus_mobile=data['cus_mobile']
    #     cus_address=data['cus_address']
    #     print(data['cus_loyalty']) 
    #     cusLoyalty=data['cus_loyalty']
    #     if tbl_customer.objects.filter(cus_email=cus_email,trash=False).exclude(cus_email="").exists():
    #             return Response({'error':"email is already exist"})
    #     elif tbl_customer.objects.filter(cus_mobile=cus_mobile,trash=False).exclude(cus_mobile="").exists():
    #         return Response({'error':"phone number is already exist"})
    #     else:
    #         data=tbl_customer(cus_name=cus_name,cus_email=cus_email,cus_mobile=cus_mobile,cus_address=cus_address,cus_loyalty=cusLoyalty)
    #         data.save()
    #         return Response("error:""saved")

   
#emploe serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_user
        fields="__all__"
#supplier serializer
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_supplier
        fields="__all__"
#branch serializer
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_branch
        fields="__all__"
#warehouse serializer
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_warehouse
        fields="__all__"
#productSeriualizer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=tbl_product
        fields="__all__"
        

       