from django.urls import path
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path('',views.home,name='home'),
    path('menu/',views.menu,name='menu'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.logIn,name='login'),
    path('logout/',views.logOut,name='logout'),
    path('indMenu/<int:id>/',views.indMenu,name='indMenu'),
    path('signup/',views.signUp,name="signup"),
    path('provost/',views.provost,name='provost'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('manager/',views.manager,name='manager'),
    path('student/',views.student,name='student'),
    path('managerMenu/<int:id>/',views.managerMenu,name='managerMenu'),
    path('cart/',views.cart,name='cart'),
    path('payment/<str:id>/',views.payment,name='payment'),
    path('notun/<str:id>/<int:id2>/<int:id3>/',views.notun,name='notun'),
    path('coupon/<str:id>/',views.coupon,name='coupon'),
    path('arekta/<str:id>/',views.render_pdf_view,name='arekta'),
    path('feast/<str:id>/',views.feast_pdf_view,name='feast'),
    path('error/',views.error,name='error')
    
]