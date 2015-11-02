import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from Config import *
import os
import codecs
import subprocess
import shlex
import lorun
import torndb
import json

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

def judge_main(work_path, pid, language):
    try:
        db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
    except:
        return False
    question_info = db.get("select * from problems where pid=" + str(pid))
    time_limit = question_info.timelimit
    mem_limit = question_info.memlimit
    ## get inputs from file
    f = file(os.path.join(system_data_path, "question", str(pid), str(pid) + ".json"))
    test_cases = json.load(f)
    i = 0
    grade = 0
    timeuse = 0
    memuse = 0
    count = 0
    correct_count = 0
    report = "Running Question Test " + str(pid) + "\n"
    for each_case in test_cases:
        i += 1
        test_input = each_case["input"]
        ##test_output = each_case["output"]
        f_input = codecs.open(os.path.join(work_path, "input.txt"), "w")
        f_input.write(test_input)
        f_input.close()

        input_data = file(os.path.join(work_path, "input.txt"))
        output_data = file(os.path.join(work_path, "output.txt"), "w")

        rst = judge_one(work_path, pid, language, input_data, output_data, time_limit, mem_limit)
        if rst == False:
            report += "(%spts) Fail Case %s: System Error\n" % (str(each_case["score"]), str(i))
        elif rst['result'] == 5:
            report += "(%spts) Fail Case %s: Runtime Error\n" % (str(each_case["score"]), str(i))
        elif rst['result'] == 2:
            report += "(%spts) Fail Case %s: Time Limit Exceeded\n" % (str(each_case["score"]), str(i))
        elif rst['result'] == 3:
            report += "(%spts) Fail Case %s: Memory Limit Exceeded\n" % (str(each_case["score"]), str(i))
        else:
            answer = file(os.path.join(work_path, "output.txt")).read()
            correct = each_case["output"]
            correct = correct.replace('\r', '')
            p_answer = answer.replace('\n', '')
            p_correct = correct.replace('\n', '')

            if correct == answer:
                report += "(%spts) Pass Case %s\n" % (str(each_case["score"]), str(i))
                grade += int(each_case["score"])
                correct_count += 1
            elif p_correct == p_answer:
                report += "(%spts) Fail Case %s: Presentation Error\n" % (str(each_case["score"]), str(i))
            else:
                report += "(%spts) Fail Case %s: Wrong Answer\n" % (str(each_case["score"]), str(i))

            if rst["timeused"]:
                 timeuse += rst["timeused"]
            else:
                 timeuse += 0

            if rst["memoryused"]:
                 memuse += rst["memoryused"]
            else:
            	    memuse += 0

            count+=1

    if count != 0:
        timeuse = timeuse / count
        memuse = memuse / count
    else:
        imeuse = memuse = 0
    
    report += "Total: %s of %s test cases passed\n" % (str(correct_count), str(i))

    return (report, grade, timeuse, memuse)

def judge_one(work_path, pid,language, input_data, output_data, time_limit, mem_limit):
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
        'timelimit': time_limit,
        'memorylimit': mem_limit*1024,
    }

    rst = lorun.run(runcfg)
    
    return rst

def checkStyle(runid, pid, uid, language, real_path):
    if language in ['c', 'c++']:
        p = subprocess.Popen("python %s --filter=-legal/copyright,-whitespace/ending_newline,-whitespace/newline %s" 
                            % (os.path.join(system_data_path, "cpplint.py"), real_path),
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        out, err = p.communicate()
        return err
    return True



def judge(runid, pid, uid, language):
    result = {
        "grade" : "0",
        "runtime" : "0",
        "runmem" : "0",
        "report" : "system error"
    }
    
    work_path = os.path.join(system_data_path, "submit", str(uid), str(runid))
    real_path = os.path.join(work_path, file_name[str(language)])

    flag = check_danger_code(real_path, language)
    if flag == False:
        result["report"] = "restrict function"
        return result

    flag = compile_code(work_path, language)
    if flag != True:
        result["report"] = "compile error\n" + flag
        return result

    ## (report, grade)
    (result["report"], result["grade"], result["runtime"], result["runmem"]) = judge_main(work_path, pid, language)

    flag = checkStyle(runid, pid, uid, language, real_path)
    if flag != True and flag != None:
        gradeM = int(flag.split()[-1])
        print flag
        result["report"] += "Case: Google Style Check -%s" % (gradeM)
        result["report"] += "\n\n===========Google Style Check============\n";
        result["report"] += flag
        result["grade"] = str(int(result["grade"]) - gradeM)


    return result
