# encoding=utf-8_general_ci

from base import *

class DiscussHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        comments = self.db.query("select * from discuss left join user on user.uid = discuss.uid order by discuss.did desc")
        replies = self.db.query("select * from Reply left join user on user.uid = Reply.uid order by Reply.rid desc")

        for each in comments:
            each.reply = filter(lambda x:x.repuid == each.did, replies)

        self.render("discuss.html", user = self.user, comments = comments)

    def post(self):
        if self.initial() == False:
            return

        method = self.get_argument("method", "")

        if method == "comment":
            content = self.get_argument("content", "")
            if content == "" or len(content) > 5000:
                self.write("Wrong content, empty or too long!")
                return
            content = content.replace("\\", "\\\\");
            content = content.replace("%", "%%");
            self.db.execute("insert into discuss (uid, content) values ('%s', '%s')" % (str(self.user.uid), str(content)))
            self.write("submit success!")
            return

        if method == "reply":
            content = self.get_argument("content", "") 
            if content == "" or len(content) > 255:
                self.write("Wrong content, empty or too long!")
                return
            content = content.replace("%", "%%")
            content = content.replace("\\", "\\\\")
            repuid = self.get_argument("repuid", "")
            try:
                self.db.execute("insert into Reply (repuid,uid,content) values ('%s', '%s', '%s')" % (str(repuid), str(self.user.uid), str(content)))
            except:
                self.write("Data Error")
                return

            self.write("submit success!")
            return

        self.write("method error!")
