import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import torndb
from Config import *

import commands
import time
import os

from Queue import Queue

import lorun
import subprocess

import Update
import Producer
import Worker

import threading

def start_get_task():
    print("start to get task.")
    t = threading.Thread(target=Producer.producer,name=start_get_task)
    t.deamon = True
    t.start()

def start_to_work():
	print("start to work")
    	t1 = threading.Thread(target=Worker.worker,args=("Alice",))
        t2 = threading.Thread(target=Worker.worker,args=("Bob",))
        t3 = threading.Thread(target=Worker.worker,args=("Ken",))
        t4 = threading.Thread(target=Worker.worker,args=("Clare",))
        t1.start()
        t2.start()
        t3.start()
        t4.start()

def check_thread():
    while True:
        try:
            if threading.active_count() < count_thread + 2:
                logging.info("start new thread")
                t = threading.Thread(target=worker)
                t.deamon = True
                t.start()
            time.sleep(1)
        except:
            pass


def start_protect():
    t = threading.Thread(target=check_thread, name="check_thread")
    t.deamon = True
    t.start()

if __name__ == '__main__':
    start_get_task()
    start_to_work()
    start_protect()

