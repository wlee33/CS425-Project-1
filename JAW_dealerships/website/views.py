from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import urllib.request
import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from . import forms
from http import cookiejar

import mysql.connector


def homePage(request):
    if (request.method == "GET"):



        if (request.COOKIES.get('auth', False)):

            db = mysql.connector.connect(user='dude', password='CS425',
                                         host='Katie',
                                         database='cars')
            cursor = db.cursor()

            user_type = request.COOKIES['type']
            user_id = request.COOKIES['auth']
            if (user_type == "customer"):
                cursor.execute("SELECT name FROM customers WHERE customerID = " + user_id)
                username = cursor.fetchone()[0]
            if (user_type == "employee"):
                cursor.execute("SELECT name FROM employee WHERE employeeID = " + user_id)
                username = cursor.fetchone()[0]

            cursor.close()
            db.close()

            return render(request, 'index.html', {'username': username, 'user_type': user_type})


        return render(request, 'index.html')
    return HttpResponse("This page doesn't handle post requests")

def login(request):
    db = mysql.connector.connect(user='dude', password='CS425',
                                 host='Katie',
                                 database='cars')
    cursor = db.cursor()

    form = forms.login_form()
    if (request.method == "GET"):
        if (request.COOKIES.get('auth', False)):
            user_id = request.COOKIES['auth']
            user_type = request.COOKIES['type']

            if (user_type == "customer"):
                cursor.execute("SELECT name FROM customers WHERE customerID = " + user_id)
                username = cursor.fetchone()[0]
            if (user_type == "employee"):
                cursor.execute("SELECT name FROM employee WHERE employeeID = " + user_id)
                username = cursor.fetchone()[0]

            message = "you are already logged in"
            return render(request, 'login.html', {'form': form, 'username': username, 'user_type': user_type, 'message': message})
        else:
            return render(request, 'login.html', {'form': form})

    # Creates a new instance of our login_form and gives it our POST data
    f = forms.login_form(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
        # Form was bad -- send them back to login page and show them an error
        return render(request, 'login.html', {'message': 'invalid input', 'form': form})

    # Sanitize username and password fields
    email = f.cleaned_data['email']
    password = f.cleaned_data['password']

    cursor.execute("SELECT customerID FROM customers WHERE email = '" + email + "' and password = '"+password+"'")
    if(cursor.rowcount != 0):
        cust_id = cursor.fetchone()[0]
        response = HttpResponseRedirect('http://localhost:8000/home/')
        response.set_cookie("auth", cust_id)
        #second cookie to designate if a customer or employee is logged in
        response.set_cookie("type", 'customer')

        return response
    else:
        return render(request, 'login.html', {'message': 'email or password is incorrect', 'form': form})

def employee_login(request):
    form = forms.employee_login_form()
    if (request.method == "GET"):
        if (request.COOKIES.get('auth', False)):
            username = "get employee's name from sql query based on cookies"
            user_type = request.COOKIES['type']
            message = "you are already logged in"
            return render(request, 'employee_login.html', {'form': form, 'username': username, 'user_type': user_type, 'message': message})
        else:
            return render(request, 'employee_login.html', {'form': form})

    # Creates a new instance of our login_form and gives it our POST data
    f = forms.employee_login_form(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
        # Form was bad -- send them back to login page and show them an error
        return render(request, 'employee_login.html', {'message': 'invalid input', 'form': form})

    # Sanitize username and password fields
    e_id = f.cleaned_data['e_id']
    password = f.cleaned_data['password']

    # check db with sql query for e_id and password combo
    valid_login = False
    # if valid get cust_id to set auth
    if (valid_login):
        response = HttpResponseRedirect('http://localhost:8000/home/')
        response.set_cookie("auth", e_id)
        # second cookie to designate if a customer or employee is logged in
        response.set_cookie("type", 'employee')
    else:
        return render(request, 'employee_login.html', {'message': 'e_id or password is incorrect', 'form': form})

def logout(request):
    if (request.COOKIES.get('auth', False)):
        #delete logged in cookies return home
        response = HttpResponseRedirect('http://localhost:8000/home/')
        response.delete_cookie('auth')
        response.delete_cookie('type')
        return response
    else:
        return HttpResponseRedirect('http://localhost:8000/home/')

def register(request):
    db = mysql.connector.connect(user='dude', password='CS425',
                                 host='Katie',
                                 database='cars')
    cursor = db.cursor(buffered=True)


    if (request.COOKIES.get('auth', False) and request.method == 'GET'):

        user_type = request.COOKIES['type']
        user_id = request.COOKIES['auth']
        if (user_type == "employee"):
            username = "get employee's name from sql query based on user_id"
        if (user_type == "customer"):
            username = "get cust's name from sql query"

        return render(request, 'register.html',
                      {'message': "you are already logged in", 'username': username, 'user_type': user_type})

    if request.method == 'GET':
        form = forms.register()
        return render(request, 'register.html', {'form': form})

    f = forms.register(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
        # Form was bad -- send them back to login page and show them an error

        form = forms.register()
        return render(request, 'register.html', {'message': 'invalid input', 'form': form})

    email = f.cleaned_data['email']
    password = f.cleaned_data['password']
    lastname = f.cleaned_data['last_name']
    firstname = f.cleaned_data['first_name']
    address = f.cleaned_data['address']
    phone_number = f.cleaned_data['phone_number']
    gender = f.cleaned_data['gender']
    #add field for annual Income

    #check if email is already in use
    valid_email = True
    cursor.execute("SELECT email FROM Customers")
    if (cursor.rowcount != 0):
        result = cursor.fetchall()
        #message = []
        for r in result:
            #message.append(r)
            if r[0] == email:
                valid_email = False

    #for testing return render(request, 'register.html', {'message': message})

    cursor.execute("SELECT customerID FROM Customers")
    if (cursor.rowcount != 0):
        max = 0;
        result = cursor.fetchall()
        for r in result:
            if max < r[0]:
                max = r[0]
        customer_id = max + 1
    else:
        customer_id = 0

    if (not valid_email):

        form = forms.register()

        return render(request, 'register.html', {'message': 'email already in use by another account', 'form': form})

    #otherwise add a sql insert statement here

    insert = "INSERT INTO Customers VALUES(" + str(customer_id) + ",'" + email + "','" + firstname + " " \
             + lastname + "','" + address + "','" + phone_number + "','" + gender + "','" + password + "', 1)"
    cursor.execute(insert)

    response = HttpResponseRedirect('http://localhost:8000/home/')
    response.set_cookie("auth", customer_id)
    response.set_cookie("type", 'customer')

    db.commit()
    cursor.close()
    db.close()
    return response

def edit_account(request):
    if (request.COOKIES.get('auth', False)):

        db = mysql.connector.connect(user='dude', password='CS425',
                                     host='Katie',
                                     database='cars')
        cursor = db.cursor()

        user_type = request.COOKIES['type']
        user_id = request.COOKIES['auth']
        if (user_type == "customer"):
            cursor.execute("SELECT name FROM customers WHERE customerID = " + user_id)
            username = cursor.fetchone()[0]

        else:
            return HttpResponse("this page is for customers")

        cursor.execute("SELECT * FROM customers WHERE customerID = " + user_id)
        cust_data = cursor.fetchone()

        if request.method == 'GET':
            form = forms.register()

            return render(request, 'register.html', {'form': form, 'cust_data': cust_data,'username': username, 'user_type': user_type})

        f = forms.register(request.POST)

        # Check if the form instance is invalid
        if not f.is_valid():
            # Form was bad -- send them back to login page and show them an error

            form = forms.register()
            return render(request, 'edit_account.html', {'message': 'invalid input', 'form': form, 'username': username, 'user_type': user_type})

        if(f.cleaned_data['email'] != ''):
            email = f.cleaned_data['email']
            #add cust data updates
        else:
            email = cust_data[1]
        if (f.cleaned_data['name'] != ''):
            name = f.cleaned_data['name']
        else:
            name = cust_data[2]
        if (f.cleaned_data['address'] != ''):
            address = f.cleaned_data['address']
        else:
            address = cust_data[3]
        if (f.cleaned_data['phone'] != ''):
            phone = f.cleaned_data['phone']
        else:
            phone = cust_data[4]
        if (f.cleaned_data['gender'] != ''):
            gender = f.cleaned_data['gender']
        else:
            gender = cust_data[5]
        if (f.cleaned_data['password'] != ''):
            password = f.cleaned_data['password']
        else:
            password = cust_data[6]
        if (f.cleaned_data['annualIncome'] != ''):
            annualIncome = f.cleaned_data['annualIncome']
        else:
            annualIncome = cust_data[7]

        cursor.execute("UPDATE Customers SET email = '"+email+"', name = '"+name+"', address = '"+address+"', phone = '"+phone+"', gender = '"+gender+"', password = '"+password+"', annualIncome = '"+annualIncome+"' WHERE customerID = " + user_id)

        db.commit()

        #return succesfully updated



    else:
        return HttpResponse("login to view this page")
