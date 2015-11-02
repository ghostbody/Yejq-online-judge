from base import BaseHandler

from config import *
import os
import codecs
import subprocess
import shlex
import lorun
import torndb
import json
import time


compile_command = {
    "c": "gcc main.c -W -std=c99 -o main",
    "c++": "g++ main.cpp -W -o main",
    "java": "javac main.java",
    "php" : "php -l main.php",
    "ruby": "ruby -c main.rb",
    "perl": "perl -c main.pl",
    "pascal": 'fpc main.pas -O2 -Co -Ct -Ci',
    "go": 'go build main.go',
    "lua": 'luac -o main main.lua',
    "python2": 'python2 -m py_compile main.py',
    "python3": 'python3 -m py_compile main.py',
    "haskell": "ghc -o main main.hs",
}

def run(work_path, language, input_data, output_data):
    if language == 'c' or language == 'c++':
        main_exe = [os.path.join(work_path, 'main'), ]
    elif language == 'python2':
        cmd = 'python2 %s' % (os.path.join(work_path,'main.pyc'))
        main_exe = shlex.split(cmd)
    elif language == 'python3':
        cmd = 'python3 %s' % (os.path.join(work_path,'__pycache__/main.cpython-34.pyc'))
        main_exe = shlex.split(cmd)
    elif language == 'java':
        cmd = 'java -cp %s main' % work_path
        main_exe = shlex.split(cmd)
    elif language == 'php':
        cmd = 'php %s' % (os.path.join(work_path,'main.php'))
        main_exe = shlex.split(cmd)
    elif language == 'lua':
        cmd = "lua %s" % (os.path.join(work_path,"main"))
        main_exe = shlex.split(cmd)
    elif language == "ruby":
        cmd = "ruby %s" % (os.path.join(work_path,"main.rb"))
        main_exe = shlex.split(cmd)
    elif language == "perl":
        cmd = "perl %s" % (os.path.join(work_path,"main.pl"))
        main_exe = shlex.split(cmd)
    else:
        main_exe = [os.path.join(work_path, 'main'), ]

    runcfg = {
        'args': main_exe,
        'fd_in': input_data.fileno(),
        'fd_out': output_data.fileno(),
        'timelimit': 1000,
        'memorylimit': 32*1024,
    }

    rst = lorun.run(runcfg)
    
    return rst

def check_danger_code(real_path, language):
    if language in ['python2', 'python3']:
        code = file(real_path).readlines()
        support_modules = [
            're',
            'sys',
            'string',
            'scanf',
            'math',
            'cmath',
            'decimal',
            'numbers',
            'fractions',
            'random',
            'itertools',
            'functools',
            'operator',
            'readline',
            'json',
            'array',
            'sets',
            'queue',
            'types',
            ]
        for line in code:
            if line.find('open') >= 0:
                return False
            if line.find('file') >= 0:
                return False
            if line.find('import') >= 0:
                words = line.split()
                tag = 0
                for w in words:
                    if w in support_modules:
                        tag = 1
                        break
                if tag == 0:
                    return False
        return True
    if language in ['c', 'c++']:
        try:
            code = file(real_path).read()
        except:
            code = file(real_path).read()
        if code.find('system') >= 0:
            return False
        if code.find('FILE') >= 0:
            return False
        if code.find('fstream') >= 0:
            return False
        return True
    if language == 'go':
        code = file(real_path).read()
        danger_package = [
            'os', 'path', 'net', 'sql', 'syslog', 'http', 'mail', 'rpc', 'smtp', 'exec', 'user',
        ]
        for item in danger_package:
            if code.find('"%s"' % item) >= 0:
                return False
        return True


def compile_code(work_path, language):
    p = subprocess.Popen(
        compile_command[language],
        shell=True,
        cwd=work_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode == 0:
        return True
    else:
        return err;
        

class CompilerHandler(BaseHandler):
    def get(self):
        if self.initial() == False:
            return
        self.render("compiler.html", user = self.user)

    def post(self):
        if self.initial() == False:
            return

        code = self.get_argument("code", "")
        theInput = self.get_argument("input", "")
        language = self.get_argument("language", "")

        self.db.execute("insert into compiler (uid) values (%s)" % str(self.user.uid))

        work_path = os.path.join(system_data_path, "compiler", str(self.user.uid))
        real_path = os.path.join(work_path, file_name[str(language)])

        os.system("rm -f " + work_path + "/*")

        f = open(real_path, "w")
        f.write(code)
        f.close()
        
        result = self.compiler(work_path,real_path, language)

        if result != True:
            self.write(result)
            return

        inputFile = open(os.path.join(work_path, "input.txt"), "w")
        inputFile.write(theInput);
        inputFile.close()

        input_data = file(os.path.join(work_path, "input.txt"))
        output_data = file(os.path.join(work_path, "output.txt"), "w")

        rst = run(os.path.join(system_data_path, "compiler", str(self.user.uid)), language, input_data, output_data)

        if rst == False:
           self.write("System Error!")
           return
        elif rst['result'] == 5:
            self.write("Runtime Error!")
            return
        elif rst['result'] == 2:
            self.write("Time limit Exceeded")
            return
        elif rst['result'] == 3:
            self.write("Memory limit Exceeded")
            return

        result = file(os.path.join(work_path, "output.txt")).read()

        p = subprocess.Popen("python %s --filter=-legal/copyright %s" 
                                % (os.path.join(system_data_path, "cpplint.py"), real_path),
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        out, err = p.communicate()

        result += "\n\n============================\n";

        result += err

        self.write(result)
        
        return

    def compiler(self, work_path, real_path, language):

        flag = check_danger_code(real_path, language)
        if flag == False:
            return "restrict function"
        flag = compile_code(work_path, language)
        if flag != True:
            return "compile error\n" + flag
        return True

