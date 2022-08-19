from django.urls import path
# from . import views
from .views import *
from knox import views as knox_views
from .views import LoginAPI


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
    path('customerswithpositivebalance/',
         CustomersWithPositiveBalanceView.as_view()),
    path('customerTransfersView/<str:username>/',
         CustomerTransfersView.as_view()),
    path('customerSupplyPaymentView/<str:username>/',
         CustomerSupplyPaymentView.as_view()),
    path('customerFreightView/',
         FreightSerializersView.as_view()),
    path('customerfreightdetails/<str:pk>/',
         FreightDetailsView.as_view()),
    path('consignmentlist/',
         ConsignmentListView.as_view()),
    path('consignmentlistopenandinturkey/',
         ConsignmentListOpenAndInTurkeyView.as_view()),
    path('consignmentlistopenandinaccra/',
         ConsignmentListOpenAndInAccraView.as_view()),
    path('consignmentUpdate/<str:pk>/',
         ConsignmentUpdateView.as_view()),
    path('register/',
         RegisterUserView.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('staffuser/', StaffUserAPI.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]
