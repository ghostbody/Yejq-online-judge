from Queue import Queue
import threading

db_host = "localhost"
db_user = "root"
db_port = 3306
db_password = "yezxcvbnm12"
db_name = "YOJ2"
db_charset = "UTF-8"
queue_size = 100
count_thread = 4

system_data_path = "/home/vinzor/project2/data/"

q = Queue(queue_size)
dblock = threading.Lock()

file_name = {
    "c" : "main.c",
    "c++" : "main.cpp",
    "python2" : "main.py",
    "python3" : "main.py",
    "java" : "main.java",
    "php" : "main.php",
    "ruby" : "main.rb",
    "perl": "main.pl",
    "pascal": "main.pas",
    "go": "main.go",
    "lua": "main.lua",
    "haskell": "main.hs"
}

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
