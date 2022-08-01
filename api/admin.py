from django.contrib import admin
from .models import CustomUser,Customer,Transfer,Supplier,SupplierPayment,Payment,Freight, Consignment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Transfer)
admin.site.register(Supplier)
admin.site.register(SupplierPayment)
admin.site.register(Payment)
admin.site.register(Freight)
admin.site.register(Consignment)
