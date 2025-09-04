from django.urls import path, include
from . import views

app_name='u_table'

urlpatterns=[
    path('', views.index, name='index'),
    path('info_form/', views.info_form, name='info_form'),
    path('get_data/', views.get_data, name='get_data'),
    path('update_data/', views.update_data, name='update_data'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_single_user/<int:user_id>/', views.update_single_user, name='update_single_user'),
]