from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator



#!Product Collection Model
class Collection(models.Model):
    title=models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title 
    

#!Product Model
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    is_available=models.BooleanField(default=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='product')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,related_name='product')


    def __str__(self) -> str:
       return self.title

    
# !Product Image Model
class ProductImage(models.Model):
    image=models.ImageField(upload_to='product/image')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_image')


# !Product Review Model
class Review(models.Model):
    description=models.TextField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='review')
    time_stamp=models.DateTimeField(auto_now_add=True)


# !Review Reply Model
class Reply(models.Model):
    description=models.TextField()
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='reply')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reply')
    time_stamp=models.DateTimeField(auto_now_add=True)


# !Order Model
class Order(models.Model):
    PENDING="P"
    COMPLETE='C'
    FAILED='F'
    PAYMENT_STATUS=[
        (PENDING,"Pending"),
        (COMPLETE,"Complete"),
        (FAILED,"Failed")
    ]
    time_stamp=models.DateTimeField(auto_now=True)
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='order')


    def __str__(self) -> str:
        return f"{self.user} - {self.payment_status}"
    

    def cancel_order(self):
        """
        Cancel the order and set status to failed
        """
        self.payment_status=self.FAILED
        self.save()
        return "Order is canceled"




# !OrderItem Model
class OrderItem(models.Model):
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_item')


# !Cart Model
class Cart(models.Model):
    time_stamp=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')

    def __str__(self) -> str:
        return f"{self.user} cart"


# !CartItem Model
class CartItem(models.Model):
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_item')


    class Meta:
        unique_together = [['cart', 'product']]







    






   