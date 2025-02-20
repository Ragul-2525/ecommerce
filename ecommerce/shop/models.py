from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(requset,filename):
  now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
  new_filename="%s%s"%(now_time,filename)
  return os.path.join('uploads/',new_filename)
 
class Catagory(models.Model):
  name=models.CharField(max_length=150,null=False,blank=False)
  image=models.ImageField(upload_to=getFileName,null=True,blank=True)
  description=models.TextField(max_length=500,null=False,blank=False)
  status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
  created_at=models.DateTimeField(auto_now_add=True)
 
  def __str__(self) :
    return self.name
 
class Product(models.Model):
  catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
  name=models.CharField(max_length=150,null=False,blank=False)
  vendor=models.CharField(max_length=150,null=False,blank=False)
  product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
  quantity=models.IntegerField(null=False,blank=False)
  original_price=models.FloatField(null=False,blank=False)
  selling_price=models.FloatField(null=False,blank=False)
  description=models.TextField(max_length=500,null=False,blank=False)
  status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
  trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
  created_at=models.DateTimeField(auto_now_add=True)
 
  def __str__(self) :
    return self.name
  
class Cart(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty = models.IntegerField(null=False,blank=False)
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price

class Favourite(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty = models.IntegerField(null=False,blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  
  def __str__(self):
        return f'{self.product.name} - {self.user.username}'

  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price

class Favourite(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

def save(self, *args, **kwargs):
        # Calculate total cost whenever the Cart object is saved
        self.total_cost = self.product.selling_price * self.product_qty
        super(Cart, self).save(*args, **kwargs)
  
  
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=255, blank=True, null=True)  # optional
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # for storing total order amount
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name} - {self.id}"