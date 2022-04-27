from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('customUserlist/', CustomUserListView.as_view()),
    path('customerdetailsByUsername/<str:username>/',
         CustomerDetailsViewByUsername.as_view()),
    path('customerlist/', CustomerListView.as_view()),
    path('customerdetails/<str:pk>/', CustomerDetailsView.as_view()),
    path('customertranfer/', CustomerTranferView.as_view()),
    path('customertranferdetails/<str:pk>/',
         CustomerTranferDetailsView.as_view()),
    path('supplierslist/', SupplierView.as_view()),
    path('supplierpayment/', SupplierPaymentView.as_view()),
    path('supplierpaymentdetails/<str:pk>/',
         SupplierPaymentDetailsView.as_view()),
    path('tranfersupplierpaymentsum/<str:date>/',
         TranferSupplierPaymentSumView.as_view()),
    path('customertranferbydate/<str:date>/',
         CustomerTranferByDateView.as_view()),
    path('customerswithnegativebalance/',
         CustomersWithNegativeBalanceView.as_view()),
]
