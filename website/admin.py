from django.contrib import admin
from .models import userAccount, product, order
import webbrowser
##admin header
admin.site.site_header = "I am SOAP - Dashboard"
admin.site.site_title = "I am SOAP - Admin"

##admin actions and customising layout
from django.shortcuts import render
def Export_Products(self, request, obj):
    count = obj.count()
    page_url = 'website/exportProducts.html'
    array = []
    products = product.objects.all().order_by('name')
    for x in range(int(count)):
        itemName = products[x].name
        itemPrice = products[x].price
        itemQuantity = products[x].quantity
        itemCategory = products[x].category
        itemPlasticFree = products[x].plastic_free
        itemPalmFree = products[x].palm_free
        itemData = {"name": itemName, "price":itemPrice,"quantity":itemQuantity, "category":itemCategory,"plastic":itemPlasticFree,"palm":itemPalmFree}
        array.append(itemData)
    data = {"products":array}
    return render(request,page_url,data)


Export_Products.label = "Export" # optional
Export_Products.short_description = "Export selected products to pdf" # optional

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price', 'quantity','category','plastic_free','palm_free']
    ordering = ['name']
    actions = [Export_Products]

class orderAdmin(admin.ModelAdmin):
    list_display = ['user','date', 'shipping','total','complete']
    ordering = ['date']

# Register your models here.
admin.site.register(userAccount)
admin.site.register(product,ProductAdmin)
admin.site.register(order, orderAdmin)