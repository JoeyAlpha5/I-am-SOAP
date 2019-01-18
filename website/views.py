from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import product, userAccount, order
from django.core.mail import send_mail
from .forms import shippingForm, accountForm
import cloudinary
import cloudinary.uploader
import cloudinary.api
import ast


# Create your views here.
@login_required(login_url='/login')
def account(request):
    if request.method == "GET":
        page_url = 'website/account.html'
        return render(request, page_url, {"shipping":shippingForm(), "account":accountForm()})
    #get the user's account details
    if request.method == "POST" and request.POST["type"] == "getAccount":
        user = request.user
        user_account = User.objects.filter(username=user)
        username = user_account[0].username
        email = user_account[0].email
        first_name = user_account[0].first_name
        last_name = user_account[0].last_name
        # ##get address info
        # UserAddress
        data = {}
        ##products
        cart = ast.literal_eval(request.POST["cart"])
        print(cart)
        price = 0
        for x in cart:
            prod = product.objects.filter(id=x["id"])
            price += (prod[0].price*int(x["quantity"]))
        if userAccount.objects.filter(user=user_account[0]).exists() == False:
            data = {"username": username, "email":email, "name":first_name,"surname":last_name, "totalPrice":price,"productcount":len(cart)}
        else:
            ##get address info
            UserAddress = userAccount.objects.filter(user=user_account[0])
            street = UserAddress[0].street_address
            apartment = UserAddress[0].apartment
            city = UserAddress[0].city
            province = UserAddress[0].Province
            country = UserAddress[0].Country
            data = {"username": username, "email":email, "name":first_name,"surname":last_name, "street":street, "apartment":apartment, "city":city, "province":province, "country":country, "totalPrice":price,"productcount":len(cart)}
        return JsonResponse(data)
    elif request.method == "POST" and request.POST["type"] == "saveAddres":
        street = request.POST["street"]
        apartment = request.POST["apartment"]
        city = request.POST["city"]
        province = request.POST["Province"]
        country = request.POST["Country"]
        apartment = request.POST["apartment"]
        ##
        user = User.objects.filter(username=request.user)
        if userAccount.objects.filter(user=user[0]).exists():
            account = userAccount.objects.get(user=user[0])
            account.street_address = street
            account.city = city
            account.Province = province
            account.Country = country
            account.apartment = apartment
            account.save()
        else:
            account = userAccount()
            account.street_address = street
            account.city = city
            account.Province = province
            account.Country = country
            account.apartment = apartment
            account.user = user[0]
            account.save()
        page_url = 'website/account.html'
        return render(request, page_url, {"shipping":shippingForm(),"account":accountForm()})

    elif request.method == "POST" and request.POST["type"] == "saveAccount":
        name = request.POST["name"]
        surname = request.POST["surname"]
        username = request.POST["username"]
        email = request.POST["email"]
        ##
        user = User.objects.get(username=request.user)
        user.first_name = name
        user.last_name = surname
        user.username = username
        user.email = email
        user.save()
        page_url = 'website/account.html'
        return render(request, page_url, {"shipping":shippingForm(),"account":accountForm()})
    
    elif request.method == "POST" and request.POST["type"] == "placeOrder":
        totalCost = request.POST["cost"]
        cart = ast.literal_eval(request.POST["cart"])
        shipping = request.POST["shipping"]
        print(shipping)
        array = []
        for x in cart:
            prod = product.objects.filter(id=x["id"])
            itemName = prod[0].name 
            itemQuatity = prod[0].quantity 
            itemPrice = prod[0].price
            itemImage = str(prod[0].ig.url)
            ##descrease quantity
            prodQ = product.objects.get(id=x["id"])
            prodQ.quantity = itemQuatity - x["quantity"]
            if itemQuatity - x["quantity"] < 0:
                prodQ.quantity = 0
            prodQ.save()
            ##the item that the user has ordered including the name, the price, the quantity
            ##that the user has ordered and the link to the product image
            item = {"name": itemName, "quantity":x["quantity"], "price":itemPrice, "image":itemImage}
            array.append(item)
            print(array)
        ## get the user
        user = User.objects.filter(username=request.user)
        #check if the user has an account
        if userAccount.objects.filter(user=user[0]).exists() and user[0].first_name != "":
            ##get user's address
            Address = userAccount.objects.filter(user=user[0])
            street = Address[0].street_address
            ##if the user does have an address
            if street == "":
                errorMessage = "Please enter and save your shipping address"
                return JsonResponse({"Message":errorMessage})
            else:
                apartment = Address[0].apartment
                city = Address[0].city
                province = Address[0].Province
                country = Address[0].Country
                ##save the order
                new_order = order()
                new_order.user = user[0]
                new_order.products = str(array)
                new_order.total = totalCost[1:]
                ##if shipping is selected set shipping bool to true
                if shipping == "R75":
                    new_order.shipping = True
                new_order.save()
                new_order_id = new_order.id
                ##set up email
                subject = "I am SOAP Customer Invoice - New order placed by: " + str(user[0].first_name + " " + user[0].last_name)
                to = ["neil@iamsoap.co.za", user[0].email]
                from_email = "sales@iamsoap.co.za"
                message = "<center style='width:937px;'><img width='200px' src='https://lh6.googleusercontent.com/dxnl2y-dmH21_vPaXnaeN08zWGueB5tEXWiIsaBVVg2_ksk26rb39GBIugvbcMAQq3lpLf9e9U01qM-MW9J3=w1366-h626'/></center>"
                message = message + "<p style='width:937px;margin-top:0px;background:#80808017;padding:0px;font-size:20px;text-align:-webkit-center;text-align:-moz-center;margin-bottom:0px;'>Products ordered by"+str(user[0].first_name + " " + user[0].last_name)+"</p>"
                message = message + "<table style='width:937px; background:#8080800a;'><tr><th style='width:50%;text-align:left;padding-left:100px;'><u>Product name</u></th><th style='text-align:-webkit-center;text-align:-moz-center;'><u>Price</u></th></tr></table>"
                for n in array:
                    orderPrice = n["price"]*n["quantity"]
                    productTable = "<table style='width:937px;background:#8080800a;'><tr><td style='width:50%;text-align:left;padding-left:100px;'><b>"+n['name']+"</b> * "+str(n["quantity"])+" @ R" +str(n['price'])+" each</td><td style='text-align:-webkit-center;text-align:-moz-center'><b>R"+str(orderPrice)+"</b></td></tr></table>"
                    message = message + productTable
                message = message + "<p style='width:937px;margin-top:0px;background:#80808017;padding:0px;font-size:20px;text-align:-webkit-center;text-align:-moz-center;margin-bottom:0px;'>User account details</p>"
                message = message + "<table style='width:937px; background:#8080800a;'><tr><td style='width:50%;text-align:left;padding-left:100px;'><b>Street address:</b></td><td style='text-align:-webkit-center;text-align:-moz-center'>"+street+"</td></tr></table>"
                message = message + "<table style='width:937px; background:#8080800a;'><tr><td style='width:50%;text-align:left;padding-left:100px;'><b>Apartment:</b></td><td style='text-align:-webkit-center;text-align:-moz-center'>"+apartment+"</td></tr></table>"
                message = message + "<table style='width:937px; background:#8080800a;'><tr><td style='width:50%;text-align:left;padding-left:100px;'><b>City:</b></td><td style='text-align:-webkit-center;text-align:-moz-center'>"+city+"</td></tr></table>"
                message = message + "<table style='width:937px; background:#8080800a;'><tr><td style='width:50%;text-align:left;padding-left:100px;'><b>Province:</b></td><td style='text-align:-webkit-center;text-align:-moz-center'>"+province+"</td></tr></table>"
                message = message + "<table style='width:937px; background:#8080800a;'><tr><td style='width:50%;text-align:left;padding-left:100px;'><b>Country:</b></td><td style='text-align:-webkit-center;text-align:-moz-center'>"+country+"</td></tr></table>"
                message = message + "<p style='width:937px;padding:10px;font-weight:bold;margin:0px;text-align:-webkit-center;text-align:-moz-center'>Shipping: "+shipping+"</p>"
                message = message + "<p style='width:937px;padding:10px;font-weight:bold;margin:0px;text-align:-webkit-center;text-align:-moz-center'><b>Payment</b>: payment details will soon be communicated with you</p>"
                message = message + "<p style='width:937px;padding:10px;font-weight:bold;margin:0px;text-decoration:underline;text-align:-webkit-center;text-align:-moz-center'>Total including shipping: "+totalCost+"</p>"
                message = message + "<center style='width:937px;'><a style='text-decoration:none;' href='http://iamsoap.herokuapp.com/orders/"+str(new_order_id)+"'><p style='width:308px;padding:10px;margin:0px;text-align:-webkit-center;text-align:-moz-center;border-radius:20px;background:#607D8B;color:white;'>Click to view order details</p></a></center>"
                send_mail(subject,message,from_email,to,fail_silently=False,html_message=message)
                return JsonResponse({"Message":"Successfull"})
        else:
            errorMessage = "Please enter and save your shipping address"
            if user[0].first_name == "":
                errorMessage = "Please enter and save your name and surname"
            if userAccount.objects.filter(user=user[0]).exists() == False:
                errorMessage = "Please enter and save your shipping address"
            return JsonResponse({"Message":errorMessage})
##register page
def register(request):
    if request.method == "GET":
        page_url = 'website/register.html'
        return render(request, page_url)

    if request.method == "POST" and request.POST["type"] == "registerAccount":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        Message = "Your account has been created"
        ## check if user exists
        userExists = User.objects.filter(username=username).exists()
        if userExists == True:
            Message = "The username already exists"
        elif len(password) >= 8: 
            ##if password is numeric 
            ##check password
            try:
                passwordIsInt = int(password)
                print(passwordIsInt)
                Message = "Your password is entirely numeric"
            except:
                Message = "Your account has been created"
                ##create a user instance
                new_user = User()
                new_user.username = username
                new_user.email = email
                new_user.set_password(password)
                new_user.save()
                message = "<center style='width:937px;'><img width='200px' src='https://lh6.googleusercontent.com/dxnl2y-dmH21_vPaXnaeN08zWGueB5tEXWiIsaBVVg2_ksk26rb39GBIugvbcMAQq3lpLf9e9U01qM-MW9J3=w1366-h626'/></center><div style='width:937px; height:120px; background:#80808008;text-align:-webkit-center;text-align:-moz-center;padding:20px;'><p>Your <i>I am SOAP</i> account has successfully been created</p><a href='http://www.iamsoap.co.za'><button style='width:200px; height:35px;border:0px;color:white;background:#e00707c9;border-radius:2px;cursor:pointer;'>Start shopping!</button></a></div>"
                subject = "Your new I am SOAP account"
                sender = "sales@iamsoap.co.za"
                reciever = [email,"neil@iamsoap.co.za"]
                send_mail(subject,message,sender,reciever,fail_silently=False,html_message=message)
        else:
            Message = "Your password must 8 characters or more"

        return JsonResponse({"Message": Message})

##homepage
def home(request):
    if request.method == "GET":
        page_url = 'website/index.html'
        return render(request, page_url)

    if request.method == "POST" and request.POST["type"] == "getFeaturedProducts":
        products = product.objects.filter(featured=True)
        array = []
        for i in products:
            print(i.name)
            prod = {"Name":i.name, "Price":i.price,"Quantity":i.quantity, "Category":i.category, "Image":str(i.ig), "id":i.id}
            array.append(prod)
        return JsonResponse({"response":array})

    elif request.method == "POST" and request.POST["type"] == "getProducts":
        products = product.objects.all()
        array = []
        for i in products:
            prod = {"Name":i.name, "Price":i.price,"Quantity":i.quantity, "Category":i.category, "Image":str(i.ig), "id":i.id}
            array.append(prod)
        return JsonResponse({"response":array})

    elif request.method == "POST" and request.POST["type"] == "getCategory":
        category = request.POST["category"]
        products = []
        array = []
        if category == "All":
            products = product.objects.all()
        elif category == "Bars":
            products = product.objects.filter(category="Bars")
        elif category == "Shampoo":
            products = product.objects.filter(category="Shampoo")
        elif category == "LiquidOil":
            products = product.objects.filter(category="Liquid soap")
        elif category == "palm":
             products = product.objects.filter(palm_free=True)
        elif category == "plastic":
            products = product.objects.filter(plastic_free=True)
        elif category == "clear":
            products = product.objects.filter(category="Clear soap")
        elif category == "Lotion":
            products = product.objects.filter(category="Lotion")
        for i in products:
            prod = {"Name":i.name, "Price":i.price,"Quantity":i.quantity, "Category":i.category, "Image":str(i.ig), "id":i.id}
            array.append(prod)
        return JsonResponse({"response":array})
    elif request.method == "POST" and request.POST["type"] == "getProductInfo":
        products = product.objects.filter(id=request.POST["id"])
        array = []
        for i in products:
            prod = {"Name":i.name, "Price":i.price,"Quantity":i.quantity, "Category":i.category, "Image":str(i.ig), "desc":i.description, "id":i.id}
            array.append(prod)
        return JsonResponse({"response":array})
    elif request.method == "POST" and request.POST["type"] == "getCartProducts":
        cart = ast.literal_eval(request.POST["cart"])
        print(cart)
        array = []
        for i in cart:
            print(i)
            item = product.objects.filter(id=i["id"])
            prod = {"Name":item[0].name, "Price":item[0].price,"Quantity":i["quantity"], "Category":item[0].category, "Image":str(item[0].ig), "desc":item[0].description, "id":item[0].id}
            array.append(prod)
        return JsonResponse({"response":array})
    
    elif request.method == "POST" and request.POST["type"] == "searchProducts":
        searchInput = request.POST["search"]
        print(searchInput)
        products = product.objects.all()
        array = []
        for o in products:
            if searchInput in o.name or searchInput in o.description:
                array.append({"name":o.name, "category":o.category, "price":o.price, "image":str(o.ig), "id":o.id})
        return JsonResponse({"response":array})
    
    elif request.method == "POST" and request.POST["type"] == "contactMessage":
        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        to = request.POST["to"]
        Postmessage = request.POST["message"]
        message = "<center style='width:937px;'><img src='http://www.iamsoap.co.za/en/img/i-am-soap-logo-1481117803.jpg'/></center><div style='width:937px; height:auto;background:#80808008;text-align:-webkit-center;text-align:-moz-center;padding:20px;'><p>"+Postmessage+"</p><p><b>Their email address:</b> "+email+"<br><b>Their mobile number:</b> "+mobile+"</p></div>"
        sender = "sales@iamsoap.co.za"
        reciever = ""
        subject = "Message from your website by: "+name+""  
        responseMessage = "Email message has been sent, I am SOAP will soon get back to you." 
        if to == "Customer support":
            reciever = ["neil@iamsoap.co.za"]
        else:
            reciever = ["chjalome@gmail.com"]
        try:
            send_mail(subject,message,sender,reciever,fail_silently=False,html_message=message)
        except:
            responseMessage = "Message could not be sent."
        return JsonResponse({"Message": responseMessage})

def orders(request, orderId):
    pageUrl = 'website/orders.html'
    orderItem = order.objects.filter(id=orderId)
    data = {}
    message ="Order does exist"
    ##if the order does exist get the user's details and the the order details
    if orderItem.exists():
        user_account = userAccount.objects.filter(user=orderItem[0].user)
        ##get the roducts associated with the order
        cart = ast.literal_eval(orderItem[0].products)
        ##check if this has shipping selected
        ##get the cart's total
        total = orderItem[0].total
        shipping = orderItem[0].shipping
        print(user_account)
        data = {"province":user_account[0].Province,"country":user_account[0].Country,"city":user_account[0].city,"street":user_account[0].street_address,"apartment":user_account[0].apartment ,"Email":orderItem[0].user.email,"Date":orderItem[0].date,"Products":orderItem[0].products, "firstname":orderItem[0].user.first_name,"lastname":orderItem[0].user.last_name,"id":orderItem[0].id, "Complete":orderItem[0].complete, "cart": cart, "shipping":shipping,"total":total,"Message":message}
    else:
        message = "The following order with order id: "+orderId+" does not exist in our records"
        data = {"Message":message}
    return render(request,pageUrl, data)

##stockists page
def stockists(request):
    page_url = 'website/stockists.html'
    return render(request,page_url)

def erroPage(request, exception):
    page_url = 'website/404.html'
    return render(request,page_url)