from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('add/', views.add_record, name='add_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
]
