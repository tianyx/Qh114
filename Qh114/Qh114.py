
# -* - coding: UTF-8 -* -
from splinter.browser import Browser

from time import sleep

import traceback

import time, sys
import re

# 登陆地址
login_url = "http://www.bjguahao.gov.cn/logout.htm"

loginOk_url = "http://www.bjguahao.gov.cn/index.htm"

# loginNeed_url = "http://www.bjguahao.gov.cn/dpt/appoint/142-200039484.htm"

loginNeed_url = "http://www.bjguahao.gov.cn/dpt/appoint/142-200039544.htm"

login_name = "13581508752"
login_pass = "tyx575910"

target_date = "2018-11-07"
#上下午 1, 2
target_noon = "1"

#医生过滤
target_docTypeKeyWords = [u"专家", u"副主任", u"特需"]
target_docNameKeyWords = None
#---------------------------------------------------------
def IsMatchDocFilter(nameIn, typeIn):
    #比较是否符合过滤条件, name 优先
    bTypeOk = False
    bNameOk = False
    if target_docNameKeyWords is None or (len(target_docNameKeyWords) == 0):
        bNameOk = True
    else:
        for oneK in target_docNameKeyWords:
            if nameIn.find(oneK) >= 0:
                #名字匹配直接返回
                bNameOk = True
                return True;
    #check type
    if target_docTypeKeyWords is None or (len(target_docTypeKeyWords) == 0):
        bTypeOk = True
    else:
        for oneT in target_docTypeKeyWords:
            if typeIn.find(oneT) >= 0:
                bTypeOk = True
                break

    bRet = bTypeOk and bNameOk
    return bRet

#--------------------------------------------------
def loginFunc():
    browser = Browser("chrome")  
    browser.visit(login_url)
    # 找到登陆按钮点击
    #browser.find_by_text(u"登录").click()

    #输入用户密码
    browser.fill("smsQuick", login_name);
    browser.find_by_id("pwQuickLogin").fill(login_pass);
    browser.find_by_id("quick_login").click();
    while True:
        #判断当前的url是否已经进入系统
        if browser.url != loginOk_url:
            sleep(1)
        else:
            break

    #进入所需挂号页面
    browser.visit(loginNeed_url);

    while True:
        #判断当前的url是否已经进入系统
        if browser.url != loginNeed_url:
            sleep(1)
        else:
            break
# 开始循环检查是否有票
    while True:
        #判断当前的url是否已经进入系统
        if not FindPiao(browser):
            sleep(1)
            browser.reload()
        else:
            break
    while True:
        if browser.url.find("http://www.bjguahao.gov.cn/order/confirm") < 0:
            sleep(0.1)

def FindPiao(browser):
        for itd in browser.find_by_tag("td"):
            if(itd.text.find(u"剩余")):
                tmptext = itd.text;
                inputList = itd.find_by_tag("input");
                if(len(inputList) > 0):
                    tgInput = inputList.first
                    tmpvalue = tgInput.value
                    tmpname = tgInput.text  
                    #0_1_2018-10-17 =列号_上1下2午_日期
                    vname = tmpvalue.split("_", 2);
                    if(len(vname) == 3):
                        if vname[1] == target_noon and vname[2] == target_date:
                            itd.click()
                            sleep(0.2)
                            #show doctor list,find doctor
                            if not FindDoctor(browser):                                
                                return False
                            else:
                                return True
                        else:
                            pass 
        return False
#------------------------------
def FindDoctor(browser):
    for allDocTag in browser.find_by_id("public_doctor"):
        #遍历所有doctor
        for oneDoc in allDocTag.find_by_tag("div"):
           #find name
           docName = oneDoc.find_by_tag("h4")
           if docName is None or len(docName) == 0:
               continue
           print(repr(docName[0].text))
           nameSp = docName[0].text
           nametwo = nameSp.split(" ", 2)
           print(nametwo)
           if not IsMatchDocFilter(nametwo[0], nametwo[1]):
               continue
           #find remain ticket
           for docInfo in oneDoc.find_by_tag("span"):
               if docInfo.text.find(u"医事服务费：") >= 0 or docInfo.text.find(u"剩余号：") >= 0:
                   print(docInfo.text, docInfo.find_by_tag("b")[0].text)
           for haoInfo in oneDoc.find_by_tag("a"): 
               if haoInfo.text.find(u"预约挂号") >= 0:
                   print("可以挂号")
                   haoInfo.click()
                   
                   return True
                
                   
    return False
# ------------------------------------
def main():
   loginFunc()





# if __name__ == '__main__'的意思是：当.py文件被直接运行时（内置变量__name__会等于'__main__'），if __name__ == '__main__'之下的代码块将被运行；
# 当.py文件以模块形式被导入时（内置变量__name__会等于'文件名'），if __name__ == '__main__'之下的代码块不被运行。
if __name__ == '__main__':  
   main()