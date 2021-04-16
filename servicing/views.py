from django.db import connection
from django.shortcuts import render, redirect
import customer.views as customer_view


def load(request):
    if request.session.is_empty():
        print(111111111111111111111)
        return redirect(customer_view.login)
    else:
        if request.method == "POST":
            name = request.POST['name']
            phone_no = request.POST['phone_no']
            imei = request.POST['imei']
            estimated_delivery_date = request.POST['estimated_delivery_date']
            problem_description = request.POST['problem_description']

            employee_id = request.session['employee_id']

            imei_fetched = imei

            # check korbo warranty ase kina

            sql = "select nvl((SP.WARRANTY*30 - (trunc(SYSDATE) - trunc(sa.DATE_OF_SALE))),0) FROM PRODUCT_IMEI I, " \
                  "PRODUCT_SPECIFICATION SP, STOCK S ,SALES sa WHERE I.IMEI_NO = S.STOCK_IMEI AND " \
                  "S.STOCK_PRODUCT_ID = SP.PRODUCT_ID and sa.PRODUCT_IMEI_NO = I.IMEI_NO and I.IMEI_NO = %s;"
            cursor = connection.cursor()
            cursor.execute(sql, [imei_fetched])
            result = cursor.fetchall()
            cursor.close()
            print(type(result))
            print(result)

            rem_warranty_days = result[0][0]

            if rem_warranty_days <= 0:
                # check korbo warranty expired or not eligible

                sql = "select nvl(SP.WARRANTY,%s) FROM PRODUCT_IMEI I, " \
                      "PRODUCT_SPECIFICATION SP, STOCK S WHERE I.IMEI_NO = S.STOCK_IMEI AND " \
                      "S.STOCK_PRODUCT_ID = SP.PRODUCT_ID and I.IMEI_NO = %s;"
                cursor = connection.cursor()
                war = -999
                cursor.execute(sql, [war, imei_fetched])
                result = cursor.fetchall()
                print(result[0][0])
                warranty_param = result[0][0]
                if warranty_param == war:
                    print("Product is not eligible for warranty")
                    message2 = "Product is not eligible for warranty"
                else:
                    print("Waranty on this product is expired")
                    message2 = "Waranty on this product is expired"

                sql = "SELECT IMEI_NO FROM PRODUCT_IMEI WHERE SALE_STATUS='Y' MINUS (select PRODUCT_IMEI_NO from CUSTOMER_SERVICE)"
                cursor = connection.cursor()
                cursor.execute(sql)
                table = cursor.fetchall()
                cursor.close()
                sold_imei = []

                employee_id = request.session['employee_id']

                for i in table:
                    row = {'imei': i[0]}
                    sold_imei.append(row)

                return render(request, "Product_Servicing_Receiving.html",
                              {'message2': message2, 'sold_imei': sold_imei, 'employee_id': employee_id})

            # Jodi database e customer thake , toh new customer entry hobe na :
            sql_0 = "SELECT * FROM CUSTOMERS WHERE NAME = %s AND PHONE_NO = %s"
            cursor = connection.cursor()
            cursor.execute(sql_0, [name, phone_no])
            table = cursor.fetchall()
            cursor.close()

            customer = [row[0] for row in table]
            if not customer:
                print("list is empty , taar maane customer er ager entry nai , new entry banate hobe")
                sql = "INSERT INTO CUSTOMERS(NAME, PHONE_NO ) VALUES(%s, %s)"
                cursor = connection.cursor()
                cursor.execute(sql, [name, phone_no])
                connection.commit()
                cursor.close()
            else:
                print("list faka na , so customer entry laagbe na")

            # ekhn insert korbo .... servicing table e . receiving date pathano hoy nai
            print(estimated_delivery_date)

            sql = "INSERT INTO CUSTOMER_SERVICE(CUSTOMER_ID, PRODUCT_IMEI_NO,DESCRIPTION, EMPLOYEE_ID) " \
                  "VALUES((select CUSTOMER_ID from CUSTOMERS where NAME = %s and PHONE_NO = %s), %s, %s, %s)"

            cursor = connection.cursor()
            print(name, phone_no, imei, problem_description, employee_id)
            cursor.execute(sql, [name, phone_no, imei, problem_description, employee_id])
            connection.commit()
            cursor.close()

            return redirect(load)
        else:
            sql = "SELECT IMEI_NO FROM PRODUCT_IMEI WHERE SALE_STATUS='Y' MINUS (select PRODUCT_IMEI_NO from CUSTOMER_SERVICE)"
            cursor = connection.cursor()
            cursor.execute(sql)
            table = cursor.fetchall()
            cursor.close()
            sold_imei = []

            employee_id = request.session['employee_id']

            for i in table:
                row = {'imei': i[0]}
                sold_imei.append(row)
            
            return render(request, "Product_Servicing_Receiving.html",
                          {'sold_imei': sold_imei, 'employee_id': employee_id})

