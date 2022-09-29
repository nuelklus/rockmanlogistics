from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from django.db.models import Sum
import requests
import ssl
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
from datetime import datetime
from knox.models import AuthToken
from datetime import datetime
# from rest_framework import generics


# def Invoice(amountPaid, customerName, paymentMode, paymentDate, transferDetails, Supplier, transactionType):
#     class PDF(FPDF):

#         # PDF HEADER
#         def header(self):
#             transaction_type = '            ' + transactionType + ' Invoice'
#             self.image('rockman-logo.png', 10, 2, 20)
#             self.set_text_color(3, 82, 140)
#             self.set_font('helvetica', 'B', 14)
#             self.cell(0, 5, transaction_type, ln=True, align='R')
#             self.ln(10)

#         # PDF HEADER

#         def footer(self):
#             Date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             self.set_y(-10)
#             self.cell(0, -6, '', 'B', 1, 'C')

#             self.set_font('helvetica', '', size=6)
#             self.cell(35, 5, Date_created, align='L')
#             self.set_text_color(176, 84, 14)
#             self.cell(70, 5, 'Rockman Logistics : Freight shipping services',
#                       ln=True, align='L')

#             # pdf.cell(80, 5, 'Rockman Logistics : Freight shipping services', ln=True, align='R')

#     AmountPaidInDallars = '$' + amountPaid
#     CustomerName = customerName
#     PaymentMode = paymentMode
#     PaymentDate = paymentDate
#     TransferDetails = transferDetails

#     pdf = PDF('P', 'mm', (105, 150))
#     pdf.add_page()
#     pdf.set_text_color(74, 74, 75)
#     pdf.set_font('helvetica', '', size=8)
#     pdf.cell(0, -6, '', 'B', 1, 'C')
#     pdf.set_font('helvetica', '', size=6)
#     # pdf.cell(35, 5, 'Date_created', align='L')
#     pdf.set_text_color(176, 84, 14)
#     pdf.cell(
#         0, 5, 'Phone : +233202729851/+233202729851     Email : nuelklus@gmail.com',  align='C')
#     pdf.set_xy(10, 30)
#     pdf.set_font('helvetica', '', size=8)
#     pdf.set_text_color(74, 74, 75)

#     # Customer
#     pdf.cell(35, 7, 'Customer', align='L')
#     pdf.cell(10, 7, ':', align='C')
#     pdf.cell(35, 7, CustomerName, ln=True, align='L')
#     # Total Amount Paid
#     pdf.cell(35, 7, 'Amount', align='L')
#     pdf.cell(10, 7, ':', align='C')
#     pdf.cell(35, 7, AmountPaidInDallars, ln=True, align='L')
#     # payment Mode
#     pdf.cell(35, 7, 'Payment Mode', align='L')
#     pdf.cell(10, 7, ':', align='C')
#     pdf.cell(35, 7, PaymentMode, ln=True, align='L')
#     # payment Date
#     pdf.cell(35, 7, 'Payment Date', align='L')
#     pdf.cell(10, 7, ':', align='C')
#     pdf.cell(35, 7, PaymentDate, ln=True, align='L')

#     if(transactionType == 'Transfer'):
#         # Transfer Details
#         pdf.cell(35, 7, 'Transfer Details', ln=True, align='L')
#         pdf.set_font('helvetica', '', size=7)
#         pdf.cell(0, 2, '', ln=True, align='C')
#         pdf.multi_cell(0, 5, TransferDetails, border=1, ln=True, align='L')
#     else:
#         # Supplier info
#         pdf.cell(35, 7, 'Supplier', align='L')
#         pdf.cell(10, 7, ':', align='C')
#         pdf.cell(35, 7, Supplier, ln=True, align='L')

#     # Messages to customer or information and more
#     pdf.cell(0, 25, '', ln=True, align='C')

#     pdf.set_font('helvetica', '', size=12)
#     pdf.cell(0, 5, 'Thank you !!!', ln=True, align='C')
#     if (transactionType == 'Transfer'):
#         pdf.output("Transfer_Invoice.pdf")
#     else:
#         pdf.output("Supplier_Payment_Invoice.pdf")


def SendSMS(content, customerPhone):
    # send SMS using hubtel
    payload = {"clientsecret": "fdkfusvx", "clientid": "zresivmf",
               "from": "RockmanLOG", "to": customerPhone, "content": content}
    r = requests.get(
        "https://smsc.hubtel.com/v1/messages/send", payload)
    print(r)


# def SendEmail(emailReceiver, transactionType):
#     # how to send emails using gmail stmp service
#     email_sender = 'nuelklus@gmail.com'
#     email_password = 'vuugipsunycollrs'
#     email_receiver = emailReceiver

#     msg = EmailMessage()
#     msg['Subject'] = 'Transaction receipt from Rockman Logistics'
#     msg['From'] = 'rockman@gmail.com'
#     msg['To'] = email_receiver
#     msg.set_content('Tranfer receipt from Rockman')

#     # Create a secure SSL context
#     # context = ssl.create_default_context()
#     if(transactionType == 'Transfer'):
#         with open('Transfer_Invoice.pdf', 'rb') as f:
#             file_data = f.read()
#             file_name = f.name
#     else:
#         with open('Supplier_Payment_Invoice.pdf', 'rb') as f:
#             file_data = f.read()
#             file_name = f.name
#     msg.add_attachment(file_data, maintype='application',
#                        subtype='octet-stream', filename=file_name)

#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.ehlo()

#         smtp.login(email_sender, email_password)
#         smtp.send_message(msg)


class CustomUserListView(APIView):

    def get(self, request):
        customUsers = CustomUser.objects.all()

        # SendSMS('test content', '233557911415')
        # SendEmail()
        serializer = CustomUserSerializers(customUsers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = RegisterSerializers(user)

        return Response({
            "user": serializer.data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class StaffUserAPI(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = CustomUserSerializers

    def get_object(self):
        return self.request.user


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
        # print("request.data.username", request.data['user_id']['username'])
        getUsername = CustomUser.objects.filter(
            username=request.data['user_id']['username'])
        if(getUsername.exists()):
            return Response('user already exist')

        else:
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

        # get cutomer id with the username from the frontend form
        customer = CustomUser.objects.filter(
            username__iexact=transferData["username"]).get()

        # print(customer.id)

        # money transferred by a customer must be added to the customers balance in the customer table
        customerByCustomUserId = Customer.objects.filter(
            user_id__id=customer.id).get()
        selectedCustomer = Customer.objects.get(id=customerByCustomUserId.id)
        selectedCustomer.account_balance += float(
            transferData["amount_sent_dollars"])
        selectedCustomer.save()

        new_transfer = Transfer.objects.create(customer_id=Customer.objects.get(id=customerByCustomUserId.id), amount_sent_dollars=transferData[
            "amount_sent_dollars"], payment_mode=transferData["payment_mode"], details=transferData["details"])

        new_transfer.save()
        new_transfer_saved = new_transfer.id

        if new_transfer_saved:
            customerName = new_transfer.customer_id.user_id.first_name + \
                ' ' + new_transfer.customer_id.user_id.last_name
            customerBalance = new_transfer.customer_id.account_balance
            customerPhone = new_transfer.customer_id.user_id.phone_no
            customerPhoneInternationalStandard = '233' + customerPhone
            paymentInDollars = new_transfer.amount_sent_dollars
            PaymentMode = new_transfer.payment_mode
            PaymentDate = new_transfer.date
            tranferDetails = new_transfer.details
            customerEmail = 'info@rockmanlogisticsgh.com'
            # print(customerBalance)
            # exit()

            content = 'Dear ' + customerName + ', ' + 'Receipt of transfer payment of ' + '$' + \
                str(paymentInDollars)+ '.00' + ' on ' + str(PaymentDate) + \
                ' with current balance of' + '$ ' + str(format(customerBalance, '.2f')) + '.'
            # send SMS to customer
            SendSMS(content, customerPhoneInternationalStandard)
            d = dict()

            # generate customer pdf file, Example : Tranfer_Invoice.pdf
            # Invoice(str(paymentInDollars), customerName,
            #         PaymentMode, str(PaymentDate),  tranferDetails, 'supplier', 'Transfer')

            # send Email to customer
            # SendEmail(customerEmail, 'Transfer')
            serializer = TransferSerializers(new_transfer)
            d['data'] = serializer.data
            return Response(d)
        else:
            return Response('Transfer object failed to save')


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

    def post(self, request):
        serializer = SupplierSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        selectedCustomer.save()

        new_payment = Payment.objects.create(
            # date=postdata["date"],
            status=postdata["payment_id"]["status"], payment_mode=postdata["payment_id"]["payment_mode"],
            balance=postdata["payment_id"]["balance"], dept=postdata["payment_id"]["dept"],
            # amount_sent_dollars=postdata["payment_id"]["amount_sent_dollars"],
            amount_sent_cedis=postdata["payment_id"]["amount_sent_cedis"], transaction_type=postdata["payment_id"]["transaction_type"])

        # new_payment.save()

        # get cutomer id with the supplier name from the frontend form
        # supplierID = 0
        try:
            supplier = Supplier.objects.get(
                company_name__iexact=postdata["supplier"])
        except Exception:
            print('text')
            new_supplier = Supplier.objects.create(
                company_name=postdata["supplier"],
                contact_name='Rockman Logistics',
                address='Ghana-Accra',
                phone_no='0244400000'
            )
            new_supplier.save()
            supplier = Supplier.objects.get(
                company_name__iexact=postdata["supplier"])
            # print(supplier.id)

        # get consignment with status open and city Turkey
        consignment = Consignment.objects.filter(
            status='open', city='Turkey')
        d = dict()
        # check if consignment is open for shipment
        if consignment.exists():
            # select Freight with consignment status open and city Turkey and the customer already have an entry in that consignment then update customers entry else make a new entry
            getFreight = Freight.objects.filter(customer_id__id=customerByCustomUserId.id,
                                                consignment_id__status='open', consignment_id__city='Turkey')

            if getFreight.exists():
                # get editable object to object content with ease
                getEditableFreightObject = Freight.objects.filter(customer_id__id=customerByCustomUserId.id,
                                                                  consignment_id__status='open', consignment_id__city='Turkey').get()
                # update freight total weight
                getEditableFreightObject.total_weight += float(
                    postdata["goods_weight"])

                getEditablePaymentObject = Payment.objects.get(
                    id=getEditableFreightObject.payment_id.id)
                print(getEditablePaymentObject.amount_sent_cedis)
                getEditablePaymentObject.amount_sent_cedis = (
                    getEditableFreightObject.total_weight) * 8
                # print(getEditableFreightObject.payment_id.amount_sent_cedis)
                getEditablePaymentObject.save()
                # exit()

                getEditableFreightObject.save()
            else:
                getEditableConsignmentObject = Consignment.objects.filter(
                    status='open', city='Turkey').get()

                new_paymentForFreight = Payment.objects.create(
                    # date=postdata["date"],
                    status=postdata["payment_id"]["status"], payment_mode=postdata["payment_id"]["payment_mode"],
                    balance=postdata["payment_id"]["balance"], dept=postdata["payment_id"]["dept"],
                    # amount_sent_dollars=postdata["payment_id"]["amount_sent_dollars"],
                    amount_sent_cedis=postdata["goods_weight"]*8, transaction_type="freight")

                new_freight = Freight.objects.create(
                    customer_id=Customer.objects.get(
                        id=customerByCustomUserId.id),
                    consignment_id=getEditableConsignmentObject.id,
                    payment_id=new_paymentForFreight,
                    total_weight=postdata["goods_weight"],
                    # amount_sent_dollars=postdata["amount_sent_cedis"],
                    goods_desc=postdata["goods_desc"])

                print(new_freight)
                new_freight.save()

            new_supplierpayments = SupplierPayment.objects.create(
                # made transaction id = 1 because its not necessary to show in supplier payment transactions cause tracking number transfer for one payment is alot of work
                customer_id=Customer.objects.get(
                    id=customerByCustomUserId.id),
                Transfer_id=Transfer.objects.get(id=1),
                payment_id=new_payment,
                goods_cost_dollars=postdata["goods_cost_dollars"],
                goods_cost_cedis=postdata["goods_cost_cedis"],
                goods_desc=postdata["goods_desc"],
                supplier_id=Supplier.objects.get(id=supplier.id),
                goods_weight=postdata["goods_weight"])

            new_supplierpayments.save()
            new_supplierpayment_saved = new_supplierpayments.id
            #
            if new_supplierpayment_saved:
                customerName = new_supplierpayments.customer_id.user_id.first_name + \
                    ' ' + new_supplierpayments.customer_id.user_id.last_name
                customerBalance = new_supplierpayments.customer_id.account_balance
                customerPhone = new_supplierpayments.customer_id.user_id.phone_no
                customerPhoneInternationalStandard = '233' + customerPhone
                paymentInDollars = new_supplierpayments.payment_id.amount_sent_cedis
                PaymentMode = new_supplierpayments.payment_id.payment_mode
                PaymentDate = new_supplierpayments.payment_id.date
                supplierCompany = new_supplierpayments.supplier_id.company_name
                customerEmail = 'info@rockmanlogisticsgh.com'

                content = 'Dear ' + customerName + ', ' + 'Receipt of supply payment of '  + '$' + \
                    str(paymentInDollars) + '.00' + ' on ' + str(PaymentDate) + \
                    ' to  ' + supplierCompany + ' with current balance of $ ' + str(format(customerBalance, '.2f')) + '.'

                # send SMS to customer
                SendSMS(content, customerPhoneInternationalStandard)

                # send email to rockman

                transactionType = 'Supplier Payment'
                # generate customer pdf file, Example : Tranfer_Invoice.pdf
                # Invoice(str(paymentInDollars), customerName,
                #         PaymentMode, str(PaymentDate), 'Transfer details', supplierCompany, transactionType)
                # send Email to customer
                # SendEmail(customerEmail, 'Supplier Payment')
                serializer = SupplierPaymentSerializers(new_supplierpayments)
                d['data'] = serializer.data
                return Response(d)
        else:
            d['hasEmailAddress'] = False
            d['StatusCode'] = 99
            d['StatusMessage'] = 'There is no open consignment in Turkey, you need to Open a new consignment before you can add supplied goods'
            return Response(d)


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
        customers = Customer.objects.filter(
            account_balance__gt=0).order_by('-id')
        serializer = CustomerSerializers(customers, many=True)
        return Response(serializer.data)


class CustomerTransfersView(APIView):

    def get(self, request, username):
        customUser = CustomUser.objects.filter(
            username__iexact=username).get()
        print(customUser.id)
        customerID = Customer.objects.get(user_id_id=customUser.id)
        # print(customerID)

        customerTransfers = Transfer.objects.filter(
            customer_id__id=customerID.id)
        serializer = TransferSerializers(customerTransfers, many=True)
        return Response(serializer.data)


class CustomerSupplyPaymentView(APIView):

    def get(self, request, username):
        customUser = CustomUser.objects.filter(
            username__iexact=username).get()
        customerID = Customer.objects.get(user_id_id=customUser.id)

        customerSupplierPayment = SupplierPayment.objects.filter(
            customer_id__id=customerID.id)
        serializer = SupplierPaymentSerializers(
            customerSupplierPayment, many=True)
        return Response(serializer.data)


class FreightSerializersView(APIView):
    def get(self, request):
        Freights = Freight.objects.order_by('-id')
        serializer = FreightSerializers(Freights, many=True)
        return Response(serializer.data)

    def post(self, request):
        postdata = request.data
        # get cutomer id with the username from the frontend form
        customer = CustomUser.objects.filter(
            username__iexact=postdata["username"]).get()
        # print(customer.id)

        # money paid by a customer must be subtracted from the customers balance in the customer model
        customerByCustomUserId = Customer.objects.filter(
            user_id__id=customer.id).get()

        #
        getFreight = Freight.objects.filter(customer_id__id=customerByCustomUserId.id,
                                            consignment_id__status='open', consignment_id__city='Turkey')

        if getFreight.exists():
            # get editable object to object content with ease
            getEditableFreightObject = Freight.objects.filter(customer_id__id=customerByCustomUserId.id,
                                                              consignment_id__status='open', consignment_id__city='Turkey').get()
            # update freight total weight
            getEditableFreightObject.total_weight += float(
                postdata["total_weight"])
            totalWeightValue = getEditableFreightObject.total_weight

            getEditablePaymentObject = Payment.objects.get(
                id=getEditableFreightObject.payment_id.id)
            print(getEditablePaymentObject.amount_sent_cedis)
            getEditablePaymentObject.amount_sent_cedis = totalWeightValue * 8
            print(getEditablePaymentObject.amount_sent_cedis)
            getEditablePaymentObject.save()

            # exit()

            getEditableFreightObject.save()
            serializer = FreightSerializers(getEditableFreightObject)
            return Response(serializer.data)
        else:
            # get open and city is Turkey consignment
            getEditableConsignmentObject = Consignment.objects.filter(
                status='open', city='Turkey').get()

            # get cutomer id with the username from the frontend form
            customer = CustomUser.objects.filter(
                username__iexact=postdata["username"]).get()

            customerByCustomUserId = Customer.objects.filter(
                user_id__id=customer.id).get()
            # print(getEditableConsignmentObject.id)
            # exit()

            # create payment object
            new_payment = Payment.objects.create(
                # date=postdata["date"],
                status=postdata["payment_id"]["status"], payment_mode=postdata["payment_id"]["payment_mode"],
                balance=postdata["payment_id"]["balance"], dept=postdata["payment_id"]["dept"],
                # amount_sent_dollars=postdata["payment_id"]["amount_sent_dollars"],
                amount_sent_cedis=postdata["total_weight"]*8, transaction_type='Freight')

            new_freight = Freight.objects.create(
                customer_id=Customer.objects.get(id=customerByCustomUserId.id),
                # date=postdata["date"],
                consignment_id=getEditableConsignmentObject.id,
                payment_id=new_payment,
                total_weight=postdata["total_weight"],
                # amount_sent_dollars=postdata["amount_sent_cedis"],
                goods_desc=postdata["goods_desc"])

            # print(new_freight)
            # exit()
            new_freight.save()
            serializer = FreightSerializers(new_freight)
            return Response(serializer.data)


class FreightDetailsView(APIView):
    def get(self, request, pk):
        freight = Freight.objects.get(id=pk)
        serializer = FreightSerializers(freight, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        freight_obj = Freight.objects.get(id=pk)
        data = request.data
        print(data)

        freight_obj.picked_up = data['checked']

        freight_obj.save()

        serializer = FreightSerializers(freight_obj)
        return Response(serializer.data)


class FreightUpdateIsPaidView(APIView):
    def put(self, request, pk):
        freight_obj = Freight.objects.get(id=pk)
        data = request.data

        freight_obj.isPaid = data['isPaid']

        freight_obj.save()

        serializer = FreightSerializers(freight_obj)
        return Response(serializer.data)


class FreightUpdateNoteView(APIView):
    def put(self, request, pk):
        freight_obj = Freight.objects.get(id=pk)
        data = request.data

        freight_obj.note = data['note']

        freight_obj.save()

        serializer = FreightSerializers(freight_obj)
        return Response(serializer.data)


class ConsignmentListView(APIView):
    def get(self, request):
        consignment = Consignment.objects.filter(status="open")
        serializer = ConsignmentSerializers(consignment, many=True)
        return Response(serializer.data)

    def post(self, request):
        postdata = request.data
        # print(postdata)

        # get check if a consignment is available in Turkey. if true then you cannot create a new consignment
        consignment = Consignment.objects.filter(city="Turkey")
        print(consignment.exists())
        # exit()
        if consignment.exists():
            d = dict()
            d['StatusCode'] = 99
            d['StatusMessage'] = 'There is a consignment already open in Turkey, you cant open two consignments in Turkey'
            return Response(d)
        else:
            # create a new consignment
            new_consignment = Consignment.objects.create(
                status=postdata["status"],
                city=postdata["city"],
                timestamp=postdata["timestamp"],
                updated=postdata["updated"]
            )
            new_consignment.save()
            serializer = ConsignmentSerializers(new_consignment)
            return Response(serializer.data)


class ConsignmentListOpenAndInTurkeyView(APIView):
    def get(self, request):
        consignment = Consignment.objects.filter(status="open", city="Turkey")
        serializer = ConsignmentSerializers(consignment, many=True)
        return Response(serializer.data)


class ConsignmentListOpenAndInAccraView(APIView):
    def get(self, request):
        consignment = Consignment.objects.filter(status="open", city="Accra")
        serializer = ConsignmentSerializers(consignment, many=True)
        return Response(serializer.data)


class ConsignmentUpdateView(APIView):
    # def get(self, request, pk):
    #     freight = Freight.objects.get(id=pk)
    #     serializer = FreightSerializers(freight, many=False)
    #     return Response(serializer.data)

    def put(self, request, pk):
        consignment_obj = Consignment.objects.get(id=pk)
        data = request.data

        consignment_obj.city = data['city']

        consignment_obj.save()

        serializer = ConsignmentSerializers(consignment_obj)
        return Response(serializer.data)

class ConsignmentUpdateStatusView(APIView):
    def put(self, request, pk):
        consignment_obj = Consignment.objects.get(id=pk)
        data = request.data

        consignment_obj.status = data['status']

        consignment_obj.save()

        serializer = ConsignmentSerializers(consignment_obj)
        return Response(serializer.data)


class FreightSendSMSView(APIView):
    def post(self, request):
        postdata = request.data
        
        d = dict()
        d['StatusCode'] = '99'
        d['StatusMessage'] = 'Sending messsages failed'
        consigmentInAccra = Freight.objects.select_related(
            'customer_id', 'customer_id__user_id').filter(consignment_id=postdata['consignment_number'])

        for px in consigmentInAccra:
            customerPhone = px.customer_id.user_id.phone_no
            customerPhoneInternationalStandard = '233' + customerPhone

            customerName = px.customer_id.user_id.first_name + \
                ' ' + px.customer_id.user_id.last_name
            freightCost = (px.total_weight + 0.00) * 8.00
            pickDate = postdata['pickup_date']
            
            content = 'Dear ' + customerName + ' , ' + 'your freight cost' + ' $' + \
                str(format(freightCost, '.2f')) + \
                ', Pickup Date is ' + pickDate + ' .'

            
            # send SMS to customer
            SendSMS(content, customerPhoneInternationalStandard)
            
            d['StatusCode'] = '01'
            d['StatusMessage'] = 'Messages sent to all customers successfully'
        return Response(d)
