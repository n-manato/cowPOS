from django.contrib import admin
from . import models

# 会計データ
class Accounting_DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','saled','c_time')
admin.site.register(models.Accounting_Data,Accounting_DataAdmin)

# 商品データ
class Prodact_NameAdmin(admin.ModelAdmin):
    list_display = ('P_name', 'P_price')
admin.site.register(models.Prodact_Name,Prodact_NameAdmin)
