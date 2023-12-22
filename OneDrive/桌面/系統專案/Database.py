import mysql.connector
import time

class Mydb:

    #商家輸入的帳密
    userInputAccount = "456"
    userInputPassword = "456"

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    #檢查登入的帳密是否存在且正確的method
    def login(self, account, password):
        conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `account`, `password` FROM `admin`")

        #userInputAccount和userInputPassword是商家輸入的帳密，會拿去資料庫比對是否正確
        for(account, password) in cursor:
            if(account ==Mydb.userInputAccount):
                if(password == Mydb.userInputPassword):
                    return True
                else:
                    print("Password error.")
        return False
    
    #商家用來新增物流資訊，將信息加進資料庫，包含company_name、company_location、arrive_time
    def addMess(self, barcode):
        conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        cursor = conn.cursor()

        cursor.execute("SELECT `company_location`, `company_name` FROM `admin` where account = '{}'".format(
            Mydb.userInputAccount))
        for (company_location, company_name) in cursor:
            self.company_location = company_location
            self.company_name = company_name

        localtime = time.localtime()
        arrive_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

        cursor.execute("INSERT INTO `goods` VALUES ('{}', '{}', '{}', '{}');".format(
            barcode, company_name, company_location, arrive_time
        ))
        conn.commit()

    #用來向消費者展示，將信息從資料庫讀出
    def showMess(self, barcode):
        conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `company_name`, `company_location`, `arrive_time` FROM `goods` where barcode = '{}'".format(
            barcode))
        
        output = "商品編號: " + barcode + "\n" + "經過:\n"
        for(company_name, company_location, arrive_time) in cursor:
            output += company_name + " " + company_location + " " + arrive_time + "\n"

        print(output)