from django.contrib import admin
from .models import FactCampaign, FactCustomer, FactSales

# Register your models here.
# Daftarkan model FactCampaign
@admin.register(FactCampaign)
class FactCampaignAdmin(admin.ModelAdmin):
    list_display = ('product', 'year', 'month', 'units_sold', 'revenue', 'roi')
    list_filter = ('year', 'product')
    search_fields = ('product',)

# Daftarkan model FactCustomer
@admin.register(FactCustomer)
class FactCustomerAdmin(admin.ModelAdmin):
    list_display = ('product', 'state', 'city', 'year', 'month', 'units_sold', 'revenue')
    list_filter = ('year', 'state', 'product')
    search_fields = ('product', 'city', 'state')

# Daftarkan model FactSales
@admin.register(FactSales)
class FactSalesAdmin(admin.ModelAdmin):
    list_display = ('product', 'retailer', 'sales_method', 'year', 'month', 'units_sold')
    list_filter = ('year', 'retailer', 'sales_method')
    search_fields = ('product', 'retailer')