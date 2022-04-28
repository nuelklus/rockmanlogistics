from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.db.models import Sum


# Create your views here.

class CustomUserListView(APIView):

    def get(self, request):
        customUsers = CustomUser.objects.all()
        serializer = CustomUserSerializers(customUsers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailsViewByUsername(APIView):

    def get(self, request, username):
        # customer = CustomUser.objects.get(username=username)
        customerInfo = Customer.objects.get(user_id__username=username)
        serializer = CustomerUpdateSerializers(customerInfo, many=False)
        return Response(serializer.data)

    def put(self, request, username):
        Customer_objupdate = Customer.objects.get(user_id__username=username)
        data = request.data
        # print(data)
        # exit()
        # print(Customer_objupdate.user_id.id)

        CustomUser_obj = CustomUser.objects.get(username=username)
        CustomUser_obj.first_name = data["user_id"]["first_name"]
        CustomUser_obj.last_name = data["user_id"]["last_name"]
        CustomUser_obj.email = data["user_id"]["email"]
        CustomUser_obj.phone_no = data["user_id"]["phone_no"]
        CustomUser_obj.username = data["user_id"]["username"]
        CustomUser_obj.password = data["user_id"]["password"]
        CustomUser_obj.save()
        # print(CustomUser_obj.first_name)

        Customer_objupdate.user_id = CustomUser_obj
        Customer_objupdate.company_name = data["company_name"]

        Customer_objupdate.save()

        serializer = CustomerUpdateSerializers(Customer_objupdate, many=False)
        return Response(serializer.data)


class CustomerListView(APIView):

    def get(self, request):
        customers = Customer.objects.order_by('-id')
        serializer = CustomerSerializers(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailsView(APIView):

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializers(customer, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        Customer_obj = Customer.objects.get(id=pk)
        data = request.data
        print(data)
        # exit()
        # print(Customer_obj.user_id.id)

        # Customer_obj.user_id = CustomUser.objects.get(id=3)
        # print(Customer_obj.user_id.id)

        # exit()
        Customer_obj.user_id.username = data["username"]
        Customer_obj.user_id.phone_no = data["phone_no"]
        Customer_obj.company_name = data["company_name"]
        Customer_obj.account_balance = data["account_balance"]
        # Customer_obj.dept = data["dept"]
        # print(Customer_obj)
        Customer_obj.save()

        serializer = CustomerSerializers(Customer_obj)
        return Response(serializer.data)


class CustomerTranferView(APIView):

    def get(self, request):
        tranfers = Transfer.objects.order_by('-id')
        serializer = TransferSerializers(tranfers, many=True)
        return Response(serializer.data)

    def post(self, request):
        transferData = request.data
        print(transferData)
        # exit()

        # get cutomer id with the username from the frontend form
        customer = CustomUser.objects.filter(
            username__iexact=transferData["username"]).get()

        print(customer.id)

        # money transferred by a customer must be added to the customers balance in the customer table
        customerByCustomUserId = Customer.objects.filter(
            user_id__id=customer.id).get()
        selectedCustomer = Customer.objects.get(id=customerByCustomUserId.id)
        selectedCustomer.account_balance += float(
            transferData["amount_sent_dollars"])
        # print(type(transferData["amount_sent_dollars"]))
        # exit()
        # selectedCustomer.account_balance += 10.2
        print(customerByCustomUserId.id)
        selectedCustomer.save()

        # exit()
        # new_transfer = Transfer.objects.create(customer_id=Customer.objects.get(id=customer.id),
        new_transfer = Transfer.objects.create(customer_id=Customer.objects.get(id=customerByCustomUserId.id),
                                               amount_sent_dollars=transferData[
                                                   "amount_sent_dollars"], amount_sent_cedis=transferData["amount_sent_cedis"],
                                               balance=transferData["balance"], payment_mode=transferData["payment_mode"])
        new_transfer.save()
        serializer = TransferSerializers(new_transfer)
        return Response(serializer.data)


class CustomerTranferDetailsView(APIView):

    def get(self, request, pk):
        tranfers = Transfer.objects.get(id=pk)
        serializer = TransferSerializers(tranfers, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        Transfer_object = Transfer.objects.get(id=pk)
        data = request.data
        # print(Transfer_object.date)

        print(Transfer_object.customer_id.id)

        # Transfer_object.customer_id = Customer.objects.get(id=3)
        # print(Transfer_object.customer_id.id)

        # exit()
        # Transfer_object.date = data["date"]
        Transfer_object.amount_sent_dollars = data["amount_sent_dollars"]
        Transfer_object.amount_sent_cedis = data["amount_sent_cedis"]
        Transfer_object.balance = data["balance"]
        Transfer_object.payment_mode = data["payment_mode"]

        Transfer_object.save()

        serializer = TransferSerializers(Transfer_object)
        return Response(serializer.data)


class SupplierView(APIView):

    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializers(suppliers, many=True)
        return Response(serializer.data)


class SupplierPaymentView(APIView):

    def get(self, request):
        supplierpayments = SupplierPayment.objects.order_by('-id')
        serializer = SupplierPaymentSerializers(supplierpayments, many=True)
        return Response(serializer.data)

    def post(self, request):
        postdata = request.data
        print(postdata)
        # exit()
        # get cutomer id with the username from the frontend form
        customer = CustomUser.objects.filter(
            username__iexact=postdata["username"]).get()
        # print(customer.id)

        # money paid by a customer must be subtracted from the customers balance in the customer model
        customerByCustomUserId = Customer.objects.filter(
            user_id__id=customer.id).get()
        selectedCustomer = Customer.objects.get(id=customerByCustomUserId.id)

        selectedCustomer.account_balance -= postdata["amount_paid"]
        # selectedCustomer.account_balance -= 4
        # print(type(postdata["amount_paid"]))
        # exit()
        selectedCustomer.save()

        # exit()
        new_payment = Payment.objects.create(
            # date=postdata["date"],
            status=postdata["payment_id"]["status"], payment_mode=postdata["payment_id"]["payment_mode"],
            balance=postdata["payment_id"]["balance"], dept=postdata["payment_id"]["dept"],
            # amount_sent_dollars=postdata["payment_id"]["amount_sent_dollars"],
            amount_sent_cedis=postdata["payment_id"]["amount_sent_cedis"], transaction_type=postdata["payment_id"]["transaction_type"])

        # new_payment.save()

        # get cutomer id with the supplier name from the frontend form
        supplier = Supplier.objects.get(
            company_name__iexact=postdata["supplier"])

        print(supplier.id)
        # exit()
        new_supplierpayments = SupplierPayment.objects.create(
            # made transaction id = 1 because its not necessary to show in supplier payment transactions cause tracking number transfer for one payment is alot of work
            customer_id=Customer.objects.get(id=customerByCustomUserId.id),
            Transfer_id=Transfer.objects.get(id=1),
            payment_id=new_payment,
            goods_cost_dollars=postdata["goods_cost_dollars"],
            goods_cost_cedis=postdata["goods_cost_cedis"],
            goods_desc=postdata["goods_desc"], supplier_id=Supplier.objects.get(id=supplier.id))

        new_supplierpayments.save()

        serializer = SupplierPaymentSerializers(new_supplierpayments)
        return Response(serializer.data)


class SupplierPaymentDetailsView(APIView):

    def get(self, request, pk):
        supplierpayment = SupplierPayment.objects.get(id=pk)
        serializer = SupplierPaymentSerializers(supplierpayment, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        SupplierPayment_object = SupplierPayment.objects.get(id=pk)
        data = request.data
        print(SupplierPayment_object.Transfer_id.balance)

        SupplierPayment_object.goods_cost_dollars = data["goods_cost_dollars"]
        SupplierPayment_object.goods_cost_cedis = data["goods_cost_cedis"]
        SupplierPayment_object.goods_desc = data["goods_desc"]
        # SupplierPayment_object.balance = data["balance"]

        SupplierPayment_object.save()

        serializer = SupplierPaymentSerializers(SupplierPayment_object)
        return Response(serializer.data)


class TranferSupplierPaymentSumView(APIView):

    def get(self, request, date):
        transferSum = Transfer.objects.filter(date=date).aggregate(
            amount_sent_dollars=Sum('amount_sent_dollars'))
        tranferSumsSerializedObj = TransferSumSerializers(
            transferSum, many=False)
        supplierPaymentSum = SupplierPayment.objects.filter(
            payment_id__date=date).aggregate(goods_cost_dollars=Sum('goods_cost_dollars'))
        supplierPaymentSumSumsSerializedObj = SupplierPaymentSumSerializers(
            supplierPaymentSum, many=False)
        result = {**supplierPaymentSumSumsSerializedObj.data,
                  **tranferSumsSerializedObj.data}
        return Response(result)

class CustomerTranferByDateView(APIView):

    def get(self, request, date):
        transfers = Transfer.objects.filter(date=date)
        # print(transfers)
        # exit()
        tranferSerializedObj = TransferSerializers(
            transfers, many=True)
        return Response(tranferSerializedObj.data)

class CustomersWithNegativeBalanceView(APIView):

    def get(self, request):
        customers = Customer.objects.filter(account_balance__lt=0)
        serializer = CustomerSerializers(customers, many=True)
        return Response(serializer.data)

class CustomersWithPositiveBalanceView(APIView):

    def get(self, request):
        customers = Customer.objects.filter(account_balance__gt=0).order_by('-id')
        serializer = CustomerSerializers(customers, many=True)
        return Response(serializer.data)

