from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField
from phone_field import PhoneField

                    #MASTER              
#USERTYPES
class tbl_user_types(models.Model):
    id=models.AutoField(primary_key=True)
    create_date=models.DateTimeField(auto_now=True)
    type_name=models.CharField(max_length=250)
    trash=models.BooleanField(default=False)
    def __str__(self):
        return self.type_name
#USERS
class tbl_user(models.Model):
    us_id=models.AutoField(primary_key=True)
    us_name=models.CharField(max_length=300)
    us_email=models.EmailField(max_length=300)
    us_password=models.CharField(max_length=300)
    us_type=models.CharField(max_length=100)
    us_phone=PhoneField(null=True)
    us_address=models.TextField(null=True)
    us_image=models.ImageField(upload_to='images', blank=True, null=True)
    company=models.IntegerField(null=True)
    trash=models.BooleanField(default=False)

    USERNAME_FIELD = 'us_email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
            return self.us_name


#CUSTOMER TABLE
class tbl_customer(models.Model):
    cus_id=models.AutoField(primary_key=True)
    cus_join_date=models.DateTimeField(auto_now=True)
    cus_name=models.CharField(max_length=300,null=True)
    cus_email=models.EmailField(max_length=300,null=True)
    cus_mobile=PhoneField(null=True)
    cus_address=models.TextField(null=True)
    cus_loyalty=models.BooleanField(default=False)
    company=models.IntegerField(null=True)
    user=models.IntegerField(null=True)
    trash=models.BooleanField(default=False)
    def __str__(self):
            return self.cus_name


#SUPPLIER TABLE
class tbl_supplier(models.Model):
    sup_id=models.AutoField(primary_key=True)
    sup_company=models.CharField(max_length=200)
    sup_pin=models.CharField(max_length=200,null=True)
    sup_name=models.CharField(max_length=500,null=True)
    sup_country=models.CharField(max_length=200,null=True)
    sup_vat=models.CharField(max_length=300,null=True)
    sup_gst=models.CharField(max_length=200,null=True)
    sup_email=models.EmailField(max_length=300)
    sup_phone=PhoneField(blank=True,)
    sup_address=models.CharField(max_length=300,null=True)
    sup_city=models.CharField(max_length=200,null=True)
    sup_state=models.CharField(max_length=300,null=True)
    sup_description=models.CharField(max_length=600,null=True)
    sup_date=models.DateTimeField(auto_now_add=True)
    company=models.IntegerField(null=True)
    user=models.IntegerField(null=True)
    trash=models.BooleanField(default=False)
    


    def __str__(self):
        return self.sup_id

#BRANCH TABLE
class tbl_branch(models.Model):
    br_id=models.AutoField(primary_key=True)
    br_name=models.CharField(max_length=300)
    br_pin=models.CharField(max_length=100,null=True)
    br_country=models.CharField(max_length=200)
    br_vat=models.CharField(max_length=300,null=True)
    br_gst=models.CharField(max_length=200,null=True)
    br_email=models.EmailField(max_length=300)
    br_phone=models.BigIntegerField()
    br_address=models.CharField(max_length=300,null=True)
    br_city=models.CharField(max_length=200,null=True)
    br_state=models.CharField(max_length=200)
    br_description=models.TextField(max_length=600)
    br_date=models.DateTimeField(auto_now_add=True)
    company=models.IntegerField(null=True)
    user=models.IntegerField(null=True)
    trash=models.BooleanField(default=False)
#WAREHOUSE TABLE
class tbl_warehouse(models.Model):
    wr_id=models.AutoField(primary_key=True)
    wr_name=models.CharField(max_length=300,null=True)
    wr_address=models.TextField(null=True)
    wr_building=models.CharField(max_length=100,null=True)
    wr_description=models.TextField(null=True)
    wr_image=models.ImageField(upload_to='warehouses',blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)
    company=models.IntegerField(null=True)
    user=models.IntegerField(null=True)
    trash=models.BooleanField(default=True)

              # PRODUCT

# PRODUCT TABLE
class tbl_product(models.Model):   
    pr_id =models.AutoField(primary_key=True)
    pr_name=models.CharField(max_length=500)
    pr_name_arabic=models.CharField(max_length=300,null=True)
    # pr_barcode=models.CharField(max_length=200,null=True)
    # pr_brand=models.CharField(max_length=200,null=True)
    # pr_weight=models.CharField(max_length=100,null=True)
    # pr_category=models.CharField(max_length=200,null=True)
    # pr_sub_category=models.CharField(max_length=200,null=True)
    # pr_unit=models.CharField(max_length=100,null=True)    
    # pr_cost=models.CharField(max_length=200,null=True)
    # pr_price=models.CharField(max_length=100,null=True)
    # pr_tax=models.CharField(max_length=100,null=True)
    # pr_tax_method=models.CharField(default=False,max_length=100)
    # pr_alert_qty=models.CharField(max_length=100,null=True)
    # pr_qty=models.IntegerField()
    # pr_description=models.CharField(max_length=500,null=True)
    # pr_image=models.ImageField(upload_to='images', blank=True, null=True)
    # company=models.IntegerField(null=True)
    # user=models.IntegerField(null=True)
    # pr_date=models.DateTimeField(auto_now=True)
    # pr_made	=models.CharField(null=True,max_length=200)
    # pr_arti_code=models.CharField(max_length=300,null=True)
    # trash=models.BooleanField(default=False)


# # BRAND TABLE 
# class tbl_brand(models.Model):
#     br_id=models.AutoField(primary_key=True)
#     br_name=models.CharField(max_length=300)
#     br_date=models.DateTimeField(auto_now=True)
#     trash=models.BooleanField(default=False)
#     def __str__(self):
#         return self.br_name
# #CATEGORY TABLE
# class tbl_category(models.Model):
#     cat_id=models.AutoField(primary_key=True)
#     cat_name=models.CharField(max_length=300)
#     cat_date=models.DateTimeField(auto_now=True)
#     trash=models.BooleanField(default=False)
#     def __str__(self):
#         return self.cat_name
# #SUBCATEGORY TABLE
# class tbl_sub_category(models.Model):
#     sub_id=models.AutoField(primary_key=True,unique = True)
#     sub_name=models.CharField(max_length=300)
#     main_catogory=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
#     date=models.DateTimeField(auto_now=True)
#     trash=models.BooleanField(default=False)
#     def __str__(self):
#         return self.sub_name

