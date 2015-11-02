import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import torndb
from Judge import judge
from Config import *
import time

def update_result(result, runid):
    try:
        db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
    except:
        pass
    if result["runtime"] == None:
        result["runtime"] = "0"
    if result["runmem"] == None:
        result["runmem"] = "0"

    report = result["report"];
    report = report.replace("%", "%%")
    report = report.replace("\\", "\\\\")
    report = report.replace("'", "''")

    sql = "update status set report='%s',grade='%s',remark=1,runtime='%s',runmem='%s' where runid=%s" % (str(report), str(result["grade"]), str(result["runtime"]), str(result["runmem"]), str(runid))
    
    dblock.acquire()
    db.execute(sql)
    dblock.release()

def worker(workerId):
    print("\033[32m[%s]\033[0m %s : %s" % (time.ctime(time.time()), workerId, " worker online"))
    while True:
        task = q.get()
        print("\033[32m[%s]\033[0m %s : %s" % (time.ctime(time.time()), workerId, "get a task"))
        runid = task.runid
        uid = task.uid
        pid = task.pid
        language = task.language

        result = judge(runid, pid, uid, language)

        if result == False:
            continue      
        
        update_result(result, runid)
        print("\033[32m[%s]\033[0m %s : %s" % (time.ctime(time.time()), workerId, "grade task "+str(runid)))

        q.task_done()

        #time.sleep(1)
