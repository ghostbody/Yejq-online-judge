# encoding=utf-8_general_ci
from base import *

class AdminHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        if self.user.authority < 3:
            self.render("error.html", message = "Permission denied!")
            return

        status = self.db.query("select * from status left join user on user.uid = status.uid order by status.runid desc")
        questions = self.db.query("select problems.pid, problems.title,  problems.difficulty, \
                                    problems.valid, gradeTable.grade, gradeTable.submit from problems \
                                    left join (select pid, sum(grade) as grade , count(*) as submit \
                                    from status group by pid) as gradeTable \
                                    on problems.pid = gradeTable.pid")
        users = self.db.query("select * from user")

        self.render("admin.html", user = self.user, status = status, users = users, questions = questions)

class AdminOperationHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        if self.user.authority < 3:
            self.render("error.html", message = "Permission denied!")
            return

        operation = self.get_argument("operation", "")
        runid = self.get_argument("runid", "")
        pid = self.get_argument("pid", "")
        uid = self.get_argument("uid", "")

        if operation == "rejudge":
            self.db.execute("update status set remark=0 where runid='" + str(runid) + "'") 
        elif operation == "kill":
            self.db.execute("update status set remark=1, grade = 0,report='killed by admin' where runid='" + str(runid) + "'")
        elif operation == "validate":
            self.db.execute("update problems set valid=1 where pid="+str(pid))
        elif operation == "invalidate":
            self.db.execute("update problems set valid=0 where pid="+str(pid))
        elif operation == "uservalidate":
            self.db.execute("update user set authority=1 where uid="+str(uid))
        elif operation == "userinvalidate":
            self.db.execute("update user set authority=0 where uid="+str(uid))

