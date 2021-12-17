from django.urls import path
from user import views


urlpatterns = [
    path('reg',views.reg_view,name='reg'),
    path('login',views.login_view,name='login'),
    path('login_out',views.login_out,name="login_out")

]