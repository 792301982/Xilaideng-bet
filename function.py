import requests
from bs4 import BeautifulSoup
import time
import base64
import urllib
import json
import import_functions_define
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import globalvar as GlobalVar
 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "http://axn.668hf.com/search.aspx"
get_cookies_url = 'https://53jndgw.51ttyin.com/cp6-2-mb/bk.aspx/GetCookie'
bet_url = "https://%sdgw.51ttyin.com/cp6-2-mb/ashx/orderHandler.ashx"
bet_url2="https://09xrdgw.51ttyin.com/cp6-2-mb/ashx/orderHandler.ashx"
checknum_url='https://53jndgw.51ttyin.com/cp6-2-mb/checknum.aspx?ts=%s'
info_url='https://%sdgw.51ttyin.com/cp6-2-mb/app/ws_game.asmx/LoadDrawsInfo'
info_url2='https://53jndgw.51ttyin.com/cp6-2-mb/app/ws_game.asmx/LoadDrawsInfo'
history_url='http://speedylottos.com/speedy10-result.php'
history21_url='http://yun.ngk77.com/ui-02/detail.aspx/GetWinningnohistoryList'
last_url='https://%sdgw.51ttyin.com/cp6-2-mb/app/ws_game.asmx/LastWinnoCheck'

'''
安全码： 30161
账号： hh1600
密码： lmj258369
'''

'''
登录
'''
# r = requests.post(url, headers=headers, data={'wd': '30161'})
# soup = BeautifulSoup(r.text, "lxml")
# login_url = soup.select("iframe")[0]['src']
# print(login_url)
# login_url2='https://53jndgw.51ttyin.com/cp6-2-mb/?'+urllib.parse.urlparse(login_url)

# r = requests.post(login_url, headers=headers, cookies=r.cookies,verify=False)

# r = requests.post(get_cookies_url, headers=headers, cookies=r.cookies,verify=False)

# r = requests.post(checknum_url%(time.time()*1000), headers=headers,verify=False)
# with open('num.jpg','wb') as f:
#     f.write(r.content)
# cookies=r.cookies

cookies="__jsluid_s=79e35e8b869c3ee74460508d4c25ab8c; CP6_2_MB=umzrxko4llyocw1q1yubjlqs; urlpara=?idcode=30161&rnd=66651; __RequestVerificationToken_L2NwNi0yLW1i0=2885F06C88877C39C1BCF884EC8678BACACC76F89E7C54693262B60B6E6937A37F834A23EDADFD826BC49B46E704294960389BE220890EB91CF015A09CF310F802C97B2CBF439B809586CDAA066B71A0; .HwAuth_CP6_2_MB=AE1E45F1FC0394DCB347E4919A1DC37BFE92D86FBA1A43678B5164D4424CB8FD46ADB66870D5E240BD1002BB028781E7299B4EEE55ABA759AFE2C6D8D5E249DB307E1EBC1629B1345C82B15FFE8C4AB0DEDC78A0DEF8A4F3CAB9011906D81429CAA70A7485C5DC7FCC861691050B4BF8D50BA55DCD3BF5378B99EA993F90FA4A4591C21B8326534CA78BBC44085D511EF7457D3EC094D3BEEEC09F3EB9DF6071C092F3031A80E3D55FD8E6337E399250088100A6CF6E6A3C7F0750089C8674454CC93EB8D29F2F8B53575A4075A18117; hh1600_USER_CP6_2_MB=jumpurl=https://47nfdgw.51ttyin.com/cp6-2-mb/&guid=umzrxko4llyocw1q1yubjlqs_9"

def Reset_cookie(username,url_numb):
    headers=GlobalVar.get_demo_value()
    CheckIn_url='https://%sdgw.51ttyin.com/cp6-2-mb/app/ws_system.asmx/ToCheckIn'%url_numb
    r=requests.post(CheckIn_url,headers=headers,verify=False,json={
        'loginno':username,
    })
    new_cookie=requests.utils.dict_from_cookiejar(r.cookies)

    cookies=headers['Cookie']
    cookie_list=cookies.split(';')
    cookie_dict=dict()
    for i in cookie_list:
        try:
            cookie_dict[ i.split('=')[0] ]=i.split('=')[1]
        except:
            continue
    cookie_dict.update(new_cookie)

    cookies_str=''
    for i in cookie_dict:
        cookies_str+='%s=%s;'%(i,cookie_dict[i])

    headers['Cookie']=cookies_str
    GlobalVar.set_demo_value(headers)

# def Get22His(headers):
#     r=requests.post(history_url,headers=headers,verify=False)
#     soup=BeautifulSoup(r.text,'lxml')
#     lines=soup.select('.bordergray2')
#     t=dict()
#     for line in lines:
#         issue=line.select('.col-xs-5')[0].text
#         numbs=list()
#         for i in line.select(".resultnum3"):
#             numbs.append(i.text)
#         numbs=','.join(numbs)
#         t[issue[-4:]]=numbs
#     return t

# def Get21His(headers):
#     timeStamp=import_functions_define.Beijing_time()
#     timeArray = time.localtime(timeStamp)
#     otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
#     r=requests.post(history21_url,headers=headers,verify=False,json={
#         'gameno':'21',
#         'gamegroupno':'6',
#         'pagesize':'15',
#         'curentsize':'1',
#         'transdate':"2019-12-26",
#     })
#     return r.text

def GetlastHis(headers,gameno,url_numb):
    r=requests.post(last_url%url_numb,headers=headers,verify=False,json={
        'gameno':str(gameno),
    })
    s=json.loads(r.text)['d']
    d=json.loads(s)
    t=dict()
    issue=d['message']['ld']
    numbs=d['message']['lr']
    numbs=','.join(numbs)
    t[issue[-4:]]=numbs
    return t
    

def GetNowIssue(gameno,url_numb,headers):
    r=requests.post(info_url%url_numb,headers=headers,json={
        'gameno':gameno
    },verify=False)
    s=json.loads(r.text)['d']
    d=json.loads(s)
    return d['message']

def Bet_xld(gameno,issue,method_list,url_numb,headers):
    """
    601：1：1
    位置：号：金额
    601-610
    冠亚和：638：3-19 ：1
    """
    # if gameno=='22':
    #     issue=GetNowIssue(gameno)['cd']
    wagers=""
    for i in method_list:
        wagers+="%s:%s:%s;" % (int(i[0])+600,int(i[1]),int(i[2]))
    print("正在投注……")
    r = requests.post(bet_url%url_numb, headers=headers, data={
        'stype': 'checkxiadan',
        'gameno': gameno,                                         #22 极速赛车 21 幸运飞艇
        'roundno': issue,
        'wagerroundno': 'D',
        'wagers': wagers,
    }, verify=False)
    print(r.text)
    return '200'

# d=Get21His()
# input()