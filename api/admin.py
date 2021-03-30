from django.contrib import admin

from .models import Article, CarouselImage, PrimaryImage, SecondaryImage, NurseryImage, DispensaryImage

admin.site.register(Article)
admin.site.register(CarouselImage)
admin.site.register(PrimaryImage)
admin.site.register(SecondaryImage)
admin.site.register(NurseryImage)
admin.site.register(DispensaryImage)