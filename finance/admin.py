from django.contrib import admin
from .models import ReceiptAllocation, Receipt, PaymentAllocation, Payment

admin.site.register(ReceiptAllocation)
admin.site.register(Receipt)
admin.site.register(PaymentAllocation)
admin.site.register(Payment)
