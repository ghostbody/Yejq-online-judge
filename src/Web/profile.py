# encoding=utf-8_general_ci

from base import *

class ProfileHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        status_info = self.db.query("select * from status where uid='%s'" % str(self.user.uid))
        status_info.sort(key = lambda statu : statu.stime, reverse = True)

        score = self.db.get("select sum(grade) as score from (select distinct pid, grade from status where uid='%s') as gra" % str(self.user.uid))
        submit = self.db.get("select count(*) as submit from (select distinct pid, grade from status where uid='%s') as gra" % str(self.user.uid))
        status = self.db.get("select count(*) as status from status where uid='%s'" % str(self.user.uid))

        self.user.score = score.score
        self.user.submit = submit.submit
        self.user.status = status.status

        self.render("my.html", user = self.user, message="", status = status_info)

    def post(self):
        if self.initial() == False:
            return
        
        username = self.get_secure_cookie('user')
        
        change = False

        change_password = self.get_argument("new_password", "")
        change_nickname = self.get_argument("new_nickname", "")
        change_email = self.get_argument("new_email", "")
        change_phone = self.get_argument("new_phone", "")


        if change_password != "":
            if len(change_password) < 6:
                self.write("password format error!")
                return
            self.db.execute("update user set password='"+change_password+"' " + "where username='" + username + "'")
            change = True

        if change_email != "":
            if not bool(re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',change_email,flags=0)):
                self.write("email format error!")
                return   
            self.db.execute("update user set email='"+change_email+"' " + "where username='" + username + "'")
            change = True

        if change:
            self.write("profile updated!")
        else:
            self.write("no change!")
