
import smtplib  
from email.mime.text import MIMEText  


def mailConfirm(href, email):
    sender = 'jerrye17@qq.com'  
    receiver = email
    subject = 'YOJ please confirm your register'  
    smtpserver = 'smtp.qq.com'  
    username = 'jerrye17@qq.com'  
    password = 'yezxcvbnm12'  
      
    msg = MIMEText('<html><h1>Welcome to YOJ</h1>\
                    <p>Please click on the link:</p>\
                    <a href="%s">%s</a></html>' % (str(href), str(href)),'html','utf-8')  
      
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
