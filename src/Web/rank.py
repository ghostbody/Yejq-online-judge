# encoding=utf-8_general_ci

from base import BaseHandler

def cmp(user1, user2):
    if user1.grade > user2.grade:
    	return 1
    if user2.grade > user1.grade:
    	return -1
    if user1.submit < user2.submit:
    	return 1
    if user2.submit < user1.submit:
    	return -1
    else:
    	return 0

class RankHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        users = self.db.query("select user.username, Table1.uid,submit,grade from (select uid, sum(grade) as grade from (select pid, uid, max(grade) as grade from status group by pid,uid) as gradeTable group by uid) as Table1, (select uid, count(*) as submit from status group by uid) as Table2, user where Table1.uid=Table2.uid and Table1.uid=user.uid")

        users.sort(cmp=cmp, reverse = True)

        self.render("rank.html", user = self.user, users = users)
