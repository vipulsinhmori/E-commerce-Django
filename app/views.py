
from.models import Customer, Product, Cart, OrderPlaced
from django.shortcuts import render, redirect # Make sure to import your form
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib import messages
from .forms import CustomerProfileForm
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import OrderPlaced
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from .models import Product, Cart
from django.shortcuts import render
from django.http import JsonResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from django.shortcuts import render, HttpResponse


#-----------------otp-------------
from django.shortcuts import render
import pyotp
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import pyotp
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
# from .models import OTP
# from .views import send_otp
#----------------end--------------------------

# def send_otp(request):
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import OTP  # Import your OTP model
from django.contrib.auth.models import User
import pyotp

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import OTP  # Import your OTP model
from django.contrib.auth.models import User
# from django.template import TemplateDoesNotExist
import pyotp

import pyotp
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import OTP

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        
        if user:
            # Generate OTP
            otp_secret = pyotp.random_base32()
            otp = pyotp.TOTP(otp_secret)
            otp_code = otp.now()

            # Save OTP to the database
            otp_obj, created = OTP.objects.get_or_create(user=user, email=email)
            otp_obj.otp_secret = otp_secret
            otp_obj.save()

            # Send OTP via email
            subject = 'Your OTP for Login'
            message = f'Your OTP for login is: {otp_code}'
            from_email = 'vipulmori073@gmail.com'  # Update with your email
            recipient_list = [email]

            # Add Phone OTP API

            send_mail(subject, message, from_email, recipient_list)

            return redirect('/verify_otp')
        else:
            return redirect('/sendotp')
    return render(request, 'app/sendotp.html', {'message': 'Email not found'})
        



def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        if user:
            otp_obj = OTP.objects.filter(user=user, is_verified=True, otp_secret=otp_code).first()
            if otp_obj:
                user = authenticate(request, username=user.username, password='')
                if user:
                    login(request, user)
                else:
                    return render(request, 'app/login.html', {'message': 'Login successful'})
            else:
                return redirect('/')
        else:
                messages.error(request, 'Invalid OTP')
    else:
            messages.error(request, 'User with provided email not found')
    return render(request, 'app/verify_otp.html')








def mobile(request, data=None):
    if data == None:
        mobile=Product.objects.filter(category='M')
    elif data=='oneplus' or data=='Vivo':
        mobile=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
         mobile=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
         mobile=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobile': mobile})


def laptop(request, data=None):
 if data == None:
        laptop=Product.objects.filter(category='L')
 elif data=='lenevo' or data=='Asus':
        laptop=Product.objects.filter(category='L').filter(brand=data)
 elif data=='below':
         laptop=Product.objects.filter(category='L').filter(discounted_price__lt=10000)
 elif data=='above':
         laptop=Product.objects.filter(category='L').filter(discounted_price__gt=10000)
 return render(request, 'app/Laptop.html',{'laptop':laptop})

def topwears(request, data=None):
 if data == None:
        topwears=Product.objects.filter(category='TW')
 elif data=='T-shrit' or data=='AMERICANCREW':
        topwears=Product.objects.filter(category='TW').filter(brand=data)
 elif data=='below':
         topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=5050)
 elif data=='above':
         topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=600)
 return render(request, 'app/topwears.html',{'topwears':topwears})

def bottomwears(request, data=None):
 if data == None:
        bottomwears=Product.objects.filter(category='BW')
 elif data=='jeans5' or data=='pants':
        bottomwears=Product.objects.filter(category='BW').filter(brand=data)
 elif data=='below':
         bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=400)
 elif data=='above':
         bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=600)
 return render(request, 'app/bottomwears.html',{'bottomwears':bottomwears})

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobile=Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')

        return render(request,'app/home.html/',
        {'topwears':topwears,'bottomwears':bottomwears,'mobile':mobile, 'laptop': laptop})




class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the actual user ID
            user_id = request.user.id

            # Now you can use user_id in your query
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=user_id)).exists()
        else:
            # If the user is not authenticated, set item_already_in_cart to False
            item_already_in_cart = False

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')



# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from .models import Product, Cart, OTP
# from django.contrib.auth.models import User

# @login_required
# def add_to_cart(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('prod_id')
#         product = Product.objects.get(id=product_id)
#         user = request.user
#     else:
#         redirect(request, '/sendotp')
#         # Check OTP verification for the user
#         otp_obj = OTP.objects.filter(user=user, is_verified=True).first()

#         if otp_obj:
#             # OTP is verified, add the product to the cart
#             Cart.objects.create(user=user, product=product)
#             messages.success(request, 'Product added to cart successfully!')
#         else:
#             return render(request, 'app/verify_otp.html')
        

#             return render(request,'/cart')





@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount

            totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emtycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
# -------------------EndplusCart----------------------


# -----------------------startminuscart------------------
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
# ---------------------Endminus------------------------------------------

# ------------------------------removecart----------------------------------
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
           
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
# ----------------------------removecart--------------------------------------


                
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})



@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')

    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        # For example, you could redirect the user to an error page or return an error message.
        return HttpResponse("Customer not found", status=404)

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()

    return redirect("orders")


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation!! Registration successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})
    
    
    
@login_required
def payment_success_view(request):
    user = request.user
    custid = request.GET.get('custid')

    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        # For example, you could redirect the user to an error page or return an error message.
        return HttpResponse("Customer not found", status=404)

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()

    return redirect("orders")

    response = render(request,'payment_success.html')
    
    return response



    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})

# -----------------------------
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):  # Corrected the method signature
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']  # Corrected 'cleaned_date' to 'cleaned_data'
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']  # Corrected 'stste' to 'state'
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode) 
            reg.save()

            messages.success(request,'Congratulations!! Profile Updated Successfully')  # Corrected 'Messages' to 'messages'
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

# ---------------------- payment gateway --------------------->
# views.py

def handle_googlepay_payment(request):
    if request.method == 'POST':
        id_token_str = request.POST['idToken']

        try:
            # Verify the ID token
            id_info = id_token.verify_oauth2_token(
                id_token_str, requests.Request(), YOUR_GOOGLE_PAY_CLIENT_ID
            )

            # Handle payment success
            # Add your payment processing logic here

            return JsonResponse({'status': 'success'})

        except ValueError:
            # Invalid token
            return JsonResponse({'status': 'error', 'message': 'Invalid token'})

    return render(request, 'payment/googlepay.html')


def forgot(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            user_obj = User.objects.filter(username=username).first()

            if not user_obj:
                return redirect('forgot-password')

            token = str(uuid.uuid4())
            

            # Extract the email address from the User object
            email = user_obj.email

            send_forget_password_mail(email, token)
    except Exception as e:
        print(e)
    return render(request, 'password_reset.html')

def changepassword(request, token):
    context = {}
    try:
        reset_obj = PasswordReset.objects.get(forget_password_token=token)
        # Now you can use reset_obj to verify the token and proceed with password reset
        print(reset_obj)
    except PasswordReset.DoesNotExist:
        print("Token not found.")
    except Exception as e:
        print(e)
    return render(request, 'passwordchange.html', context)





