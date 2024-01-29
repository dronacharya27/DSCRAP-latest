from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact2,name='contact'),
    path('signup/',views.handlesignup),
    path('login/',views.handlelogin),
    path('logout/',views.handlelogout),
    path('scrapcalc/',views.trye,name='scr'),
    path('add/',views.address,name='add'),
] 
