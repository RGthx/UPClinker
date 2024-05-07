# coding=utf-8
# Author: RGthx
# Python version: 3.11
# ---------------------------------------------------------------------------



import os
import sys
import socket
import urllib.request
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

# ---------------------------Global-Variable--------------------------------------------
## request data
url = 'http://wlan.upc.edu.cn'
refUrl = ''
loginUrl = 'http://wlan.upc.edu.cn/eportal/InterFace.do?method=login'
hostIP = ''
reqHeader = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
             'Connection': 'Keep-Alive',
             'Host': 'wlan.upc.edu.cn',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
             }
postHeader = {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Cache-Control': 'no-cache',
              'Connection': 'Keep-Alive',
              'Content-Length': '339',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'Host': 'wlan.upc.edu.cn',
              'Origin': 'http://wlan.upc.edu.cn',
              'Pragma': 'no-cache',
              'Referer': '',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
              }
postData = {'userId': '',
            'password': '',
            'service': '',
            'queryString': '',
            'operatorPwd': '',
            'operatorUserId': '',
            'validcode': '',
            'passwordEncrypt': 'false'
            }

# -----------Recipient Class Define-----------------
class recipient:
    def __init__(self, name, mail):
        self.userName = name
        self.userMail = [mail]

    def Send(self):
        global hostIP
        global senderMail
        global senderPwd
        global senderServer
        global senderPort
        global mailMsgTemp
        global mailSubject
        mail = MIMEText(mailMsgTemp.format(name=self.userName, ip=hostIP), 'plain', 'utf-8')
        mail['from'] = senderMail
        mail['to'] = self.userMail[0]
        mail['subject'] = Header(mailSubject, 'utf-8')
        # --try-send-mail--
        smtpObj = smtplib.SMTP(senderServer, senderPort)
        # smtpObj.helo()
        # smtpObj.starttls()
        smtpObj.login(senderMail, senderPwd)
        smtpObj.sendmail(senderMail, self.userMail[0], mail.as_string())
        smtpObj.quit()
        return


# ---------Check Login Status-----------------------
def CheckLoginStatus(url):
    global reqHeader
    req = urllib.request.Request(url, headers=reqHeader)
    try:
        response = urllib.request.urlopen(req, timeout = 4)
    except Exception:
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(localTime + ' :Can not open ' + url)
        exit(0)
    else:
        if 'success' in response.url:
            return True
        else:
            global refUrl
            refUrl = response.url
            return False


# -------------Send Login Request----------------------
def SendLoginRequest(userId, password, service):
    global postHeader
    global postData
    global loginUrl
    global refUrl
    global url
    # ---extract data for http POST---
    postData['userId'] = userId
    postData['password'] = password
    postData['service'] = service
    postData['queryString'] = urllib.parse.quote(refUrl.split('?')[1])
    postHeader['Referer'] = refUrl
    postDataByte = urllib.parse.urlencode(postData).encode()
    postHeader['Content-Length'] = len(postDataByte)
    req = urllib.request.Request(loginUrl, headers=postHeader, data=postDataByte,  method= 'POST')
    # ---send post---
    try:
        response = urllib.request.urlopen(req, timeout=4)
        if response.length is None:
            raise Exception('No response after POST')
    except Exception:
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(localTime + ' :Can not post login request to ' + loginUrl)
        exit(0)
    else:
        responseData = response.read().decode('utf-8')
        if 'success' in responseData:
            return True
        elif 'fail' in responseData:
            return False


# ---------------Login---------------------------
def Login():
    filePath = os.path.dirname(os.path.realpath(sys.argv[0])) + '/accountList'
    try:
        with open(filePath, 'r', encoding='utf-8') as accountfile:
            accountlines = accountfile.readlines()
        if len(accountlines) != 0:
            for i in range(len(accountlines)):
                if SendLoginRequest(accountlines[i].split()[0], accountlines[i].split()[1], accountlines[i].split()[2]):
                    return
                if i == len(accountlines) - 1:
                    # i = last accout but cant login
                    raise Exception()
        else:
            raise Exception()
    except IOError:
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(localTime + ' :Can not read accountList File in: ' + filePath)
        exit(0)
    except Exception:
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(localTime + ' :Can not login using account from: ' + filePath)
        exit(0)
    else:
        return




# ---------------Script---Start-----------------------------------------------------------
if __name__ == '__main__':
    while 1==1:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if CheckLoginStatus(url) is False:
            Login()
            print(localtime + ' :检测掉线，重新连接！')
        else:
            print(localtime + ' :已连接，1min后重新检测')
            time.sleep(60)



    exit(0)
