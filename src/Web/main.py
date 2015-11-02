# encoding=utf-8_general_ci

from base import *

class MainHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        status_info = self.db.query("select * from status order by runid desc limit 50")
        submit_num = self.db.query("select count(*) from status")

        self.render(
                "main.html",
                user = self.user,
                message = "",
                status = status_info,
                judge_worker_num = 4,
                submit_num = submit_num[0]["count(*)"]
            )
