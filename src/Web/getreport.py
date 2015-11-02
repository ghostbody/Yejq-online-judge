# encoding=utf-8_general_ci

from base import *

class getreportHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        runid = self.get_argument("runid", "")
        report = self.db.get("select report, uid from status where runid=%s"\
                        % str(runid))

        if(report.uid == self.user.uid or self.user.authority >= 3):
            self.write(report["report"])
        else:
            self.write("you can not acess the report")
