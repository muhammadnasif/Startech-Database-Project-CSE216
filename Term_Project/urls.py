"""Term_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import sales.views as sales_view
import servicing.views as servicing_view
import customer.views as customer_view
import administrator.views as administrator_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales_entry',sales_view.load),
    path('servicing',servicing_view.load),
    path('product_info', sales_view.product_info),
    path('home',customer_view.load),
    path('laptop',customer_view.load_laptop),
    path('login',customer_view.login),
    path('',customer_view.load),
    path('admin_panel',administrator_view.load),
    path('logout', customer_view.del_session),
    path('hire', administrator_view.hire),
    path('all_employees', administrator_view.show_employees),
    path('imei_entry',sales_view.imei_entry_load),
    path('submit_imei',sales_view.submit_imei),
    path('<int:id>',administrator_view.update_employees, name='employee_update'),
    path('check_stock',sales_view.check_stock),
    path('sale_status', administrator_view.sale_status),
    path('sales_representative_status',sales_view.sales_representative_status),
    path('<int:id>', administrator_view.employee_report, name='employee_report'),
    path('change_info',sales_view.change_info)
]
