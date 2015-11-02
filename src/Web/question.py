# encoding=utf-8_general_ci

from base import *

class QuestionsHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        operation = self.get_argument("operation", "")

        if operation == "getResult":
            runid = self.get_argument("runid", "")
            grade = self.db.get("select grade, remark, report from status where runid='%s'" % str(runid))
            if grade:
                self.write(grade)
            return
        
        query = self.get_argument("query", "")

        if query == "":
            questions =  self.db.query("select problems.pid, problems.title,  problems.difficulty, \
                                    problems.valid, gradeTable.grade, gradeTable.submit from problems \
                                    left join (select pid, sum(grade) as grade , count(*) as submit \
                                    from status group by pid) as gradeTable \
                                    on problems.pid = gradeTable.pid")
            myRecord = self.db.query("select pid, max(grade) as grade from status where uid='%s' group by pid" % str(self.user.uid))
            self.render("question.html", user = self.user, questions = questions, myRecord = myRecord)
            return

        try:
            question = self.db.get("select * from problems \
                                    left join (select pid, sum(grade) as grade , count(*) as submit \
                                    from status group by pid) as gradeTable \
                                    on problems.pid = gradeTable.pid where problems.pid=%s" % str(query))
            question.pid = query
            if question == None:
                question = self.db.get("select * from problems where pid=%s" % str(query))
                question.submit = 0
        except:
            self.render("error.html", message = "no such question!")
            return
        
        if question.valid == 0 and self.user.authority < 3:
            self.render("error.html", message = "Invalid question!")
            return

        theSubmits = self.db.query("select runmem, username, language, runtime, grade, stime from (select user.uid, runtime, runmem, language, grade, stime, user.username, status.pid from status left join user on user.uid = status.uid) as status where status.grade = 100 and status.pid = '%s' group by username order by username" % str(query))

        self.render("question_detail.html", user = self.user, question = question, rank=theSubmits)

    def post(self):
        if self.initial() == False:
            return

        pid = self.get_argument("pid", "")
        code = self.get_argument("code", "")
        language = self.get_argument("language", "")
        operation = self.get_argument("operation", "")

        if pid == "" or code == "":
            return

        question = self.db.get("select * from problems where pid='%s'" % pid)

        sql = "insert into status (pid, uid, language) values ('%s', '%s', '%s')" % (str(pid), str(self.user.uid), str(language))
        
        self.db.execute(sql)

        runid = self.db.get("select runid from status where uid='%s' and pid='%s' order by runid desc limit 1" % (str(self.user.uid), str(pid)))

        submitPath = os.path.join(system_data_path, "submit", str(self.user.uid), str(runid.runid))

        flag = os.system("mkdir " + submitPath)

        f = open(os.path.join(submitPath, file_name[language]), "w")
        f.write(str(code))
        f.close()

        self.db.execute("update status set remark=0 where runid='%s'" % runid.runid)

        self.write(runid)

