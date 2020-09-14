from django.contrib import admin
from .models import *

admin.site.site_header = 'Python Libralies Courses Admin'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'Back end'

class AllproductAdmin(admin.ModelAdmin):
	list_display = ['name','id','instock','price','quantity']
	list_editable = ['instock','price','quantity']

admin.site.register(Allproduct,AllproductAdmin)
admin.site.register(Profile)
admin.site.register(Cart)

class OrderListAdmin(admin.ModelAdmin):
	list_display = ['orderid','productname','total']

admin.site.register(OrderList, OrderListAdmin)
admin.site.register(OrderPending)
