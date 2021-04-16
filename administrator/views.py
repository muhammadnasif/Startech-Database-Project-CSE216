import hashlib

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
import customer.views as customer_view


def load(request):
    if request.session.is_empty():
        return redirect(customer_view.login)
    else:
        if request.session['username'] == "cm_abrar":
            return render(request, 'admin_panel.html')
        else:
            return render(request, customer_view.load)


def hire(request):
    if request.session['username'] != "cm_abrar":
        return redirect(customer_view.login)
    else:
        if request.method == "POST":
            name = request.POST['name']
            designation = request.POST['designation']
            salary = request.POST['salary']
            date = request.POST['date']
            password = request.POST['password']
            username = request.POST['username']
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

            sql_2 = "SELECT max(EMPLOYEE_ID) FROM EMPLOYEES;"
            cursor = connection.cursor()
            cursor.execute(sql_2)
            max_id = cursor.fetchall()
            cursor.close()

            cursor = connection.cursor()
            sql_1 = "INSERT INTO EMPLOYEES(EMPLOYEE_ID,NAME, DESIGNATION, SALARY, DATE_OF_JOINING, USERNAME, PASSWORD) VALUES(%s,%s ,  %s, %s, %s, %s, %s)"
            cursor.execute(sql_1, [max_id, name, designation, salary, date, username, hashed_password])
            connection.commit()
            cursor.close()

            return render(request, 'admin_panel.html')
        else:
            return render(request, 'hire.html')


def show_employees(request):
    if request.session['username'] != "cm_abrar":
        return redirect(customer_view.login)
    else:
        if request.method == "POST" and 'Click' in request.POST:
            name = request.POST['name']
            designation = request.POST['designation']
            salary = request.POST['salary']
            date = request.POST['date']
            password = request.POST['password']
            username = request.POST['username']

            #
            branch = request.POST['branch']
            branch_no = branch[len(branch) - 1]
            #
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

            sql_3 = "SELECT max(EMPLOYEE_ID) FROM EMPLOYEES;"
            cursor = connection.cursor()
            cursor.execute(sql_3)
            val = cursor.fetchall()
            cursor.close()

            max_id = [value[0] for value in val]
            max_id = int(max_id[0])

            max_id = max_id + 1

            cursor = connection.cursor()

            # ekhane likhsi0
            if date == "":
                print("date is empty")
                sql_1 = "INSERT INTO EMPLOYEES(EMPLOYEE_ID, NAME, DESIGNATION, SALARY, USERNAME, PASSWORD) VALUES(%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_1, [max_id, name, designation, salary, username, hashed_password])
            else:
                print("date is not empty")
                sql_1 = "INSERT INTO EMPLOYEES(EMPLOYEE_ID, NAME, DESIGNATION, SALARY, DATE_OF_JOINING, USERNAME, PASSWORD) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_1, [max_id, name, designation, salary, date, username, hashed_password])

            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            sql_branch_employee = "INSERT INTO BRANCH_EMPLOYEE(BRANCH_ID, EMPLOYEE_ID) VALUES(%s, %s)"
            cursor.execute(sql_branch_employee, [branch_no, max_id])
            connection.commit()
            cursor.close()

            days = ['SATURDAY', 'SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
            start = '9:00'
            end = '17:00'
            for day in days:
                sql = "INSERT INTO ROSTER(EMPLOYEE_ID, WEEKLY_DAY,START_TIME, END_TIME) values(%s, %s, %s, %s) ;"
                cursor = connection.cursor()
                cursor.execute(sql, [max_id, day, start, end])
                connection.commit()
                cursor.close()

            sql = "select b.WEEKLY_OFFDAY from BRANCH b, BRANCH_EMPLOYEE be where b.BRANCH_ID = be.BRANCH_ID and be.EMPLOYEE_ID = %s;"
            cursor = connection.cursor()
            cursor.execute(sql, [max_id])
            result = cursor.fetchall()
            cursor.close()

            off_day = result[0][0]

            sql = "update ROSTER set START_TIME = %s, END_TIME = %s where EMPLOYEE_ID = %s and WEEKLY_DAY = %s;"
            cursor = connection.cursor()
            cursor.execute(sql, ['Off-day', 'Off-day', max_id, off_day])
            connection.commit()
            cursor.close()



            cursor = connection.cursor()
            sql_2 = "select * from EMPLOYEES e, BRANCH_EMPLOYEE b where e.EMPLOYEE_ID = b.EMPLOYEE_ID  order by e.EMPLOYEE_ID"
            cursor.execute(sql_2)
            table = cursor.fetchall()
            cursor.close()

            result = []
            for i in table:
                id = i[0]
                name = i[1]
                designation = i[2]
                salary = i[3]
                doj = i[4]
                username = i[5]
                branch_id = i[7]
                print(username)
                row = {'name': name, 'designation': designation, 'salary': salary, 'doj': doj, 'username': username,
                       'id': id, 'branch_id': branch_id}
                result.append(row)

            print(66666666666666666666666)
            #
            cursor = connection.cursor()
            sql = "SELECT AREA||' '||BRANCH_ID FROM BRANCH"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            branches = []

            for i in table:
                branch = i[0]
                row = {'branch': branch}
                branches.append(row)

            cursor = connection.cursor()
            sql = "SELECT DESIGNATION FROM DESIGNATION"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            desigs = []

            for i in table:
                desig = i[0]
                row = {'desig': desig}
                desigs.append(row)

            #

            return render(request, 'all_employees.html', {'table': result, 'branches': branches, 'desigs': desigs})


        else:
            cursor = connection.cursor()
            sql = "select * from EMPLOYEES e, BRANCH_EMPLOYEE b where e.EMPLOYEE_ID = b.EMPLOYEE_ID order by e.EMPLOYEE_ID"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            result = []
            for i in table:
                id = i[0]
                name = i[1]
                designation = i[2]
                salary = i[3]
                doj = i[4]
                username = i[5]
                branch_id = i[7]
                row = {'name': name, 'designation': designation, 'salary': salary, 'doj': doj, 'username': username,
                       'id': id, 'branch_id': branch_id}
                result.append(row)
            #
            cursor = connection.cursor()
            sql = "SELECT AREA||' '||BRANCH_ID FROM BRANCH"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            branches = []

            for i in table:
                branch = i[0]
                row = {'branch': branch}
                branches.append(row)
            #

            cursor = connection.cursor()
            sql = "SELECT DESIGNATION FROM DESIGNATION"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            desigs = []

            for i in table:
                desig = i[0]
                row = {'desig': desig}
                desigs.append(row)
            #
            return render(request, 'all_employees.html', {'table': result, 'branches': branches, 'desigs': desigs})


def update_employees(request, id):
    if request.session['username'] != "cm_abrar":
        return redirect(customer_view.login)
    else:
        if request.method == "POST" and 'Click' in request.POST:
            print("ID is : ")
            print(id)
            name = request.POST['name']
            designation = request.POST['designation']
            salary = request.POST['salary']
            password = request.POST['password']
            username = request.POST['username']

            #
            branch = request.POST['branch']
            branch_no = ""
            if branch:
                branch_no = branch[len(branch) - 1]
            #
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

            if not branch_no:
                sql = "SELECT BRANCH_ID FROM BRANCH_EMPLOYEE WHERE EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql, [id])
                result = cursor.fetchall()
                cursor.close()
                name = result[0][0]

            if not name:
                sql = "SELECT NAME FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql, [id])
                result = cursor.fetchall()
                cursor.close()
                name = result[0][0]
            if not designation:
                sql = "SELECT DESIGNATION FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql, [id])
                result = cursor.fetchall()
                cursor.close()
                designation = result[0][0]
            if not salary:
                sql = "SELECT SALARY FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql, [id])
                result = cursor.fetchall()
                cursor.close()
                salary = result[0][0]
            if not password:
                sql = "SELECT PASSWORD FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql, [id])
                result = cursor.fetchall()
                cursor.close()
                hashed_password = result[0][0]
            if not username:
                sql = "SELECT USERNAME FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
                cursor = connection.cursor()
                cursor.execute(sql, [id])
                result = cursor.fetchall()
                cursor.close()
                username = result[0][0]

            cursor = connection.cursor()
            print([name, designation, salary, username, hashed_password, id])

            sql = "UPDATE EMPLOYEES SET NAME = '" + name + "',DESIGNATION = '" + designation + "' ,SALARY = " \
                  + salary + " ,USERNAME='" + username + "' ,PASSWORD='" + hashed_password + "' WHERE EMPLOYEE_ID=" + str(
                id)

            cursor.execute(sql)
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            print(branch_no)
            sql = "UPDATE BRANCH_EMPLOYEE SET BRANCH_ID = %s WHERE EMPLOYEE_ID = %s"
            cursor.execute(sql, [branch_no, id])
            connection.commit()
            cursor.close()
            return redirect(show_employees)

        else:
            sql = "SELECT * FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
            cursor = connection.cursor()
            cursor.execute(sql, [id])
            result = cursor.fetchall()
            name = result[0][1]
            designation = result[0][2]
            salary = result[0][3]
            username = result[0][5]
            cursor.close()

            print(111111111111111)
            cursor = connection.cursor()
            sql = "select * from EMPLOYEES e, BRANCH_EMPLOYEE b where e.EMPLOYEE_ID = b.EMPLOYEE_ID order by e.EMPLOYEE_ID"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            result = []
            for i in table:
                id_1 = i[0]
                name_1 = i[1]
                designation_1 = i[2]
                salary_1 = i[3]
                doj_1 = i[4]
                username_1 = i[5]
                branch_id_1 = i[7]
                row = {'name': name_1, 'designation': designation_1, 'salary': salary_1, 'doj': doj_1, 'username': username_1,
                       'id': id_1, 'branch_id': branch_id_1}
                result.append(row)
            #
            print(222222222222222222)
            cursor = connection.cursor()
            sql = "SELECT AREA||' '||BRANCH_ID FROM BRANCH"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            branches = []

            for i in table:
                branch = i[0]
                row = {'branch': branch}
                branches.append(row)
            #
            print(3333333333333333333)
            cursor = connection.cursor()
            sql = "SELECT DESIGNATION FROM DESIGNATION"
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()

            desigs = []

            for i in table:
                desig = i[0]
                row = {'desig': desig}
                desigs.append(row)
            #
            # sql = "select BRANCH_ID FROM BRANCH B, BRANCH_EMPLOYEE BE WHERE BE.EMPLOYEE_ID = %s"
            # result = cursor.execute(sql,[id])
            # branch
            print(4444444444444444444)
            return render(request, 'update_employees.html',
                    {'name': name, 'designation' : designation, 'salary': salary,'username': username,'table': result, 'branches': branches, 'desigs': desigs})


def sale_status(request):
    if request.session['username'] != "cm_abrar":
        return redirect(customer_view.login)
    else:
        sql = "select sl.EMPLOYEE_ID,(select e.NAME from EMPLOYEES e where e.EMPLOYEE_ID = sl.EMPLOYEE_ID )" \
              " as Name, SUM(sp.PRICE - nvl(sp.BUYING_PRICE,0)) as Profit from SALES sl, STOCK stk, PRODUCT_SPECIFICATION sp" \
              " where sl.PRODUCT_IMEI_NO = stk.STOCK_IMEI and stk.STOCK_PRODUCT_ID = sp.PRODUCT_ID " \
              "group by sl.EMPLOYEE_ID order by (SUM(sp.PRICE - nvl(sp.BUYING_PRICE,0))) DESC"

        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        table = []

        for i in result:
            id = i[0]
            name =  i[1]
            profit = i[2]
            row = {'id':id, 'name':name, 'profit':profit}
            table.append(row)

        return render(request,"sale_status.html", {'table':table})


def employee_report(request, id):
    if request.session['username'] != "cm_abrar":
        return redirect(customer_view.login)
    else:
        employee_id = request.session['employee_id']
        sql = "SELECT * FROM EMPLOYEES WHERE EMPLOYEE_ID = %s"
        cursor = connection.cursor()
        cursor.execute(sql,[employee_id])

        return HttpResponse()