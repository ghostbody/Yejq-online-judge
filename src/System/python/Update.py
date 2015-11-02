import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import torndb
from Config import *
import os
import os.path

def update():
    try:
        db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
    except:
        return

    users = db.query("select * from user")

    for user in users:
        first_sb = db.query("select distinct pid from status where author='"+user.username+"'")
        first_ac = db.query("select distinct pid from status where author='"+user.username+"' and statu='accepted'")
        status = db.query("select pid from status where author='"+user.username+"'")
        db.execute("update user set submit="+str(len(first_sb))+",accepted="+str(len(first_ac)) +",status="+str(len(status))+" where username='"+user.username+"'")
        user_path = os.path.join(system_dir, user.username)
        try:
            os.mkdir(user_path)
        except OSError as e:
            if str(e).find("exist")>0:
                pass
            else:
                return False

    questions = db.query("select * from problems")

    for question in questions:
        accepted = db.query("select * from status where statu='accepted' and pid=" + str(question.pid))
        submit = db.query("select * from status where pid="+str(question.pid))
        db.execute("update problems set submit="+str(len(submit))+",accepted="+str(len(accepted))+" where pid="+str(question.pid))



