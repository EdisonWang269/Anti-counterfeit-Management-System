from Barcode import Barcode
from Database import Mydb

camera_id = 0
delay = 1

#建立Database物件db，連接資料庫，要填入自己的資訊
host = "127.0.0.16"
user = "root"
password = "root"
database = "project"
db = Mydb(host, user, password, database)

#開啟鏡頭掃描barcode，會回傳字串型態的barcode
barcode = Barcode.scan()

#檢查商家登入帳號是否正確，呼叫login()
db.login("123", "123")

#若是商家登入，則呼叫addMess()
db.addMess(barcode)

#若是使用者掃描barcode，則呼叫showMess()
db.showMess(barcode)
