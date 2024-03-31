import mysql.connector
import time

class Mydb:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    # 檢查登入的帳密是否存在且正確的方法
    def login(self, account, password):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `password` FROM `admin` WHERE `account` = %s", (account,))

        for (db_password,) in cursor:
            if db_password == password:
                return True
            else:
                print("Password error.")
                return False

        print("Account not found.")
        return False
    
    def loginCustomer(self, account, password):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `password` FROM `customer` WHERE `account` = %s", (account,))

        for (db_password,) in cursor:
            if db_password == password:
                return True
            else:
                print("Password error.")
                return False

        print("Account not found.")
        return False

    # 商家用來新增物流資訊，將信息加進資料庫
    def addMess(self, account, barcode):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        cursor.execute("SELECT `company_location`, `company_name` FROM `admin` WHERE account = %s", (account,))
        company_location, company_name = None, None
        for (loc, name) in cursor:
            company_location, company_name = loc, name

        localtime = time.localtime()
        arrive_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

        cursor.execute("INSERT INTO `goods` (barcode, company_name, company_location, arrive_time) VALUES (%s, %s, %s, %s);", (barcode, company_name, company_location, arrive_time))
        conn.commit()

    #用來向消費者展示，將信息從資料庫讀出
    def showMess(self, barcode):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `company_name`, `company_location`, `arrive_time` FROM `goods` WHERE `barcode` = %s", (barcode,))

        results = []
        for (company_name, company_location, arrive_time) in cursor:
            
            results.append({
                'company_name': company_name,
                'company_location': company_location,
                'arrive_time': arrive_time.strftime("%Y-%m-%d %H:%M:%S") if arrive_time else "N/A"
            })

        cursor.close()
        conn.close()

        # 返回JSON格式的數據
        return {'barcode': barcode, 'results': results}

    def save_order(self, account, barcode):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO `order` (account, barcode) VALUES (%s, %s)", (account, barcode))
            conn.commit()
            return {'success': True, 'message': 'Order saved successfully'}
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Error: {err}")
            return {'success': False, 'message': 'Failed to save order'}
        finally:
            cursor.close()
            conn.close()

    def get_orders(self, account):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT barcode FROM `Order` WHERE account = %s", (account,))
            orders = cursor.fetchall() 
            order_details = []

            for order in orders:
                barcode = order[0]
                cursor.execute("SELECT `company_name`, `company_location`, `arrive_time` FROM `goods` WHERE `barcode` = %s", (barcode,))
                details = cursor.fetchall()
                details_list = [{'company_name': detail[0], 'company_location': detail[1], 'arrive_time': detail[2].strftime("%Y-%m-%d %H:%M:%S") if detail[2] else "N/A"} for detail in details]
                order_details.append({'barcode': barcode, 'details': details_list})

            return order_details
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            conn.close()
