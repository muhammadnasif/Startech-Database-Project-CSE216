import hashlib

from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
import customer.views as customer_view

# Create your views here.


def load(request):
    if request.session.is_empty():
        print(111111111111111111111)
        return redirect(customer_view.login)
    else:
        if request.method == "POST":
            imei = request.POST['imei']
            date_of_sell = request.POST['date_of_sell']
            name = request.POST['name']
            phone_no = request.POST['phone_no']
            area = request.POST['area']
            postal_code = request.POST['postal_code']
            district = request.POST['district']
            # add kora
            employee_id = request.session['employee_id']
            # add kora end

            # Jodi database e customer thake , toh new customer entry hobe na :
            sql_0 = "SELECT * FROM CUSTOMERS WHERE NAME = %s AND PHONE_NO = %s"
            cursor = connection.cursor()
            cursor.execute(sql_0, [name, phone_no])
            table = cursor.fetchall()
            cursor.close()

            customer = [row[0] for row in table]
            if not customer:
                print("list is empty , taar maane customer er ager entry nai , new entry banate hobe")
                sql = "INSERT INTO CUSTOMERS(NAME, PHONE_NO, AREA, POSTAL_CODE, DISTRICT) VALUES(%s, %s, %s, %s, %s)"
                cursor = connection.cursor()
                cursor.execute(sql, [name, phone_no, area, postal_code, district])
                connection.commit()
                cursor.close()
            else:
                print("list faka na , so customer entry laagbe na")

            sql_2 = "UPDATE PRODUCT_IMEI SET SALE_STATUS = %s WHERE IMEI_NO = %s"
            cursor = connection.cursor()
            cursor.execute(sql_2, ['Y', imei])
            connection.commit()
            cursor.close()

            sql_3 = "SELECT IMEI_NO FROM PRODUCT_IMEI WHERE SALE_STATUS='N'"
            cursor = connection.cursor()
            cursor.execute(sql_3)
            table = cursor.fetchall()
            cursor.close()
            available_imei = []

            for i in table:
                row = {'imei': i[0]}
                available_imei.append(row)

            # ekhane sale table update korbo

            sql_customer = "SELECT CUSTOMER_ID FROM CUSTOMERS WHERE NAME = %s and PHONE_NO= %s"
            cursor = connection.cursor()
            cursor.execute(sql_customer, [name, phone_no])
            customer_ids = cursor.fetchall()

            customer_id_fetched = [customer_id[0] for customer_id in customer_ids]
            customer_id_fetched = str(customer_id_fetched[0])

            cursor.close()

            cursor = connection.cursor()
            cursor.callproc('insert_sale', [customer_id_fetched, imei, date_of_sell, employee_id])

            # if not date_of_sell:
            #     print("XDXDXDXDXDXDXDXDXDXDXDXDXDX")
            #     sql_4 = "INSERT INTO SALES(CUSTOMER_ID,PRODUCT_IMEI_NO,EMPLOYEE_ID) VALUES(%s,%s,%s);"
            #     cursor.execute(sql_4, [customer_id_fetched, imei, employee_id])
            #
            # else:
            #     sql_4 = "INSERT INTO SALES(CUSTOMER_ID,PRODUCT_IMEI_NO,DATE_OF_SALE,EMPLOYEE_ID) VALUES(%s,%s,%s,%s);"
            #     cursor.execute(sql_4, [customer_id_fetched, imei, date_of_sell, employee_id])

            connection.commit()
            cursor.close()

            # my code ends

            messages.info(request,'Product Sold Successfully')

            return render(request, 'data_entry.html', {'available_imei': available_imei, 'employee_id':employee_id})

        else:

            sql = "SELECT IMEI_NO FROM PRODUCT_IMEI WHERE SALE_STATUS='N'"
            cursor = connection.cursor()
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()
            available_imei = []

            employee_id = request.session['employee_id']
            print(98989898)
            print(employee_id)
            for i in table:
                row = {'imei': i[0]}
                available_imei.append(row)

            employee_id = request.session['employee_id']
            sql_5 = "select NAME from EMPLOYEES where EMPLOYEE_ID=%s"
            cursor = connection.cursor()
            cursor.execute(sql_5, [employee_id])
            result = cursor.fetchall()
            emp_name = result[0][0]

            logged_flag = 0
            if request.session['logged_once'] == 1:
                logged_flag = request.session['logged_once']
                request.session['logged_once'] = 0

            return render(request, 'data_entry.html', {'available_imei': available_imei, 'employee_id':employee_id,'logged_flag':logged_flag})


def product_info(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
    else:
        if request.method == "POST":
            product_name = request.POST['product_name']
            description = request.POST['description']
            price = request.POST['price']
            warranty = request.POST['warranty']
            total_product = request.POST['total_product']
            dict = {'product_name':product_name, 'description':description, 'price':price, 'warranty':warranty, 'total_product':total_product}

            cursor = connection.cursor()
            sql = "INSERT INTO HISTORY(NAME, STOCK, PRICE, DESCRIPTION, WARRANTY) " \
                  "VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(sql, [product_name, total_product, price, description, warranty])
            connection.commit()
            cursor.close()
            return redirect(imei_entry_load)
        else:
            return render(request, "Product_Info.html")

def imei_entry_load(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
        #return render(request, 'login.html')
    else:
        if request.method == "POST" and 'add_imei' in request.POST:
            imei = int(request.POST['imei_value'])
            sql = "INSERT INTO TEMP_IMEI(IMEI) VALUES(%s)"
            cursor = connection.cursor()
            cursor.execute(sql,[imei])
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            sql_1 = "SELECT * FROM TEMP_IMEI"
            sql_2 = "SELECT COUNT(*) FROM TEMP_IMEI"
            sql_3 = "select * from history where history_id = (select max(history_id) from history)"

            cursor.execute(sql_1)
            table = cursor.fetchall()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute(sql_2)
            total_count = cursor.fetchall()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute(sql_3)
            dict = cursor.fetchall()

            print(dict)

            cursor.close()

            remaining = 0

            result = []
            for i in table:
                row = {'imei': i[0]}
                result.append(row)

            for i in dict:
                remaining = i[4]


            remaining = int(remaining)
            temp = [value[0] for value in total_count]
            total_value = temp[0]
            total_value = int(total_value)

            remaining = remaining - total_value

            return render(request, "imei_entry.html", {'table': result, 'remaining':remaining, 'total_value':total_value})
        else:
            cursor = connection.cursor()
            sql_1 = "SELECT * FROM TEMP_IMEI"
            sql_2 = "SELECT COUNT(*) FROM TEMP_IMEI"
            sql_3 = "select * from history where history_id = (select max(history_id) from history)"

            cursor.execute(sql_1)
            table = cursor.fetchall()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute(sql_2)
            total_count = cursor.fetchall()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute(sql_3)
            dict = cursor.fetchall()
            cursor.close()

            remaining = 0

            result = []
            for i in table:
                row = {'imei': i[0]}
                result.append(row)

            for i in dict:
                remaining = i[4]

            remaining = int(remaining)

            temp = [value[0] for value in total_count]
            total_value = temp[0]

            total_value = int(total_value)

            remaining = remaining - total_value

            return render(request, "imei_entry.html", {'table': result, 'remaining':remaining, 'total_value':total_value})


def submit_imei(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
    else:


        sql_1 = "select * from history where history_id = (select max(history_id) from history)"
        sql_2 = "SELECT IMEI FROM TEMP_IMEI"
        sql_3 = "INSERT INTO STOCK(STOCK_PRODUCT_ID, STOCK_IMEI) VALUES(%s, %s)"
        sql_4 = "INSERT INTO PRODUCT_SPECIFICATION(PRODUCT_ID, NAME, DESCRIPTION, PRICE, STOCK, WARRANTY) VALUES(%s, %s, %s, %s, %s, %s)"
        sql_5 = "INSERT INTO PRODUCT_IMEI(IMEI_NO) VALUES(%s)"
        sql_6 = "DELETE FROM TEMP_IMEI"

        cursor = connection.cursor()
        cursor.execute(sql_1)
        result_fetched_1 = cursor.fetchall()
        cursor.close()
        history_id = -1
        product_name = ""
        total_product = -1
        price = 0
        description = ""
        warranty = 0
        for i in result_fetched_1:
            history_id = i[0]
            product_name = i[1]
            description = i[2]
            price = i[3]
            total_product = i[4]
            warranty = i[5]

        cursor = connection.cursor()
        cursor.execute(sql_2)
        result_fetched_2 = cursor.fetchall()
        cursor.close()

        imei_table=[]
        for i in result_fetched_2:
            imei_table.append(i[0])

        print(imei_table)
        for data in imei_table:
            print(data)
        cursor = connection.cursor()

        for data in imei_table:
            cursor.execute(sql_5,[data])
            connection.commit()

        #cursor.execute(sql_4, [history_id, product_name, description, price, total_product, warranty])
        cursor.close()

        cursor = connection.cursor()
        sql_product_check = "select * from PRODUCT_SPECIFICATION WHERE NAME=%s AND DESCRIPTION=%s"
        cursor.execute(sql_product_check, [product_name, description])
        product = cursor.fetchall()
        cursor.close()

        # product = [row[0] for row in products]

        if not product:
            print("product list khali . so product spec table e insert hobe new row")
            cursor = connection.cursor()
            cursor.execute(sql_4, [history_id, product_name, description, price, total_product, warranty])
            connection.commit()
            cursor.close()

        else:
            print("product list e ase, so spec table e just update hobe")
            print(type(product[0]))
            print("product print hoy")
            print(product[0])
            spec_id = int(product[0][0])
            history_id = spec_id
            stock = int(product[0][4]) + int(total_product)
            cursor = connection.cursor()
            sql_update = "UPDATE PRODUCT_SPECIFICATION SET PRICE = %s, STOCK = %s, WARRANTY = %s WHERE PRODUCT_ID = %s"
            cursor.execute(sql_update, [price, stock, warranty, spec_id])
            connection.commit()
            cursor.close()
        employee_id = request.session['employee_id']

        sql = "SELECT BRANCH_ID FROM BRANCH_EMPLOYEE WHERE EMPLOYEE_ID = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])
        result = cursor.fetchall()
        branch_id = result[0][0]
        cursor.close()
        cursor = connection.cursor()

        for data in imei_table:
            cursor.callproc('insert_into_stock', [history_id, data])
            # cursor.execute(sql_3, [history_id, data])
            cursor.callproc('insert_into_branch_stock', [branch_id, data])

            # cursor.execute(sql_7, [branch_id, data])
            connection.commit()

        cursor.execute(sql_6)
        connection.close()
        messages.info(request, "Stock added successfully")
        return redirect(load)

def check_stock(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
    else:
        if request.method == 'POST':

            product_id = request.POST['product_id']

            sql = "select (B.AREA ||' '||B.BRANCH_ID) AS branch , count(B.BRANCH_ID) as stock " \
                  "from PRODUCT_SPECIFICATION SP, STOCK STK, PRODUCT_IMEI I, BRANCH_PRODUCT_STOCK BP, BRANCH B " \
                  "where SP.PRODUCT_ID = STK.STOCK_PRODUCT_ID AND STK.STOCK_IMEI = I.IMEI_NO " \
                  "AND I.IMEI_NO = BP.STOCK_IMEI AND BP.STOCK_BRANCH_ID = B.BRANCH_ID AND SP.PRODUCT_ID = %s " \
                  "group by (B.AREA ||' '||B.BRANCH_ID)"

            cursor = connection.cursor()
            cursor.execute(sql,[product_id])
            result = cursor.fetchall()
            table = []
            if not result:
                messages.warning(request, 'This product is not available')
                return render(request,'check_stock.html')
            else:
                for i in result:
                    branch = i[0]
                    stock = i[1]
                    row = {'branch': branch, 'stock': stock}
                    table.append(row)

                print("printing table.........")
                print(table)

                sql_1 = "select NAME from PRODUCT_SPECIFICATION where PRODUCT_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql_1, [product_id])
                result_1 = cursor.fetchall()

                name = result_1[0][0]

                return render(request, "check_stock.html", {'available_stock': table, 'product_name': name})

        else:
            return render(request, "check_stock.html")

def sales_representative_status(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
    else:
        sql = "SELECT * FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
        sql_1 = "select employee_profit(EMPLOYEE_ID) from EMPLOYEES where  EMPLOYEE_ID=%s "
        employee_id = request.session['employee_id']

        cursor = connection.cursor()
        cursor.execute(sql,[employee_id])
        result = cursor.fetchall()
        cursor.close()
        emp_info = []

        cursor = connection.cursor()
        cursor.execute(sql_1, [employee_id])
        result_1 = cursor.fetchall()
        cursor.close()

        profit = result_1[0][0]

        for i in result:
            name = i[1]
            designation = i[2]
            salary = i[3]
            emp_id = employee_id
            row = {'name':name,'designation':designation,'salary':salary,'emp_id':emp_id,'profit':profit}
            emp_info.append(row)

        print(emp_info)
        flag = 0
        designation = request.session['username']
        if designation[0:5] == "sales":
            flag = 1
        else:
            flag = 0
        sql = "SELECT WEEKlY_DAY, START_TIME, END_TIME FROM ROSTER WHERE EMPLOYEE_ID = %s;"
        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])
        result = cursor.fetchall()
        cursor.close()
        table = []

        for data in result:
            row = {'day': data[0], 'start_time': data[1], 'end_time': data[2]}
            table.append(row)

        return render(request, 'sales_representative_status.html', {'emp_info': emp_info, 'flag': flag, 'table': table})


def change_info(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
    else:
        if request.method == "POST":
            id = request.session['employee_id']
            name = request.POST['name']
            username = request.POST['username']
            password_1 = request.POST['password_1']
            password_2 = request.POST['password_2']

            if password_1 != password_2:
                messages.warning(request,"Password does not match")
                print("ALERTTTTTTTTTTTTTTTTTTTTTTT")
                return redirect(change_info)
            else:
                hashed_password = hashlib.md5(password_1.encode('utf-8')).hexdigest()
                sql_1 = "update EMPLOYEES set NAME = %s, USERNAME = %s, PASSWORD =%s where EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql_1, [name, username, hashed_password, id])
                connection.commit()
                cursor.close()
                return redirect(sales_representative_status)
        else:
            employee_id = request.session['employee_id']
            sql = "SELECT * FROM EMPLOYEES WHERE EMPLOYEE_ID=%s"
            cursor = connection.cursor()
            cursor.execute(sql, [employee_id])
            result = cursor.fetchall()
            name = result[0][1]
            username = result[0][5]

            return render(request, 'change_employee_info.html', {'name': name, 'username': username})