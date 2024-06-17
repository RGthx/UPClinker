# UPC无线校园网认证python脚本
# 本项目基于AutoLogin_Mail for UPC Network Authentication，感谢大佬的项目，大佬NB！！！
## 该脚本能够方便使用python的系统登录校园网
此脚本针对UPC校园网认证系统！
openwrt路由器也可以在安装python3的前提下运行此脚本并登录校园网;
需要注意的是在配置dns时需要加上：121.251.251.251;121.251.251.250;
否则无法访问wlan.upc.edu.cn;程序也无法登录校园网
功能：登陆状况检测（默认1min一次）+自动登陆
## 1、使用方法   
accountList文件：填写能够登陆的网络账号 账号名 密码 运营商 使用空格分隔 多用户使用换行符分隔，顶行使用'#'注释该行，此文件需要与脚本保存在同一目录下。

运营商代码（中国联通：unicom，中国电信：ctcc，中国移动：cmcc，校园网：default，校园内网：local）  
        
## 2、不同认证系统的自定义方法
（1）此脚本主要适用UPC锐捷web认证，不同认证系统需要修改全局变量中postHeader和postData的格式。  
（2）不同认证系统登陆成功后的重定向网址不同，根据需要可修改CheckLoginStatus函数中的判别方法。   
## 3、部署方法
 Windows10/11用户可以尝试直接使用封装好的release包
或者使用python3运行UPClinker.py  
注意修改accountList文件；改成自己的校园网账号

## 4、 其他有关项目链接
1. 中国石油大学(华东) 网络认证系统Python接口  https://github.com/jerry-yuan/ePortalUPC
