from .extension import ma


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('cust_id', 'cust_name', 'contact_number', 'cust_mail')


class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('rest_id', 'rest_name', 'contact_number', 'rest_address')


class DeliveryPersonSchema(ma.Schema):
    class Meta:
        fields = ('dp_id', 'dp_name', 'contact_number', 'dp_mail')


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'cust_id', 'rest_id', 'dp_id', 'order_date', 'order_addr')


class OrderItemSchema(ma.Schema):
    class Meta:
        fields = ('item_id', 'order_id', 'item_name', 'item_price')


class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('pay_id', 'order_id', 'total_amount', 'amount_payed', 'amount_returned')