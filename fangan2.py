from import_functions_define import *
from function import *
import globalvar as GlobalVar

moniyue=''

def worker2(cookies, lotteryid, model, stop_to_bet, set_moneys, relation, treeview1, treeview2, balance_label, zongshuying_label,headers,username,url_numb,):
    '''
    方案二主函数 。单参数有多个值的均为列表 relation为列表内字典["{'0-9':['01','02'],'4-9':['02','05']}"] 开始投注的数字
                                                            ["0-9:1,5,9/1-8:1,7,9"]
                                                            （格式：1-0,1-2/2-1,2-3/1-3,1-4） 填满 01 到 10
    '''
    global moniyue
    moni_yue=moniyue

    bet_list_flag = ''  # 用于检测是否开奖
    bet_list_dict = dict()  # 各期投注信息用于treeview打印
    bet_location_dict = dict()  # 每个位置 正在下注的数字 的金额
    for i in range(10):
        bet_location_dict[str(i)] = dict()

    relation = relation[0]  # 处理字典
    relation_l = relation.split('/')
    relation = dict()
    relation_m=list()
    
    def Change2two(x):
        return '%0*d' % (2, int(x))
    for i in relation_l:
        relation_m.append(i.split(','))
        # relation[i.split(':')[0]] = list(
        #     map(Change2two, i.split(':')[1].split(',')))
    
    for i in relation_m:
        for u in i:
            relation[u]=['01','02','03','04','05','06','07','08','09','10']

    bet_loc_rela_dict = dict()
    numbs_dict=dict()
    bet_relation_numbs=dict()         #各关系上一期投注的数字
    for i in relation_m:
        for u in i:
            bet_relation_numbs[u]=list()
    GlobalVar.set_demo_value(headers)
    while(1):
        try:
            Reset_cookie(username,url_numb)
            headers=GlobalVar.get_demo_value()
            if(str(lotteryid) == '3'):
                lotteryid='21'
            next_issue = GetNowIssue(lotteryid,url_numb,headers)['cd']
            # if(str(lotteryid) == '22'):
            #     next_issue = GetNowIssue(lotteryid,url_numb,headers)['cd']
            # else:
            #     next_issue = getCurInfoAndModel(lotteryid, cookies)[0]

            # if(str(lotteryid) == '3'):
            #     next_issue1 = ''.join(next_issue.split('-'))
            #next_issue = getCurInfoAndModel(lotteryid, cookies)[0]    # 正在投注的这一期

            numbs_dict.update(GetlastHis(headers,lotteryid,url_numb))
            
            # if(str(lotteryid) == '22'):
            #     numbs_dict.update(Get22His(headers))
            # else:
            #     numbs_dict.update(Get_last30_number(lotteryid, cookies))  # 开奖信息列表

            # if(lotteryid == '9'):
            #     now_issue = '%0*d' % (4, int(next_issue[-4:])-1)
            # else:
            #     # 开奖的最新一期（仅4位）
            #     now_issue = '%0*d' % (4, int(next_issue.split('-')[1])-1)
            # if(lotteryid == '9'):
            #     now_issue = '%0*d' % (4, int(next_issue[-4:])-1)
            # elif(str(lotteryid) == '22'):
            #     now_issue = '%0*d' % (4, int(next_issue[-4:])-1)
            # else:
            #     # 仅4位
            #     now_issue = '%0*d' % (4, int(next_issue.split('-')[1])-1)
            now_issue = '%0*d' % (4, int(next_issue[-4:])-1)

            treeview_del(treeview1)
            treeview_insert(treeview1, numbs_dict)  # 设置开奖信息
            if(str(model)=='1'):
                #balance_label.set(GetUserBalance(cookies))  # 设置余额
                pass
            else:
                balance_label.set(moni_yue)
        except:
            # print(traceback.print_exc())
            print('获取账户信息失败，等待10秒后重试')
            time.sleep(10)
            continue

        zong = 0
        # 计算彩种总输赢
        # for i in bet_list_dict:
        #     for u in bet_list_dict[i]:
        #         try:
        #             if(lotteryid == '9'):
        #                 if(u[1] == numbs_dict[i[-4:]].split(',')[int(u[0])]):
        #                     zong += int(u[2])*9.96-int(u[2])
        #                 else:
        #                     zong -= int(u[2])
        #             else:
        #                 if(u[1] == numbs_dict[i.split('-')[1]].split(',')[int(u[0])]):
        #                     zong += int(u[2])*9.96-int(u[2])
        #                 else:
        #                     zong -= int(u[2])
        #         except:
        #             # print('计算输赢金额出错')
        #             pass
        for i in bet_list_dict:
            for u in bet_list_dict[i]:
                try:
                    if(u[1] == numbs_dict[i[-4:]].split(',')[int(u[0])]):
                        zong += int(u[2])*9.698-int(u[2])
                    else:
                        zong -= int(u[2])
                except:
                    # print('计算输赢金额出错')
                    pass

        if(int(zong) >= int(stop_to_bet[0])):
            input("止赢，等待中……")
        elif(int(zong) <= -int(stop_to_bet[1])):
            input("止损，等待中……")

        moni_yue=str(int(moniyue)+int(zong))
        if(int(moni_yue) <= 0):
            input("余额空，等待中……") 

        if(model == '1'):
            try:
                #zongshuying_label.set(ZongWinSearch(cookies))  # 设置今日总输赢
                pass
            except:
                pass
        else:
            # 单彩种总输赢
            zongshuying_label.set(str(zong))

        try:
            now_numbs = numbs_dict[now_issue].split(',')
        except KeyError:
            print('彩种：%s' % lotteryid, '开奖结果尚未更新，正在重试……')
            time.sleep(10)
            continue

        if(now_numbs == bet_list_flag):
            print(time.asctime(time.localtime(time.time())), lotteryid,
                  '当前期号：', next_issue, '等待开奖中……')
            time.sleep(20)
            continue
        else:
            # 方案投注策略从此开始-----------------------------------------------------------
            # 验证是否中奖
            for i in bet_loc_rela_dict:
                start_loc = i.split('-')[0]  # 开始投注的位置
                bet_loc = i.split('-')[1]  # 实际投注的位置
                if(len(bet_loc_rela_dict[i]) != 0):
                    for p in bet_list:
                        if(bet_loc == p[0] and bet_relation_numbs[i] == p[1] ):
                            if(now_numbs[int(bet_loc)] == p[1]):
                                print(now_issue, start_loc+'-'+bet_loc, now_numbs[int(bet_loc)], '中奖')
                                bet_loc_rela_dict[i] = list()
                                for m in relation_m:
                                    if(i in m):
                                        for u in m:
                                            bet_loc_rela_dict[u] = list()
                                # for u in bet_loc_rela_dict:
                                #     if(u.split('-')[0] == i.split('-')[0]):
                                #         bet_loc_rela_dict[u] = list()
            
            for i in relation_m:
                for u in i:
                    bet_relation_numbs[u]=list()

            for i in range(10):
                bet_location_dict[str(i)] = dict()                     #清空

            for n, i in enumerate(relation):
                start_loc = i.split('-')[0]  # 开始投注的位置
                bet_loc = i.split('-')[1]  # 实际投注的位置
                for u in relation[i]:
                    if(int(u) == int(now_numbs[int(start_loc)]) and (i not in bet_loc_rela_dict or len(bet_loc_rela_dict[i]) == 0)):
                        bet_loc_rela_dict[i] = set_moneys[::-1]
                        # bet_location_dict[bet_loc][u]=set_moneys[::-1]               #设置金额。bet_location_dict[赛道][数字]=金额列表

            '''for n, i in enumerate(bet_list_flag):
                if i == now_numbs[n]:
                    money_dict[str(n)] = set_moneys[::-1]'''

        # 更改投注数字
        for i in bet_loc_rela_dict:
            start_loc = i.split('-')[0]  # 开始投注的位置
            bet_loc = i.split('-')[1]  # 实际投注的位置
            if(len(bet_loc_rela_dict[i]) != 0):
                #bet_location_dict[bet_loc].clear()
                if(now_numbs[int(start_loc)] not in bet_location_dict[bet_loc]):
                    bet_location_dict[bet_loc][now_numbs[int(start_loc)]] =list()
                bet_location_dict[bet_loc][now_numbs[int(start_loc)]] .append(
                    bet_loc_rela_dict[i].pop() )
                bet_relation_numbs[i]=now_numbs[int(start_loc)]

        bet_list = list()  # 位置 投注内容 金额
        for i in bet_location_dict:
            if(len(bet_location_dict[i]) != 0):
                for u in bet_location_dict[i]:
                    if(len(bet_location_dict[i][u]) != 0):
                        # 提取金额
                        bet_money = str(bet_location_dict[i][u].pop())
                        bet_list.append([str(i), u, bet_money])

        bet_list_dict[next_issue] = bet_list

        treeview_del(treeview2)
        treeview2_insert(treeview2, bet_list_dict)  # 设置投注信息

        if(len(bet_list) != 0):
            if(model == '1'):
                try:
                    # if(str(lotteryid) == '3'):
                    #     d = Bet(lotteryid, ''.join(
                    #         next_issue.split('-')), bet_list, cookies)
                    # else:
                    #     d = Bet(lotteryid, next_issue, bet_list, cookies)
                    d = Bet_xld(lotteryid, next_issue,bet_list,url_numb,headers)
                except:
                    d = '0'
                    print("投注异常")
            else:
                d = '200'
                print(
                    ''' 
        模拟投注成功
        彩种：%s
        期号：%s
        '''
                    % (lotteryid, next_issue)
                )
                # for i in bet_list:
                #     print('位置:'+str(i[0]), '内容:'+str(i[1]), str(i[2])+'元')
            if(d != '200'):
                print('投注失败，跳过')
                time.sleep(10)
        bet_list_flag = now_numbs[:]


def fangan2(cookies,moni_yue,headers,username,url_numb):
    # 方案二 主线程
    global moniyue
    moniyue=moni_yue
    base = tk.Tk()
    base.title('方案二：位置互换')
    base.geometry('760x700')
    fm1 = Frame(base)
    balance_label = StringVar()
    balance_label.set('0')
    Label(fm1, text='余额：').grid(row=1, column=1)
    Label(fm1, textvariable=balance_label).grid(row=1, column=2)
    zongshuying_label = StringVar()
    zongshuying_label.set('0')
    Label(fm1, text='今日总输赢：').grid(row=2, column=1)
    Label(fm1, textvariable=zongshuying_label).grid(row=2, column=2)
    fm1.grid(row=1, column=1)

    def start_bet(frame1, cookies, lotteryid, model, stop_to_bet, set_moneys, relation, treeview1, treeview2, balance_label, zongshuying_label):
        t = threading.Thread(target=worker2, args=(cookies, lotteryid, model, stop_to_bet,
                                                   set_moneys, relation, treeview1, treeview2, balance_label, zongshuying_label,headers,username,url_numb,))
        t.start()

        def pause_bet():
            print('暂停')
            stop_thread(t)
        Button(frame1, text="暂停", command=pause_bet).grid(row=13, column=1)

    notebook = ttk.Notebook(base)
    # 22极速赛车
    frame1 = Frame(notebook)
    col = 1
    Label(frame1, text="22极速赛车开奖信息：").grid(row=1, column=col)
    columns = ['期号', '开奖号']
    treeview_jisu1 = ttk.Treeview(
        frame1, height=10, show="headings", columns=columns)  # 表格
    treeview_jisu1.column("期号", width=50, anchor='center')  # 表示列,不显示
    treeview_jisu1.column("开奖号", width=200, anchor='center')
    treeview_jisu1.heading("期号", text="期号")  # 显示表头
    treeview_jisu1.heading("开奖号", text="开奖号")
    treeview_jisu1.grid(row=2, column=col)

    columns = ['期号', '赛道', '投注内容', '投注金额']
    treeview_jisu2 = ttk.Treeview(
        frame1, height=10, show="headings", columns=columns)  # 表格
    treeview_jisu2.column("期号", width=100, anchor='center')  # 表示列,不显示
    treeview_jisu2.column("赛道", width=30, anchor='center')
    treeview_jisu2.column("投注内容", width=50, anchor='center')
    treeview_jisu2.column("投注金额", width=50, anchor='center')
    treeview_jisu2.heading("期号", text="期号")  # 显示表头
    treeview_jisu2.heading("赛道", text="赛道")
    treeview_jisu2.heading("投注内容", text="投注内容")
    treeview_jisu2.heading("投注金额", text="投注金额")
    treeview_jisu2.grid(row=2, column=col+1)

    Label(frame1, text="极速赛车止赢止损（空格分隔）：").grid(row=4, column=col)
    text_jisu_stop2bet = Text(frame1, width=10, height=2)
    text_jisu_stop2bet.grid(row=5, column=col)

    Label(frame1, text="极速赛车模式（1真实 2模拟）：").grid(row=6, column=col)
    text_jisu_model = Text(frame1, width=10, height=2)
    text_jisu_model.grid(row=7, column=col)

    Label(frame1, text="极速赛车金额（空格分隔）：").grid(row=8, column=col)
    text_jisu_moneys = Text(frame1, width=20, height=4)
    text_jisu_moneys.grid(row=9, column=col)

    Label(frame1, text="极速赛车 车道关系和投注数字（格式：1-0,1-2/2-1,2-3/1-3,1-4）").grid(row=10, column=col)
    text_jisu_chedao = Text(frame1, width=50, height=8)
    text_jisu_chedao.grid(row=11, column=col)

    Button(frame1, text="开始", command=lambda: start_bet(frame1, cookies, '22', text_jisu_model.get('1.0', END).strip(), text_jisu_stop2bet.get('1.0', END).strip().split(' '), text_jisu_moneys.get(
        '1.0', END).strip().split(' '), text_jisu_chedao.get('1.0', END).strip().split(' '), treeview_jisu1, treeview_jisu2, balance_label, zongshuying_label)).grid(row=12, column=col)

    # 3幸运飞艇
    frame2 = Frame(notebook)
    col = 2
    Label(frame2, text="3幸运飞艇开奖信息：").grid(row=1, column=col)
    columns = ['期号', '开奖号']
    treeview_xingyun1 = ttk.Treeview(
        frame2, height=10, show="headings", columns=columns)  # 表格
    treeview_xingyun1.column("期号", width=50, anchor='center')  # 表示列,不显示
    treeview_xingyun1.column("开奖号", width=200, anchor='center')
    treeview_xingyun1.heading("期号", text="期号")  # 显示表头
    treeview_xingyun1.heading("开奖号", text="开奖号")
    treeview_xingyun1.grid(row=2, column=col)

    columns = ['期号', '赛道', '投注内容', '投注金额']
    treeview_xingyun2 = ttk.Treeview(
        frame2, height=10, show="headings", columns=columns)  # 表格
    treeview_xingyun2.column("期号", width=100, anchor='center')  # 表示列,不显示
    treeview_xingyun2.column("赛道", width=30, anchor='center')
    treeview_xingyun2.column("投注内容", width=50, anchor='center')
    treeview_xingyun2.column("投注金额", width=50, anchor='center')
    treeview_xingyun2.heading("期号", text="期号")  # 显示表头
    treeview_xingyun2.heading("赛道", text="赛道")
    treeview_xingyun2.heading("投注内容", text="投注内容")
    treeview_xingyun2.heading("投注金额", text="投注金额")
    treeview_xingyun2.grid(row=2, column=col+1)

    Label(frame2, text="feiting止赢止损（空格分隔）：").grid(row=4, column=col)
    text_feiting_stop2bet = Text(frame2, width=10, height=2)
    text_feiting_stop2bet.grid(row=5, column=col)

    Label(frame2, text="feiting模式（1真实 2模拟）：").grid(row=6, column=col)
    text_feiting_model = Text(frame2, width=10, height=2)
    text_feiting_model.grid(row=7, column=col)

    Label(frame2, text="feiting金额（空格分隔）：").grid(row=8, column=col)
    text_feiting_moneys = Text(frame2, width=20, height=4)
    text_feiting_moneys.grid(row=9, column=col)

    Label(frame2, text="feiting车道关系和投注数字（格式：1-0,1-2/2-1,2-3/1-3,1-4）：").grid(row=10, column=col)
    text_feiting_chedao = Text(frame2, width=50, height=8)
    text_feiting_chedao.grid(row=11, column=col)

    Button(frame2, text="开始", command=lambda: start_bet(frame2, cookies, '3', text_feiting_model.get('1.0', END).strip(), text_feiting_stop2bet.get('1.0', END).strip().split(' '), text_feiting_moneys.get(
        '1.0', END).strip().split(' '), text_feiting_chedao.get('1.0', END).strip().split(' '), treeview_xingyun1, treeview_xingyun2, balance_label, zongshuying_label)).grid(row=12, column=col)

    # 9疯狂赛车
    col = 3
    frame3 = Frame(notebook)
    Label(frame3, text="9疯狂赛车开奖信息：").grid(row=1, column=col)
    columns = ['期号', '开奖号']
    treeview_huanle1 = ttk.Treeview(
        frame3, height=10, show="headings", columns=columns)  # 表格
    treeview_huanle1.column("期号", width=50, anchor='center')  # 表示列,不显示
    treeview_huanle1.column("开奖号", width=200, anchor='center')
    treeview_huanle1.heading("期号", text="期号")  # 显示表头
    treeview_huanle1.heading("开奖号", text="开奖号")
    treeview_huanle1.grid(row=2, column=col)

    columns = ['期号', '赛道', '投注内容', '投注金额']
    treeview_huanle2 = ttk.Treeview(
        frame3, height=10, show="headings", columns=columns)  # 表格
    treeview_huanle2.column("期号", width=100, anchor='center')  # 表示列,不显示
    treeview_huanle2.column("赛道", width=30, anchor='center')
    treeview_huanle2.column("投注内容", width=50, anchor='center')
    treeview_huanle2.column("投注金额", width=50, anchor='center')
    treeview_huanle2.heading("期号", text="期号")  # 显示表头
    treeview_huanle2.heading("赛道", text="赛道")
    treeview_huanle2.heading("投注内容", text="投注内容")
    treeview_huanle2.heading("投注金额", text="投注金额")
    treeview_huanle2.grid(row=2, column=col+1)

    Label(frame3, text="fengkuang止赢止损（空格分隔）：").grid(row=4, column=col)
    text_fengkuang_stop2bet = Text(frame3, width=10, height=2)
    text_fengkuang_stop2bet.grid(row=5, column=col)

    Label(frame3, text="fengkuang模式（1真实 2模拟）：").grid(row=6, column=col)
    text_fengkuang_model = Text(frame3, width=10, height=2)
    text_fengkuang_model.grid(row=7, column=col)

    Label(frame3, text="fengkuang金额（空格分隔）：").grid(row=8, column=col)
    text_fengkuang_moneys = Text(frame3, width=20, height=4)
    text_fengkuang_moneys.grid(row=9, column=col)

    Label(frame3, text="fengkuang车道关系和投注数字（格式：1-0,1-2/2-1,2-3/1-3,1-4）：").grid(row=10, column=col)
    text_fengkuang_chedao = Text(frame3, width=50, height=8)
    text_fengkuang_chedao.grid(row=11, column=col)

    Button(frame3, text="开始", command=lambda: start_bet(frame3, cookies, '9', text_fengkuang_model.get('1.0', END).strip(), text_fengkuang_stop2bet.get('1.0', END).strip().split(' '), text_fengkuang_moneys.get(
        '1.0', END).strip().split(' '), text_fengkuang_chedao.get('1.0', END).strip().split(' '), treeview_huanle1, treeview_huanle2, balance_label, zongshuying_label)).grid(row=12, column=col)

    # t1=threading.Thread(target=worker1,args=(cookies,'22',model,stop_to_bet,set_moneys,chedao))
    # t2=threading.Thread(target=worker1,args=(cookies,'3',model,stop_to_bet,set_moneys,chedao))
    # t3=threading.Thread(target=worker1,args=(cookies,'31',model,stop_to_bet,set_moneys,chedao))
    # t1.start()
    # t2.start()
    # t3.start()

    notebook.add(frame1, text="22极速赛车")
    notebook.add(frame2, text="3幸运飞艇")
    #notebook.add(frame3, text="9疯狂赛车")
    notebook.grid(row=1, column=2)

    base.mainloop()


if __name__ == "__main__":
    # 一个方案一个进程
    multiprocessing.freeze_support()
    '''
        方案二：位置互换
    '''
    print('喜来登自动投注')
    print('方案二：位置互换')
    print('22极速赛车        3幸运飞艇        9疯狂赛车')
    # model=input('选择模式前的序号 1真实 2模拟：')
    # jisusaiche_chedao=input('选择极速赛车车道（空格分隔）：')
    # xingyun_chedao=input('选择幸运飞艇车道（空格分隔）：')
    # huanle_chedao=input('选择欢乐赛车车道（空格分隔）：')
    # set_moneys = input("输入投注金额（用空格分隔开）：").split(' ')
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    #"Cookie": "Cookie: CP6_2_MB=x2na2vbosfgdrobjygz0yvqd; urlpara=?idcode=30161&rnd=66651; __RequestVerificationToken_L2NwNi0yLW1i0=3ECC7991F3FB148AFA2987B2E0F4E0A05A286E9071EF866B847A9353C9E3AAB0E3DB8025EB59C79248163090D899C8258ACE41BC9726927A68F83CD86A56932E5E3FA8FFD6A011CAFFF53D29E1DE7F80; __jsluid_s=87c5a3813be00d87c5de8d34a8bd9078; .HwAuth_CP6_2_MB=B42750686C3EBEF016D1D2B64F8692C748860366A70726830368609183BA983BA3FE3FBC9EDFA4827905A62749804BE02769851D8EAF0BA7D7655E69110384147059A9953AF50C453C110477F7C708101E4FF0288E9818E07C8984E6A515A54FD0182838F43A64F9F01BF3682188A2D521219A9BBC64FA7DBD4099CB829C218BCC27700775B91AB96300EB5C4C782475311ED2619141B965F5423A70DE98D139F61034884973C70635E3FECEF838CB177F5F435827D8110C4AF22D01DA431FB921A5F078C002683D1B6B074B4A705CBC; hh1600_USER_CP6_2_MB=jumpurl=https://09xrdgw.51ttyin.com/cp6-2-mb/&guid=x2na2vbosfgdrobjygz0yvqd_53",
    }
    #cookies = login()
    # cookies=''
    moni_yue=int(input("输入模拟金额："))
    headers['Cookie']=input("输入cookies：")
    GlobalVar.set_demo_value(headers)
    url_numb=input("输入域名序号：")
    username=input("输入用户名：")
    fangan2(cookies,moni_yue,headers,username,url_numb)
    # p1=Process(target=worker1,args=(cookies,'22',model,set_moneys,jisusaiche_chedao,))
    # p2=Process(target=worker1,args=(cookies,'31',model,set_moneys,huanle_chedao,))
    # p1.start()
    # p2.start()
