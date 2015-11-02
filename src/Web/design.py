# encoding=utf-8_general_ci
from base import BaseHandler

import os
import json
from config import *

class DesignHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        self.render("design.html", user = self.user)

    def post(self):
        if self.initial() == False:
            return

        if self.user.authority < 2:
            self.render("error.html", error_message = "Permision Denied")

        title = self.get_argument("title", "")
        fromwhere = self.get_argument("fromwhere", "")
        description = self.get_argument("description", "")
        inputoutput = self.get_argument("inputoutput", "")
        source = self.get_argument("source", "")
        difficulty = self.get_argument("difficulty", "")
        timelimit = self.get_argument("timelimit", "")
        memlimit = self.get_argument("memlimit", "")
        
        if title == "" or description == "" or inputoutput == "" or source == "":
            self.render("error.html",  message = "Incomplete Input")
            return

        source = source.replace("%","%%")
        source = source.replace("\\","\\\\")
        description = description.replace("\\", "\\\\")
        score = 0

        try:
            check = json.loads(inputoutput)
            for each in check:
                test_a = each['input']
                test_b = each['output']
                test_c = each['score']
                score += int(test_c)
        except:
            self.render("error.html", message = "Wrong Json Format")
            return

        if score != 100:
            self.render("error.html", message = "Total socre should be 100 pts")
            return


        if timelimit == "":
            timelimit = 1000;
        if memlimit == "":
            memlimit = 32;
        if difficulty == "":
            difficulty = 0.1

        pid = self.db.get("select pid from problems where title='%s'" % title)

        if pid:
            self.render("error.html", message = "Title Duplicated")
            return

        self.db.execute("insert into problems (author,fromwhere,title,description,source,timelimit,memlimit,difficulty, valid) values ('%s','%s','%s','%s','%s','%s','%s','%s',0)" % (str(self.user.username),str(fromwhere),str(title),str(description),str(source), str(timelimit),str(memlimit), str(difficulty)))

        pid = self.db.get("select pid from problems where title='%s'" % title)

        questionPath = os.path.join(system_data_path, "question", str(pid.pid))

        flag = os.system("mkdir " + questionPath)

        f = open(os.path.join(questionPath, str(pid.pid)+".json"), "w")
        f.write(str(inputoutput))
        f.close()

        self.render("error.html", message = "Submit success, wait to be verified!")
