from django.contrib import admin

from .models import *

admin.site.register(Subject)
admin.site.register(Period)
admin.site.register(DailyTimeTable)
admin.site.register(WeeklyTimeTable)
