from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True)
    phone_no = models.CharField(max_length=10)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username


class Customer(models.Model):
    user_id = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='user')
    company_name = models.CharField(max_length=50)
    account_balance = models.FloatField()
    dept = models.FloatField()

    # @property
    # def users(self):
    #     return self.customUser_set.all()


class Transfer(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_now=False)
    amount_sent_dollars = models.FloatField()
    payment_mode = models.CharField(max_length=20)
    details = models.TextField(null=True, blank=True)


class Payment(models.Model):
    date = models.DateField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=20)
    balance = models.FloatField()
    dept = models.FloatField()
    # amount_sent_dollars = models.FloatField()
    amount_sent_cedis = models.FloatField()
    transaction_type = models.CharField(max_length=20)


class Supplier(models.Model):
    company_name = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True)
    phone_no = models.CharField(max_length=15, null=True)


class SupplierPayment(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    Transfer_id = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    payment_id = models.OneToOneField(Payment, on_delete=models.CASCADE)
    goods_cost_dollars = models.FloatField()
    goods_cost_cedis = models.FloatField()
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    goods_desc = models.CharField(max_length=255)
    goods_weight = models.FloatField(blank=True, null=True)


class Consignment(models.Model):
    status = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class Freight(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='customer_id')
    payment_id = models.OneToOneField(
        Payment, on_delete=models.CASCADE, null=True, blank=True)
    consignment = models.ForeignKey(
        Consignment, on_delete=models.CASCADE, null=True, blank=True, related_name='consignment')
    date = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    total_weight = models.FloatField()
    note = models.CharField(default='Note', max_length=255,null=True, blank=True)
    goods_desc = models.CharField(max_length=255)
    picked_up = models.BooleanField(default=False, null=True, blank=True)
    isPaid = models.BooleanField(default=False, null=True, blank=True)

