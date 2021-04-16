import hashlib

from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
import sales.views as sales_view
import administrator.views as administrator_view
import servicing.views as servicing_view


# Create your views here.

def load(request):
    print(98798798798987987987)
    if request.method == "POST" and 'search_click' in request.POST:
        text_val = request.POST['search']
        text_val = text_val.lower()
        print(text_val)
        print(123123123123)
        sql = "SELECT * FROM PRODUCT_SPECIFICATION WHERE LOWER(NAME) like '%" + text_val + "%'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result_search = cursor.fetchall()
        cursor.close()
        print(result_search)
        table = []
        for i in result_search:
            product_id = i[0]
            name = i[1]
            type = i[2]
            price = i[3]
            stock = i[4]
            warranty = i[5]
            row = {'product_id': product_id, 'name': name, 'type': type, 'warranty': warranty, 'price': price}
            table.append(row)
        print(table)
        return render(request, 'home.html', {'table': table})
    else:
        print(456456456456)
        cursor = connection.cursor()
        sql = "SELECT * FROM PRODUCT_SPECIFICATION"
        cursor.execute(sql)
        result = cursor.fetchall()

        table = []
        for i in result:
            product_id = i[0]
            name = i[1]
            type = i[2]
            price = i[3]
            warranty = i[5]
            row = {'product_id': product_id, 'name': name, 'type': type, 'price': price, 'warranty': warranty}
            table.append(row)
        flag = 0
        if request.session.is_empty():
            flag = 0
        else:
            logged_user = request.session['username']
            logged_user_type = logged_user[0:5]
            if logged_user_type == "sales":
                flag = 1
            logged_user_type = logged_user[0:9]
            if logged_user_type == "servicing":
                flag = 2
        return render(request, 'home.html', {'table': table, 'flag': flag})


def load_laptop(request):
    cursor = connection.cursor()
    sql = ""  ### sql query to collect all laptop info
    cursor.execute(sql)
    result = cursor.fetchall()

    table = []
    for i in result:
        product_id = i[0]
        name = i[1]
        type = i[2]
        price = i[3]
        warranty = i[5]
        row = {'product_id': product_id, 'name': name, 'type': type, 'price': price, 'warranty': warranty}
        table.append(row)

    return render(request, '', {'table': table})


def load_headphone(request):
    cursor = connection.cursor()
    sql = ""  ### sql query to collect all headphone info
    cursor.execute(sql)
    result = cursor.fetchall()

    table = []
    for i in result:
        product_id = i[0]
        name = i[1]
        type = i[2]
        price = i[3]
        warranty = i[5]
        row = {'product_id': product_id, 'name': name, 'type': type, 'price': price, 'warranty': warranty}
        table.append(row)

    return render(request, '', {'table': table})


def load_mouse(request):
    cursor = connection.cursor()
    sql = ""  ### sql query to collect all mouse info
    cursor.execute(sql)
    result = cursor.fetchall()

    table = []
    for i in result:
        product_id = i[0]
        name = i[1]
        type = i[2]
        price = i[3]
        warranty = i[5]
        row = {'product_id': product_id, 'name': name, 'type': type, 'price': price, 'warranty': warranty}
        table.append(row)

    return render(request, '', {'table': table})


def load_chair(request):
    cursor = connection.cursor()
    sql = ""  ### sql query to collect all mouse info
    cursor.execute(sql)
    result = cursor.fetchall()

    table = []
    for i in result:
        product_id = i[0]
        name = i[1]
        type = i[2]
        price = i[3]
        warranty = i[5]
        row = {'product_id': product_id, 'name': name, 'type': type, 'price': price, 'warranty': warranty}
        table.append(row)

    return render(request, '', {'table': table})


def create_session(request, username):
    request.session['username'] = username
    sql = "SELECT EMPLOYEE_ID FROM EMPLOYEES WHERE USERNAME=%s"

    cursor = connection.cursor()
    cursor.execute(sql, [username])
    result = cursor.fetchall()
    cursor.close()

    employee_id_fetched = [value[0] for value in result]
    employee_id_fetched = int(employee_id_fetched[0])

    request.session['employee_id'] = employee_id_fetched
    request.session['employee_id']
    request.session['logged_once'] = 1
    print(request.session['employee_id'])
    print(type(request.session['employee_id']))


def del_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect(login)


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password_input = request.POST['password']
        hashed_password = hashlib.md5(password_input.encode('utf-8')).hexdigest()

        cursor = connection.cursor()
        sql = "SELECT USERNAME,PASSWORD FROM EMPLOYEES WHERE USERNAME = '" + username + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        username_fetched = ""
        password_fetched = ""

        if cursor.rowcount > 0:
            username_fetched = [value[0] for value in result]
            username_fetched = str(username_fetched[0])

            password_fetched = [value[1] for value in result]
            password_fetched = str(password_fetched[0])
        if username_fetched == username:
            if password_fetched == hashed_password:

                create_session(request, username)
                if username[0:2] == "cm":
                    return redirect(administrator_view.show_employees)
                elif username[0:5] == "sales":
                    return redirect(sales_view.load)
                elif username[0:9] == "servicing":
                    return redirect(servicing_view.load)
            else:
                messages.error(request, 'Wrong Password')
                return render(request, 'login.html')
        else:
            messages.error(request, 'No username exists')
            return render(request, 'login.html')

    else:
        return render(request, "login.html")
