from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/data/campaign/
    path('campaign/table/', views.tampil_fact_campaign, name='tampil_campaign'),
    path('campaign/chart/', views.tampil_fact_campaign_chart, name='tampil_campaign_chart'),
    # http://127.0.0.1:8000/data/customers/
    path('customers/table/', views.tampil_fact_customers, name='tampil_customers'),
    path('customers/chart/', views.tampil_fact_customers_chart, name='tampil_customers_chart'),
    # contoh: http://127.0.0.1:8000/data/sales/
    path('sales/table/', views.tampil_fact_sales, name='tampil_sales'),
    path('sales/chart/', views.tampil_fact_sales_chart, name='tampil_sales_chart'),
]