from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
import json
import datetime
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')
    # return HttpResponse("<h1>This site will be back soon</h1>")

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        useremail = request.POST['email']
        userpassword = request.POST['password']
        userpassword2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username")
            return redirect('signup')

        if User.objects.filter(email=useremail).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 character")

        if userpassword != userpassword2:
            messages.error(request, "Password didn't match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username musst be Alpha-Numeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, useremail, userpassword)
        myuser.save()

        new_cust = Customer(user=myuser,  email=useremail)
        new_cust.save(())


        messages.success(request, "Your account has been succesfully created")

        return redirect('login')
    else:        
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        userpassword = request.POST['password']

        user = auth.authenticate(username=username, password=userpassword)

        if user is not None:
            auth.login(request, user)
            return redirect('store')    
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signup')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect("home")


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems' : cartItems}
    return render(request, 'store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems' : cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems' : cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = Orderitem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity) + 1
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity) - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        print("User is not logged in")

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse("Order Completed", safe=False)


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
