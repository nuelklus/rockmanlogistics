from rest_framework import serializers
from .models import CustomUser, Customer, Transfer, Supplier, SupplierPayment, Payment, Freight, Consignment


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # read_only_fields = ['id']
        depth = 1


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class CustomerUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # read_only_fields = ['id']
        depth = 1


class CustomerSerializers(serializers.ModelSerializer):
    user_id = CustomUserSerializers()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user_id')
        user = CustomUserSerializers.create(
            CustomUserSerializers(), validated_data=user_data)
        customer, created = Customer.objects.update_or_create(user_id=user, account_balance=validated_data.pop(
            'account_balance'), dept=validated_data.pop('dept'), company_name=validated_data.pop('company_name'))
        return customer


class TransferSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        read_only_fields = ['id']
        depth = 2


class SupplierSerializers(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['id']
        # depth = 1


class SupplierPaymentSerializers(serializers.ModelSerializer):

    class Meta:
        model = SupplierPayment
        fields = '__all__'
        read_only_fields = ['id']
        depth = 3


class TransferSumSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['amount_sent_dollars']


class SupplierPaymentSumSerializers(serializers.ModelSerializer):
    class Meta:
        model = SupplierPayment
        fields = ['goods_cost_dollars']


class FreightSerializers(serializers.ModelSerializer):
    class Meta:
        model = Freight
        fields = '__all__'
        read_only_fields = ['id']
        depth = 2


class ConsignmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Consignment
        fields = '__all__'
        read_only_fields = ['id']
