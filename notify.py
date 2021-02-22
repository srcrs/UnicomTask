import smtplib,traceback,os,requests
from email.mime.text import MIMEText

def readFile(filepath):
    with open(filepath,'r',encoding='UTF-8') as fp:
        content=fp.read()
    return content

#邮件推送api来自流星云
def sendEmail():
    #要发送邮件内容
    content = readFile('log.txt')
    #接收方邮箱
    receivers = os.environ.get('EMAIL_COVER')
    #邮件主题
    subject = 'UnicomTask每日报表'
    param = '?address=' + receivers + '&name=' + subject + '&certno=' + content
    res = requests.get('http://liuxingw.com/api/mail/api.php' + param)
    res.encoding = 'utf-8'
    res = res.json()
    print(res['msg'])

#钉钉群自定义机器人推送
def sendDing():
    #要发送邮件内容
    content = readFile('log.txt')
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'UnicomTask每日报表',
            'text': content
        }
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    res = requests.post(os.environ.get('DINGTALK_WEBHOOK'),headers=headers,json=data)
    res.encoding = 'utf-8'
    res = res.json()
    if res['errcode'] == '0':
        print('dinngTalk push success')
    else:
        print('dinngTalk push error : ' + res['errmsg'])


'''
#参考自文章 https://zhuanlan.zhihu.com/p/24180606 用python发送邮件
def sendEmail():
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = 'bot2021' 
    #密码(部分邮箱为授权码) 
    mail_pass = 'KXEXSFCZWFEIASLE'   
    #邮件发送方邮箱地址
    sender = 'bot2021@163.com'  
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [os.environ.get('EMAIL_COVER')]  
    
    #设置email信息
    #要发送的邮件内容
    basename = os.path.basename("log.txt")
    content = readFile('log.txt')
    #邮件内容设置
    message = MIMEText(content,'html','utf-8')
    #邮件主题       
    message['Subject'] = 'UnicomTask每日报表' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  
    
    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('email push success')
    except smtplib.SMTPException as e:
        print('email push error')
        print(traceback.format_exc())
'''