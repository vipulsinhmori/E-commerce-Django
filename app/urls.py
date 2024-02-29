from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomerRegistrationView
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm,SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from .views import ProfileView
# from django.urls import path
from .views import orders











urlpatterns = [
    # path('', views.home),
path('', views.ProductView.as_view(), name="home"),  
path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'), 
path('buy/', views.buy_now, name='buy-now'),


path('sendotp/', views.send_otp, name='sendotp'),
path('verify_otp/', views.verify_otp, name='verify_otp'),
   

path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

path('cart/', views.show_cart, name='showcart'),


path('pluscart/', views.plus_cart),
path('minuscart/', views.minus_cart),

path('removecart/', views.remove_cart),



# app/urls.py



    # Other paths...
    path('orders/', orders, name='orders'),


path('profile/', ProfileView.as_view(), name='profile'),

path('address/', views.address, name='address'),
path('address/', views.address, name='address'),

path('mobile/', views.mobile, name='mobile'),
path('mobile/<slug:data>', views.mobile, name='mobile'),

path('laptop/', views.laptop, name='laptop'),
path('laptop/<slug:data>', views.laptop, name='laptop'),  

path('topwears/', views.topwears, name='topwears'),
path('topwears/<slug:data>', views.topwears, name='topwears'),

path('bottomwears/', views.bottomwears, name='bottomwears'),
path('bottomwears/<slug:data>', views.bottomwears, name='bottomwears'),

path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),

path('accounts/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm),name='login'),

path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=SetPasswordForm),name='password_reset_confirm'),

path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

path('checkout/', views.checkout, name='checkout'),
path('paymentdone/', views.payment_done, name='paymentdone'),

path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=PasswordResetForm),name='password_reset'),

path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/pass/'),name='passwordchange'),
path('pass/', auth_views.PasswordChangeView.as_view(template_name='app/pass.html'),name='pass'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



