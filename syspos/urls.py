
from django.urls import path
from.views import  CreateProduct, RegisterAdmin,CreateBranch, LoginView,CreateCustomer,CreateEmployee,createsupplier, createwarehouse
urlpatterns = [
    #Reg user
    path('reg',RegisterAdmin.as_view()),
    #log in page
    path('log',LoginView.as_view()),
    #create a customer
    path('add_customer',CreateCustomer.as_view()),
    #editupdate customer
    path('add_customer/<int:c_id>',CreateCustomer.as_view()),
    # path('editupdate_customer/<int:pk>',UpdateDeleteCustomer.as_view()),
    #create employee
    path('add_employee',CreateEmployee.as_view()),
    #GET,UPDATE,DELETE emloyee
    path('add_employee/<int:u_id>',CreateEmployee.as_view()),
    #supplier
    path('add_supplier',createsupplier.as_view()),
    #GET,UPDATE,DELETE SUPPLIER
    path('add_supplier/<int:sup_id>',createsupplier.as_view()),
    #ADD BRANCH
    path('add_branch',CreateBranch.as_view()),
     #GET,UPDATE,DELETE BRANCH
    path('add_branch/<int:br_id>',CreateBranch.as_view()),
    #WAREHOUSE
    path('add_warehouse',createwarehouse.as_view()),
    #GET,UPDATE,DELETE WAREHOUSE
    path('add_warehouse/<int:wr_id>',createwarehouse.as_view()),
            #PRODUCT
    #ADD PRODUCT
    path('add_product',CreateProduct.as_view())


    
]
