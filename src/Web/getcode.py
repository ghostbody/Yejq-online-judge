# encoding=utf-8_general_ci

from base import *

class getcodeHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return

        runid = self.get_argument("runid", "")
        language = self.get_argument("language", "")
        uid = self.get_argument("uid", "")

        if(int(uid) != self.user.uid and self.user.authority < 3):
            self.write("read code error!")
            return

        
        codePath = os.path.join(system_data_path, "submit", str(uid), str(runid), file_name[language])

        try:
            code = file(codePath).read()
        except Exception, e:
            self.write("read code error!")
            return

        self.write(code)
