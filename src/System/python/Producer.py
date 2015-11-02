import torndb
import time
from Config import *

def producer():
    while True:
        q.join()
        sql = "select * from status where remark=0"
        db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
        data = db.query(sql)
        
        for each in data:
            q.put(each)

