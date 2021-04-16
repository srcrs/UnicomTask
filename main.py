# -*- coding: utf-8 -*-
# @Time    : 2021/2/15 06:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com

import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring
import pytz

#用户登录全局变量
client = None

#获取沃之树首页，得到领流量的目标值
def get_woTree_glowList():
    index = client.post('https://m.client.10010.com/mactivity/arbordayJson/index.htm')
    index.encoding='utf-8'
    res = index.json()
    return res['data']['flowChangeList']

#沃之树任务
#位置: 首页 --> 游戏 --> 沃之树
def woTree_task():
    #领取4M流量*3
    try:
        flowList = get_woTree_glowList()
        num = 1
        for flow in flowList:
            takeFlow = client.get('https://m.client.10010.com/mactivity/flowData/takeFlow.htm?flowId=' + flow['id'])
            takeFlow.encoding='utf-8'
            res1 = takeFlow.json()
            if res1['code'] == '0000':
                logging.info('【沃之树-领流量】: 4M流量 x' + str(num))
            else:
                logging.info('【沃之树-领流量】: 已领取过 x' + str(num))
            #等待1秒钟
            time.sleep(1)
            num = num + 1
        client.post('https://m.client.10010.com/mactivity/arbordayJson/getChanceByIndex.htm?index=0')
        #浇水
        grow = client.post('https://m.client.10010.com/mactivity/arbordayJson/arbor/3/0/3/grow.htm')
        grow.encoding='utf-8'
        res2 = grow.json()
        logging.info('【沃之树-浇水】: 获得' + str(res2['data']['addedValue']) + '培养值')
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【沃之树】: 错误，原因为: ' + str(e))

#经多次测试，都可加倍成功了
#每日签到，1积分 ，第七天得到 1G 日包
#位置: 我的 --> 我的金币
def daySign_task(username):
    try:
        #参考同类项目 HiCnUnicom 待明日验证是否能加倍成功
        client.headers.update({'referer': 'https://img.client.10010.com/activitys/member/index.html'})
        param = 'yw_code=&desmobile=' + username + '&version=android@$8.0100'
        client.get('https://act.10010.com/SigninApp/signin/querySigninActivity.htm?' + param)
        client.headers.update({'referer': 'https://act.10010.com/SigninApp/signin/querySigninActivity.htm?' + param})
        daySign = client.post('https://act.10010.com/SigninApp/signin/daySign')
        daySign.encoding='utf-8'
        #本来是不想加这个的，但是会出现加倍失败的状况，暂时加上也是有可能出问题
        client.post('https://act.10010.com/SigninApp/signin/todaySign')
        client.post('https://act.10010.com/SigninApp/signin/addIntegralDA')
        client.post('https://act.10010.com/SigninApp/signin/getContinuous')
        client.post('https://act.10010.com/SigninApp/signin/getIntegral')
        client.post('https://act.10010.com/SigninApp/signin/getGoldTotal')
        client.headers.pop('referer')
        res = daySign.json()
        if res['status'] == '0000':
            logging.info('【每日签到】: ' + '打卡成功')
        elif res['status'] == '0002':
            logging.info('【每日签到】: ' + res['msg'])
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日签到】: 错误，原因为: ' + str(e))

#获取 encrymobile，用于抽奖
def get_encryptmobile():
    page = client.post('https://m.client.10010.com/dailylottery/static/textdl/userLogin')
    page.encoding='utf-8'
    match = re.search('encryptmobile=\w+',page.text,flags=0)
    usernumber = match.group(0)[14:]
    return usernumber

#天天抽奖
#我的 --> 我的金币 --> 天天抽好礼
def luckDraw_task():
    try:
        numjsp = get_encryptmobile()
        #加上这一堆，看中奖率会不会高点
        client.post('https://m.client.10010.com/mobileservicequery/customerService/share/defaultShare.htm')
        client.get('https://m.client.10010.com/dailylottery/static/doubleball/firstpage?encryptmobile=' + numjsp)
        client.get('https://m.client.10010.com/dailylottery/static/outdailylottery/getRandomGoodsAndInfo?areaCode=076')
        client.get('https://m.client.10010.com/dailylottery/static/active/findActivityInfo?areaCode=076&groupByType=&mobile=' + numjsp)
        for i in range(3):
            luck = client.post('https://m.client.10010.com/dailylottery/static/doubleball/choujiang?usernumberofjsp=' + numjsp)
            luck.encoding='utf-8'
            res = luck.json()
            logging.info('【天天抽奖】: ' + res['RspMsg'] + ' x' + str(i+1))
            #等待1秒钟
            time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【天天抽奖】: 错误，原因为: ' + str(e))

#游戏任务中心每日打卡领积分，游戏任务自然数递增至7，游戏频道每日1积分
#位置: 首页 --> 游戏 --> 每日打卡
def gameCenterSign_Task(username):
    data1 = {
        'methodType': 'signin',
        'clientVersion': '8.0100',
        'deviceCode': client.cookies['d_deviceCode'],
        'deviceType': 'Android'
    }
    data2 = {
        'methodType': 'iOSIntegralGet',
        'gameLevel': '1',
        'deviceType': 'iOS'
    }
    try:
        client.get('https://img.client.10010.com/gametask/index.html?yw_code=&desmobile='+username+'&version=android@8.0100')
        time.sleep(2)
        headers = {
            'origin': 'https://img.client.10010.com',
            'referer': 'https://img.client.10010.com/gametask/index.html?yw_code=&desmobile='+username+'&version=android@8.0100'
        }
        client.headers.update(headers)
        #进行游戏中心签到
        gameCenter = client.post('https://m.client.10010.com/producGame_signin', data=data1)
        gameCenter.encoding = 'utf-8'
        res1 = gameCenter.json()
        if res1['respCode'] == '0000' and res1['respDesc'] == '打卡并奖励成功':
            logging.info('【游戏中心签到】: ' + '获得' + str(res1['currentIntegral']) + '积分')
        elif res1['respCode'] == '0000':
            logging.info('【游戏中心签到】: ' + res1['respDesc'])
        time.sleep(1)
        #游戏频道积分
        gameCenter_exp = client.post('https://m.client.10010.com/producGameApp',data=data2)
        gameCenter_exp.encoding='utf-8'
        res2 = gameCenter_exp.json()
        if res2['code'] == '0000':
            logging.info('【游戏频道打卡】: 获得' + str(res2['integralNum']) + '积分')
        else:
            logging.info('【游戏频道打卡】: ' + res2['msg'])
        client.headers.pop('referer')
        client.headers.pop('origin')
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【游戏中心签到】: 错误，原因为: ' + str(e))

#每日领取100定向积分
#位置: 发现 --> 定向积分 --> 领取定向积分兑爆款
def day100Integral_task():
    data = {
        'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
    }
    try:
        integral = client.post('https://m.client.10010.com/welfare-mall-front/mobile/integral/gettheintegral/v1', data=data)
        integral.encoding = 'utf-8'
        res = integral.json()
        logging.info("【100定向积分】: " + res['msg'])
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【100定向积分】: 错误，原因为: ' + str(e))

#积分抽奖，可在环境变量中设置抽奖次数，否则每天将只会抽奖一次
#需要注意的是，配置完抽奖次数，程序每运行一次都将触发积分抽奖，直至达每日30次抽奖用完或积分不够(测试过程中未中过奖)
#位置: 发现 --> 定向积分 --> 小积分，抽好礼
def pointsLottery_task(n):
    try:
        numjsp = get_encryptmobile()
        #每日首次免费
        oneFree = client.post('https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp)
        oneFree.encoding = 'utf-8'
        res1 = oneFree.json()
        logging.info("【积分抽奖】: " + res1['RspMsg'] + ' x免费')
        #如果用户未设置此值，将不会自动抽奖
        #预防用户输入30以上，造成不必要的抽奖操作
        num = min(30,int(n))
        for i in range(num):
            #用积分兑换抽奖机会
            client.get('https://m.client.10010.com/dailylottery/static/integral/duihuan?goldnumber=10&banrate=30&usernumberofjsp=' + numjsp)
            #进行抽奖
            payx = client.post('https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp + '&flag=convert')
            payx.encoding = 'utf-8'
            res2 = payx.json()
            logging.info("【积分抽奖】: " + res2['RspMsg'] + ' x' + str(i+1))
            #等待随机秒钟
            time.sleep(5)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【积分抽奖】: 错误，原因为: ' + str(e))

#冬奥积分活动，第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底
#位置: 发现 --> 定向积分 --> 每日领积分超值兑东奥特许商品
def dongaoPoints_task():
    data = {
        'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
    }
    trance = [600,300,300,300,300,300,300]
    try:
        #领取积分奖励
        dongaoPoint = client.post('https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/getIntegral/v1', data=data)
        dongaoPoint.encoding = 'utf-8'
        res1 = dongaoPoint.json()
        #查询领了多少积分
        dongaoNum = client.post('https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/winterTwoShop/v1', data=data)
        dongaoNum.encoding = 'utf-8'
        res2 = dongaoNum.json()
        #领取成功
        if res1['resdata']['code'] == '0000':
            #当前为连续签到的第几天
            day = int(res2['resdata']['signDays'])
            #签到得到的积分
            point = trance[day%7] + 300 if day==1 else trance[day%7]
            logging.info('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + str(point) + '积分')
        else:
            logging.info('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + res2['resdata']['desc'])
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【东奥积分活动】: 错误，原因为: ' + str(e))

#读取用户配置信息
#错误原因有两种：格式错误、未读取到错误
def readJson():
    try:
        #用户配置信息
        with open('./config.json','r') as fp:
            users = json.load(fp)
            return users
    except Exception as e:
        print(traceback.format_exc())
        logging.error('账号信息获取失败错误，原因为: ' + str(e))
        logging.error('1.请检查是否在Secrets添加了账号信息，以及添加的位置是否正确。')
        logging.error('2.填写之前，是否在网站验证过Json格式的正确性。')

#获取积分余额
#分类：奖励积分、定向积分、通信积分
def getIntegral():
    try:
        integral = client.post('https://m.client.10010.com/welfare-mall-front/mobile/show/bj2205/v2/Y')
        integral.encoding = 'utf-8'
        res = integral.json()
        for r in res['resdata']['data']:
            if r['name'] != None and r['number'] != None:
                logging.info('【'+str(r['name'])+'】: ' + str(r['number']))
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【积分余额】: 错误，原因为: ' + str(e))

#获得我的礼包页面对象
def getQuerywinning(username):
    #获得我的礼包页面
    querywinninglist = client.get(
        'http://m.client.10010.com/myPrizeForActivity/querywinninglist.htm?yw_code=&desmobile='+str(username)+'&version=android@8.0100')
    querywinninglist.encoding = 'utf-8'
    #将页面格式化
    doc = f"""{querywinninglist.text}"""
    #转换为html对象
    html = fromstring(doc)
    return html

#存储并返回未使用的流量包
def getStorageFlow(username):
    #获得我的礼包页面
    html = getQuerywinning(username)
    #寻找ul下的所有li，在未使用流量包栏页面
    ul = html.xpath('/html/body/div[1]/div[7]/ul/li')
    #存储流量包数据
    datas = []
    #获得所有流量包的标识并存储
    for li in ul:
        data = {
            'activeCode': None,
            'prizeRecordID': None,
            'phone': None
        }
        tran = {1:'activeCode',2:'prizeRecordID',3:'phone'}
        line = li.attrib.get('onclick')
        #正则匹配字符串 toDetailPage('2534','20210307073111185674422127348889','18566669999');
        pattern = re.finditer(r'\'[\dA-Za-z]+\'',line)
        i = 1
        for match in pattern:
            data[tran[i]] = match.group()[1:-1]
            i = i + 1
        datas.append(data)
    return datas

#获取Asia/Shanghai时区时间戳
def getTimezone():
    timezone = pytz.timezone('Asia/Shanghai')
    dt = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

#获得流量包的还剩多长时间结束，返回形式时间戳
def getflowEndTime(username):
    #获得中国时间戳
    now = getTimezone()
    #获得我的礼包页面对象
    html = getQuerywinning(username)
    #获得流量包到期的时间戳
    endStamp = []
    endTime = html.xpath('/html/body/div[1]/div[7]/ul/li[*]/div[2]/p[3]')
    for end in endTime:
        #寻找起止时间间隔位置
        #end为空，可能无到期时间和开始时间
        end = end.text
        if end != None:
            index = end.find('-')+1
            #切割得到流量包失效时间
            end = end[index:index+10] + ' 23:59:59'
            end = end.replace('.','-')
            #将时间转换为时间数组
            timeArray = time.strptime(end, "%Y-%m-%d %H:%M:%S")
            #得到时间戳
            timeStamp = int(time.mktime(timeArray))
            endStamp.append(timeStamp-now)
        else:
            #将找不到结束时间的流量包设置为不激活
            endStamp.append(86401)
    return endStamp

#激活即将过期的流量包
def actionFlow(username):
    #获得所有未使用的流量包
    datas = getStorageFlow(username)
    #获得流量包还剩多长时间到期时间戳
    endTime = getflowEndTime(username)
    #流量包下标
    i = 0
    flag = True
    for end in endTime:
        #如果时间小于1天就激活
        #程序早上7：30运行，正好当天可使用
        if end < 86400:
            flag = False
            activeData = {
                'activeCode': datas[i]['activeCode'],
                'prizeRecordID': datas[i]['prizeRecordID'],
                'activeName': '做任务领奖品'
            }
            #激活流量包
            res = client.post('http://m.client.10010.com/myPrizeForActivity/myPrize/activationFlowPackages.htm',data=activeData)
            res.encoding = 'utf-8'
            res = res.json()
            if res['status'] == '200':
                logging.info('【即将过期流量包】: ' + '激活成功')
            else:
                logging.info('【即将过期流量包】: ' + '激活失败')
            time.sleep(8)
        i = i + 1
    if flag:
        logging.info('【即将过期流量包】: 暂无')

#每月领取1G流量包，仅限湖北用户
#位置：暂时不清楚
def monthOneG(username):
    #获取当前是本月几号
    now = getTimezone()
    timeArray = time.localtime(now)
    day = time.strftime("%d",timeArray)
    ## 联通活动 不需要登录
    url = f'https://wap.10010hb.net/zinfo/activity/mobilePrize/getAward?serialNumber={username}'
    #每月3号领取
    if day==3:
        award = client.post(url,'{}')
        award.encoding = 'utf-8'
        res = award.json()
        logging.info('【每月领取1G】: ' + res['alertMsg'])

#自动续约王卡福利二选一 初步每个月执行一次
def autoKingCardWelfare(upgradeType):
    #获取当前是本月几号
    now = getTimezone()
    timeArray = time.localtime(now)
    day = time.strftime("%d",timeArray)
    url = "https://m.client.10010.com/mobileService/businessTransact/tencentCardUpgradeChg.htm"
    data = {
        'upgradeType': upgradeType
    }
    arr = {
        1 : "100分钟通话",
        2 : "1G流量月包"
    }
    #每月4号领取
    if day==3:
        stat = client.post(url,data=data)
        stat.encoding = 'utf-8'
        stat = stat.json()
        try:
            if len(stat['content']) != 0:
                if 'ok' == stat['msg']:
                    logging.info('【王卡福利续约】: 成功, ' + arr[upgradeType])
                else:
                    logging.info('【王卡福利续约】: 失败, ' + stat['msg'])
            else:
                logging.info('【王卡福利续约】: 失败, ' + stat['msg'])
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【王卡福利续约】: 错误, ' + stat['msgStr'])

#腾讯云函数入口
def main(event, context):
    users = readJson()
    for user in users:
        #清空上一个用户的日志记录
        open('./log.txt',mode='w',encoding='utf-8')
        global client
        client = login.login(user['username'],user['password'],user['appId'])
        if client != False:
            getIntegral()
            daySign_task(user['username'])
            luckDraw_task()
            if ('lotteryNum' in user):
                pointsLottery_task(user['lotteryNum'])
            else:
                pointsLottery_task(0)
            day100Integral_task()
            dongaoPoints_task()
            gameCenterSign_Task(user['username'])
            woTree_task()
            actionFlow(user['username'])
            monthOneG(user['username'])
            if ('autoKingCardType' in user) :
                autoKingCardWelfare(user['autoKingCardType'])
        if ('email' in user) :
            notify.sendEmail(user['email'])
        if ('dingtalkWebhook' in user) :
            notify.sendDing(user['dingtalkWebhook'])
        if ('telegramBot' in user) :
            notify.sendTg(user['telegramBot'])
        if ('pushplusToken' in user) :
            notify.sendPushplus(user['pushplusToken'])
        if('enterpriseWechat' in user) :
            notify.sendWechat(user['enterpriseWechat'])
        if('IFTTT' in user) :
            notify.sendIFTTT(user['IFTTT'])
        if('Bark' in user) :
            notify.sendBark(user['Bark'])

#主函数入口
if __name__ == '__main__':
    main("","")
