from django.contrib import admin
from .models import Allocation, Receipt, PaymentAllocation, Payment

admin.site.register(Allocation)
admin.site.register(Receipt)
admin.site.register(PaymentAllocation)
admin.site.register(Payment)
