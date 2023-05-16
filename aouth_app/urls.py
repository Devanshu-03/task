from django.urls import path
from aouth_app.views import insert_user_details,listusers
from aouth_app import views
from .views import home
from .views import list_user


urlpatterns = [
    path('api/userdetails/', insert_user_details, name='insert_user_details'),
    path('api/listusers/', listusers),
    path('',views.home,name='home'),
    path('list_user/',views.list_user,name='listuser')
    
]