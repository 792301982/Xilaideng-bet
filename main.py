from fangan1 import *
from fangan2 import *
from fangan3 import *
from function import *
import globalvar as GlobalVar

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    #"Cookie": "Cookie: CP6_2_MB=x2na2vbosfgdrobjygz0yvqd; urlpara=?idcode=30161&rnd=66651; __RequestVerificationToken_L2NwNi0yLW1i0=3ECC7991F3FB148AFA2987B2E0F4E0A05A286E9071EF866B847A9353C9E3AAB0E3DB8025EB59C79248163090D899C8258ACE41BC9726927A68F83CD86A56932E5E3FA8FFD6A011CAFFF53D29E1DE7F80; __jsluid_s=87c5a3813be00d87c5de8d34a8bd9078; .HwAuth_CP6_2_MB=B42750686C3EBEF016D1D2B64F8692C748860366A70726830368609183BA983BA3FE3FBC9EDFA4827905A62749804BE02769851D8EAF0BA7D7655E69110384147059A9953AF50C453C110477F7C708101E4FF0288E9818E07C8984E6A515A54FD0182838F43A64F9F01BF3682188A2D521219A9BBC64FA7DBD4099CB829C218BCC27700775B91AB96300EB5C4C782475311ED2619141B965F5423A70DE98D139F61034884973C70635E3FECEF838CB177F5F435827D8110C4AF22D01DA431FB921A5F078C002683D1B6B074B4A705CBC; hh1600_USER_CP6_2_MB=jumpurl=https://09xrdgw.51ttyin.com/cp6-2-mb/&guid=x2na2vbosfgdrobjygz0yvqd_53",
}

if __name__ == "__main__":
    #一个方案一个进程
    multiprocessing.freeze_support()

    moni_yue=input('设置模拟投注余额：')
    headers['Cookie']=input("输入cookies：")
    url_numb=input("输入域名序号：")
    username=input("输入用户名：")
    GlobalVar.set_demo_value(headers)
    #cookies=login()
    #cookies=''
    #fangan2(cookies)
    p1=Process(target=fangan1,args=(cookies,moni_yue,headers,username,url_numb))
    p2=Process(target=fangan2,args=(cookies,moni_yue,headers,username,url_numb))
    #p3=Process(target=fangan3,args=(cookies,moni_yue,headers,url_numb))
    p1.start()
    p2.start()
    #p3.start()