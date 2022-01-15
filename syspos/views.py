from django.db.models import query
from django.shortcuts import render
from.models import tbl_branch, tbl_customer, tbl_product, tbl_supplier, tbl_user_types,tbl_user, tbl_warehouse
import datetime,jwt
from.serializer import BranchSerializer, CustomerSerializer,EmployeeSerializer, ProductSerializer, RegSerializer, SupplierSerializer, WarehouseSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status
from .middilewares import authentications
# Create your views here.
#Register Admin
class RegisterAdmin(APIView):
    def post(self,request):
        
        data=self.request.data
        print(data)
        
        us_name=data['us_name']
        us_email=data['us_email']
        us_password=data['us_password']
        us_phone=data['us_phone']
        us_image=data['us_image']
        
        if tbl_user.objects.filter(us_email=us_email,trash=False).exists():
            return Response({'error':"email is already exist"})

        # elif tbl_user.objects.filter(us_name=us_name,trash=False,us_type="Admin").exists():
        #     return Response({'error':"Admin name is already exist"})
        elif tbl_user.objects.filter(us_phone=us_phone,trash=False).exists():
            return Response({'error':"Phone number already exist"})
        elif len(us_password) < 6:
            return Response({'error':"password must be six Characters"})
        else:
            data=tbl_user(us_name=us_name,us_email=us_email, us_password= us_password,us_type="Admin",us_phone=us_phone,us_image=us_image)
            data.save()
            return Response({'Message': 'created'}) 
        
  
    


#LOGIN VIEW
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        email = request.data['us_email']
        password = request.data['us_password']
        user = tbl_user.objects.filter(us_email = email, us_password= password).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        payload = {
            'id': user.us_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        print(token)
       
        response = Response()
        response.set_cookie(key = 'jwt', value = token, httponly = True)
        response.data = {
            'jwt': token
        }
        return response


#Customer Adding
class CreateCustomer(APIView):
    serializer_class=CustomerSerializer
    def post(self,request):
        log_user=authentications(request)
        a=tbl_user.objects.get(us_id=log_user)     
        data=self.request.data
        cus_name=data['cus_name']
        cus_email=data['cus_email']
        cus_mobile=data['cus_mobile']
        cus_address=data['cus_address']
        # cusLoyalty=data['cus_loyalty']
       
        if a.us_type=="Admin":
            if tbl_customer.objects.filter(cus_email=cus_email,trash=False,company=log_user).exclude(cus_email="").exists():
                return Response({'error':"email is already exist"})
            elif tbl_customer.objects.filter(cus_mobile=cus_mobile,trash=False,company=log_user).exclude(cus_mobile="").exists():
                return Response({'error':"phone number is already exist"})
            else:
                data=tbl_customer(cus_name=cus_name,cus_email=cus_email,cus_mobile=cus_mobile,cus_address=cus_address,user=log_user,company=log_user)
                data.save()
                return Response("error:""saved")
        else:
            if tbl_customer.objects.filter(cus_email=cus_email,trash=False,company=a.log_user).exclude(cus_email="").exists():
                    return Response({'error':"email is already exist"})
            elif tbl_customer.objects.filter(cus_mobile=cus_mobile,trash=False,company=a.log_user).exclude(cus_mobile="").exists():
                return Response({'error':"phone number is already exist"})
            else:
                data=tbl_customer(cus_name=cus_name,cus_email=cus_email,cus_mobile=cus_mobile,cus_address=cus_address,user=log_user,company=a.company)
                data.save()
                return Response("error:""saved")
        
    def get(self,request,c_id=None):
        log_user=authentications(request)
        log_data=tbl_user.objects.get(us_id=log_user)
        print(log_user)
        if c_id:
            try:
                queryset=tbl_customer.objects.get(cus_id=c_id)
                
            except:
                return Response(status=status.HTTP_404_NOT_FOUND) 
            read_serializer = CustomerSerializer(queryset)
            
            trash=queryset.trash
            if trash==True:
                return Response({"Message":"user is already deleted"})
            print(trash)
            
            return Response(read_serializer.data)
        else:
            queryset=tbl_customer.objects.filter(trash=False,company=log_data.company)
            read_serializer = CustomerSerializer(queryset, many = True)
            return Response(read_serializer.data)
    def put(self,request,c_id=None):
        try:
            customer_dtl=tbl_customer.objects.get(cus_id=c_id,trash=False)
        except:
             return Response(status=status.HTTP_404_NOT_FOUND)
        
        if tbl_customer.objects.filter(cus_mobile=request.data['cus_mobile']).exclude(cus_id=c_id).exclude(cus_mobile="").exists():
           
            
            return Response({'error:'"phone number already exist"})
       
        update_serializer=CustomerSerializer(customer_dtl,data=request.data)
        if update_serializer.is_valid():
            customer_dtl_objects=update_serializer.save()
            read_serializer=CustomerSerializer(customer_dtl_objects)
            return Response(read_serializer.data, status = 200)
        return Response(update_serializer.errors, status = 400)
    def delete(self,request,c_id=None):
        try:
            customer_dtl=tbl_customer.objects.get(cus_id=c_id,trash=False)
        except:
            return Response("error:""EMPLOYEE DOES NOT EXIST")

        delete_serializer=CustomerSerializer(customer_dtl)
        tbl_customer.objects.filter(cus_id=c_id).update(trash=True)
        return Response("error:""DELETED")



                



# #EditDelete Customer
# class UpdateDeleteCustomer(RetrieveUpdateDestroyAPIView):
#     serializer_class=CustomerSerializer
#     queryset=tbl_customer.objects.filter(trash=False)
#     def delete(self, request, *args, **kwargs):
#         if tbl_customer.objects.get(cus_id=kwargs['pk'],trash=False):
#             tbl_customer.objects.filter(cus_id=kwargs['pk']).update(trash=True)
            
#             return Response({'Message': 'deleted'}) 
#         else:
#             return Response({'Message': 'no data found'})


#Employee Adding
class CreateEmployee(APIView):
    serializer_class=EmployeeSerializer
    
    def post(self,request):
        log_user=authentications(request)
        
        data=self.request.data
        us_name=data['us_name']
        us_email=data['us_email']
        us_password=data['us_password']
        us_type=data['us_type']
        us_phone=data['us_phone']
        us_image=data['us_image']

        a=tbl_user.objects.get(us_id=log_user)
        # print(a.us_type)
        if a.us_type=="Admin":        
            if tbl_user.objects.filter(us_email=us_email,trash=False,company=log_user).exists():
                return Response({'error':"email is already exist"})

            elif tbl_user.objects.filter(us_name=us_name,trash=False,company=log_user).exists():
                return Response({'error':"name is already exist"})
            elif tbl_user.objects.filter(us_phone=us_phone,trash=False,company=log_user).exists():
                return Response({'error':"Phone number already exist"})
            elif len(us_password) < 6:
                return Response({'error':"password must be six Characters"})
            else:
                data=tbl_user(us_name=us_name,us_email=us_email, us_password= us_password,us_type=us_type,us_phone=us_phone,us_image=us_image,company=log_user)
                data.save()
                return Response({'Message': 'created'}) 
        else:

            if tbl_user.objects.filter(us_email=us_email,trash=False,company=a.company).exists():
                    return Response({'error':"email is already exist"})

            elif tbl_user.objects.filter(company=a.company,us_name=us_name,trash=False).exists():
                return Response({'error':"name is already exist"})
            elif tbl_user.objects.filter(us_phone=us_phone,trash=False,company=a.company).exists():
                return Response({'error':"Phone number already exist"})
            elif len(us_password) < 6:
                return Response({'error':"password must be six Characters"})
            else:
                data=tbl_user(us_name=us_name,us_email=us_email, us_password= us_password,us_type=us_type,us_phone=us_phone,us_image=us_image,company=a.company)
                data.save()
                return Response({'Message': 'created'}) 
    # def get(self,request):
    #     queryset=tbl_user.objects.filter(trash=False)
    #     read_serializer = EmployeeSerializer(queryset, many = True)
    #     return Response(read_serializer.data)
   
    def get(self,request,u_id=None):
        log_user=authentications(request)
        a=tbl_user.objects.get(us_id=log_user)
        print()
        if u_id:
            try:
                queryset=tbl_user.objects.get(us_id=u_id)
                print(queryset)
                
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            read_serializer = EmployeeSerializer(queryset)
            
            trash=queryset.trash
            if trash==True:
                return Response({"Message":"user is already deleted"})
            print(trash)
            
            return Response(read_serializer.data)
        else:
            if a.us_type=="Admin":
                queryset=tbl_user.objects.filter(trash=False,company=a.company)
                read_serializer = EmployeeSerializer(queryset, many = True)
                return Response(read_serializer.data)
            else:
                print(a.us_type)
                queryset=tbl_user.objects.filter(trash=False,company=a.company).exclude(us_type=a.us_type)
                read_serializer = EmployeeSerializer(queryset, many = True)
                return Response(read_serializer.data)

#UPDATE EMPLOYEE
    def put(self,request,u_id=None):
        log_user=authentications(request)
        try:
            user_dtl=tbl_user.objects.get(us_id=u_id,trash=False)
        except:
             return Response(status=status.HTTP_404_NOT_FOUND)
        
        if len(request.data['us_password']) < 6:
            
            return Response({'error':"Password must be at least 6 characters"})
        elif  tbl_user.objects.filter(us_phone=request.data['us_phone']).exclude(us_id=u_id).exists():
            
            return Response({"error":"phone number is already exists"})
        update_serializer=EmployeeSerializer(user_dtl,data=request.data)
        if update_serializer.is_valid():
            user_dtl_objects=update_serializer.save()
            read_serializer=EmployeeSerializer(user_dtl_objects)
            return Response(read_serializer.data, status = 200)
        
        return Response(update_serializer.errors, status = 400)


#DELETE EMPLOYEE
    def delete(self,request,u_id=None):
        try:
            user_dtl=tbl_user.objects.get(us_id=u_id,trash=False)
        except:
            return Response("error:""EMPLOYEE DOES NOT EXIST")
        # delete_serializer=EmployeeSerializer(user_dtl)
        # trash=delete_serializer.data['trash']
        # if trash== True:
        #     return Response("error:""USER WAS DELETD")
        # else:
        #     tbl_user.objects.filter(us_id=u_id).update(trash=True)
        # print(trash)

        delete_serializer=EmployeeSerializer(user_dtl)
        tbl_user.objects.filter(us_id=u_id).update(trash=True)
        return Response("error:""DELETED")



#SUPPLIER ADDING
class createsupplier(APIView):
    #get supplier
    serializer_class=SupplierSerializer
    def get(self,request,sup_id=None):
        log_user=authentications(request)
        a=tbl_user.objects.get(us_id=log_user)
        if sup_id:
            
            try:
                queryset=tbl_supplier.objects.get(sup_id=sup_id)
            except:
                return  Response("message:""NOT FOUND")
            read_serializer = SupplierSerializer(queryset)
            
            trash=queryset.trash
            if trash==True:
                return Response({"Message":"supplier is already deleted"})
            return Response(read_serializer.data)
        else:
            if a.us_type=="Admin":
                queryset=tbl_supplier.objects.filter(trash=False,company=log_user,)
                read_serializer = SupplierSerializer(queryset, many = True)
                return Response(read_serializer.data)
            else:
                queryset=tbl_supplier.objects.filter(trash=False,company=a.company)
                read_serializer = SupplierSerializer(queryset, many = True)
                return Response(read_serializer.data)
    #POST SUPPLIER
    def post(self,request):
        log_user=authentications(request)       
        a=tbl_user.objects.get(us_id=log_user)
        company=a.company
        data=self.request.data  
        if a.us_type=="Admin":
            if tbl_supplier.objects.filter(sup_email=data['sup_email'],company=log_user).exclude(sup_email="").exists():
                return Response('error:''email is already exist')
            else:
                sup_data=SupplierSerializer(data=request.data)
                
                if sup_data.is_valid():
                    print(company)
                    sup_datas=sup_data.save()
                    sup_datas.company=log_user
                    sup_datas.user=log_user
                    sup_datas.save()               
                    return Response("message:""saved")
                else:
                    return Response("message:""chek fields")
        else:
            if tbl_supplier.objects.filter(sup_email=data['sup_email'],company=a.company).exclude(sup_email="").exists():
                return Response('error:''email is already exist')
            else:
                sup_data=SupplierSerializer(data=request.data)
                
                if sup_data.is_valid():
                    print(company)
                    sup_datas=sup_data.save()
                    sup_datas.company=company
                    sup_datas.user=log_user
                    sup_datas.save()               
                    return Response("message:""saved")
                else:
                    return Response("message:""chek fields")
    #EDIT SUPPLIER
    def put(self,request,sup_id=None):
        try:
            supplier_tbl=tbl_supplier.objects.get(sup_id=sup_id,trash=False)
        except:
             return Response(status=status.HTTP_404_NOT_FOUND)
        if tbl_supplier.objects.filter(sup_email=request.data['sup_email']).exclude(sup_id=sup_id).exists():
            return Response("message:""email is already exist")
        update_serializer=SupplierSerializer(supplier_tbl,data=request.data)
        if update_serializer.is_valid():
            supplier_dtl_objects=update_serializer.save()
            read_serializer=SupplierSerializer(supplier_dtl_objects)
            return Response(read_serializer.data, status = 200)
        
        return Response(update_serializer.errors, status = 400)
    #DELETE SUPPLIER
    def delete(self,request,sup_id= None):
        try:
            supplier_dtl=tbl_supplier.objects.filter(sup_id=sup_id,trash=False)
        except:
            return Response("message:""SUPPLIER DOESNOT EXIST")
        delete_serializer=SupplierSerializer(supplier_dtl)
        tbl_supplier.objects.filter(sup_id=sup_id).update(trash=True)
        return Response("error:""DELETED")  

    
class CreateBranch(APIView):
    serializer_class=BranchSerializer
    def get(self,request,br_id= None):
        log_user=authentications(request)       
        a=tbl_user.objects.get(us_id=log_user)
        company=a.company
        if br_id:
            try:
                queryset=tbl_branch.objects.get(br_id=br_id)
            except:
                return Response("message:""NOT FOUND")
            read_serializer=BranchSerializer(queryset)
            trash=queryset.trash
            if trash==True:
                return Response("message:""branch was deleted")
            return Response(read_serializer.data)
        else:
            if a.us_type=="Admin":
                queryset=tbl_branch.objects.filter(company=log_user,trash=False)
                read_serializer = BranchSerializer(queryset, many = True)
                return Response(read_serializer.data)
            else:
                queryset=tbl_branch.objects.filter(company=company,trash=False)
                read_serializer = BranchSerializer(queryset, many = True)
                return Response(read_serializer.data)

    def post(self,request):
        log_user=authentications(request)       
        a=tbl_user.objects.get(us_id=log_user)
        company=a.company
        if a.us_type=="Admin":
            data=self.request.data 
            if tbl_branch.objects.filter(br_email=data['br_email'],company=log_user).exclude(br_email="").exists():
                return Response("message:""EMAIL IS ALREADY EXISTS")
            else:
                branch_data=BranchSerializer(data=self.request.data)
                if branch_data.is_valid():

                    datas=branch_data.save()
                    datas.company=log_user
                    datas.user=log_user
                    datas.save()
                    return Response("saved")
                else:
                    return Response("message:""NOT VALIDATED DATA")
        else:
            data=self.request.data 
            if tbl_branch.objects.filter(br_email=data['br_email'],company=a.company).exclude(br_email="").exists():
                return Response("message:""EMAIL IS ALREADY EXISTS")
            else:
                branch_data=BranchSerializer(data=self.request.data)
                if branch_data.is_valid():

                    datas=branch_data.save()
                    datas.company=a.company
                    datas.user=log_user
                    datas.save()
                    return Response("saved")
                else:
                    return Response("message:""NOT VALIDATED DATA")
            
    def put(self,request,br_id=None):
        log_user=authentications(request)
        a=tbl_user.objects.get(us_id=log_user)
        try:
            branch_tbl=tbl_branch.objects.get(br_id=br_id,trash=False)
        except:
             return Response(status=status.HTTP_404_NOT_FOUND)
        if a.us_type=="Admin":
            if tbl_branch.objects.filter(br_email=request.data['br_email'],copmany=log_user).exclude(br_id=br_id).exists():
                return Response("message:""email is already exist")
            update_serializer=  BranchSerializer(branch_tbl,data=request.data)
            if update_serializer.is_valid():
                branch_dtl_objects=update_serializer.save()
                read_serializer=BranchSerializer(branch_dtl_objects)
                return Response(read_serializer.data, status = 200)
            
            return Response(update_serializer.errors, status = 400)
        else:
            if tbl_branch.objects.filter(br_email=request.data['br_email'],company=a.company).exclude(br_id=br_id).exists():
                return Response("message:""email is already exist")
            update_serializer=  BranchSerializer(branch_tbl,data=request.data)
            if update_serializer.is_valid():
                branch_dtl_objects=update_serializer.save()
                read_serializer=BranchSerializer(branch_dtl_objects)
                return Response(read_serializer.data, status = 200)
            
            return Response(update_serializer.errors, status = 400)

        
    def delete(self,request,br_id):
        try:
            branch_dtl=tbl_branch.objects.filter(br_id=br_id,trash=False)
        except:
            return Response("message:""SUPPLIER DOESNOT EXIST")
        delete_serializer=SupplierSerializer(branch_dtl)
        tbl_branch.objects.filter(br_id=br_id).update(trash=True)
        return Response("error:""DELETED")




#WAREHOUSE
class createwarehouse(APIView):
    serializer_class=   WarehouseSerializer
   
    def get(self,request,wr_id=None):
        log_user=authentications(request)
        a=tbl_user.objects.get(us_id=log_user)
        if wr_id:
            try:
                queryset=tbl_warehouse.objects.get(wr_id=wr_id,company=a.company)
            except:
                return Response("message:""NOT FOUND")
            read_serializer=WarehouseSerializer(queryset)             
            trash=queryset.trash
            if trash==True:
                return Response("error:"" warehouse already deleted")
            return Response(read_serializer.data)
        else:
            if a.us_type=="Admin":
                queryset=tbl_warehouse.objects.filter(trash=False,company=log_user)
                read_serializer = WarehouseSerializer(queryset, many = True)
                return Response(read_serializer.data)
            else:
                queryset=tbl_warehouse.objects.filter(trash=False,company=a.company)
                read_serializer = WarehouseSerializer(queryset, many = True)
                return Response(read_serializer.data)
            
    def post(self,request):
        log_user=authentications(request)       
        a=tbl_user.objects.get(us_id=log_user)
        company=a.company
        data=self.request.data
        if a.us_type=="Admin":
            if tbl_warehouse.objects.filter(wr_name=data['wr_name'],trash=False,company=log_user).exists():
                return Response("message:""NAME IS ALREADY EXIST")
            else:
                ware_data=WarehouseSerializer(data=request.data)
                if ware_data.is_valid():
                    datas=ware_data.save()
                    datas.company=log_user
                    datas.user=log_user
                    datas.save()
                    return Response("saved")
                else:
                    return Response("check validations")
        else:
            if tbl_warehouse.objects.filter(wr_name=data['wr_name'],trash=False,company=company).exists():
                return Response("message:""NAME IS ALREADY EXIST")
            else:
                ware_data=WarehouseSerializer(data=request.data)
                if ware_data.is_valid():
                    datas=ware_data.save()
                    datas.company=company
                    datas.user=log_user
                    datas.save()
                    return Response("saved")
                else:
                    return Response("check validations")
     
                   
    def put(self,request,wr_id=None):
        print(wr_id)
        try:
            wr_data=tbl_warehouse.objects.filter(wr_id=wr_id,trash=False)
        except:
            return Response("MESSAGE:NOT FOUND")
        if tbl_warehouse.objects.filter(wr_name=request.data['wr_name']).exclude(wr_id=wr_id).exists():
            return Response("message:name is already exists")
        else:
            update_serailizer=WarehouseSerializer(wr_data,data=request.data)
            if update_serailizer.is_valid():
                ware_data=update_serailizer.save()
                read_serializer=WarehouseSerializer(ware_data)
                return Response(read_serializer.data, status = 200)
        
        return Response(update_serailizer.errors, status = 400)

    def delete(self,request,wr_id):
        try:
            warehouse_dtl=tbl_warehouse.objects.filter(wr_id=wr_id,trash=False)
        except:
            return Response("message:""SUPPLIER DOESNOT EXIST")
        delete_serializer=WarehouseSerializer(warehouse_dtl)
        tbl_warehouse.objects.filter(wr_id=wr_id).update(trash=True)
        return Response("error:""DELETED")




#PRODUCT ADDING
            
# class CreateProduct(APIView):
#     serializer_class=ProductSerializer
#     def post(self,request):
#         data=self.request.data
#         print(data)


           




        

       
         


        
        
    


        



        

        
        
        
        
        
        



   



