## Yejq online judge

Project 当前版本：4.0
运行网站(内网)：http://172.18.215.225:8080/



Run project:

```shell
  sh run.sh
```

### Inspiration

One day, when I am trying my best to solve some problems in sicily(a online judge system of SYSU), I wonder how it works to judge my sumit code to runtime error. And just a few days before, I am helping my classmate to debug, and I wrote some auto-test(a small random test program). And also, I am learning some useful skills in course "Web 2.0 Programming." So, I decided to build a online judge system by myself using the knowledge I have learnt.

### YOJ Targets

How to design a database?
How to analysis a system?
How to use python?
How to use Web technology?
Targets

There are many online judge system in the internet. Some of them are for programming language learning, such as python and c. There are a lot of questions posted on the system and people can upload ther solution to the sytem to judge whether it's right or not. Most ACMer have the experience of these systems.

We are going to build the system step by step.

### Reference

http://www.cnblogs.com/ma6174/archive/2013/05/12/3074034.html

oops: I have consulted a lot of information in the internet and this is a system that most like what in my mind. I try to download the source code of the author but fail to run it. However, the framework of the system design is really good.

### YOJ What to do first?

The system we are going to design will a front-side for the users to browse. In addition to it, the "judgers" will busily run in the backstage. So the most improtant thing to enable the two side to communicate is the database and it's the core part of this project.

Database:

The most popular databse nowadays are Mongodb, Postgresql and MySQL and so on.

Mongodb is a non relational database system. We have used it in Project Activitee. We are not going to use it. Non-Sql is very good to use. But if we use this system, the data module will be very complex. For example:

user: {_id, username, status:[{_id, problem, statu....}]}

It's very complex!

Some one will say we can simplify the object schema. So why don't we use a simple and operational SQL system. So we will use MySQL, because I am familiar with it.

### YOJ requirements:

1. Users. There always should be a user management system in each system. We need simple information form the user when executing register.

2. Questions. OJ system need some questions for user to solve. We need to decribe the quesiton and then give the standar answer(input and output of a program) to test whether the user have solved the quesion or not.

3. Question Submiting. User can submit the question. And judgers will judge the questions.

We will have the following database schema:

USER(uid, authority, username, password, email, register_time)

STATUS(sid, pid, uid, submit_time, code, statu, runtime, runmem, language)

QUESTIONS(pid, uid, title, decription, language, input, output, code, timelimit, memlimit, accepted, submit)

### Framwork

Databse: Mysql libmysql - 5.5.44
Web Framework: Python Tornado 4.1
Backstage: Python + loruner(a project on github)
Optional: Nginx Reverse proxy
Front End

### Requirements

Login and Register: Users can login in the system, the login handler should verify the username and password. Users can also use the register to creat a new account and complete a email verification.

Profile Management: Users can see personal data(accepted questions or etc) here and can modify their profile.

Question List: We can see all the questions in a list.

Question Detail: So the question detail, including memory limit, time limit and so on.

Question Submit: Submit the question to the sytem to judge.

Question Result: Show the result of the judge.

### Backstage

1. Producer and Consumers Model

Multi thread programming:The thread is an entity in the process, and is the basic unit of the system. A process can have multiple threads, a thread must have a parent process, thread itself does not have system resources, only to run some of the data structure, but it can be shared with other threads belonging to a process to have all the resources, a thread can be created and revoked another thread, the same process can be executed between multiple threads.

Producer: Fetch submits from the database to the Server Memory Queue, there are only one Producer.

Consumers.

Consumers: Comsumers are judgers or in other word, workers, that get a question submit from the queue to judge. And muti consumers can work in the same time.

2. How to judge a submit

First, we get the source code from the database, and then save the source code into a local file. Next, we check whether the code is dangerous(contain some restrict functions like IO/System). And then, we will compile the code using the corresponding compiler. Next, run the the programm according to the time limit and memory limit and save the ouput. Last contrast the result with the standar answer.

There are serveral status, 'accepted','run time error','wrong answer','compile error','time limit','memory limit','presentation error','output limit','system error','waiting','compulsory killed','restrict function'.

accepted: The answer is passed.

run time error: Critical error like illegal memory access.

compile error: Syntax error.

time limit: Program running time is too long.

memory limit: Using too much memory.

presentation error: the format of the answer is incorrect.

output limit: the ouput is too long.

system error: the system has some problem.

compulsory killed: the submit is killed by the Administrator.

restrict function: Some restict functions are used such as IO/System.
