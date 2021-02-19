# -*- coding: utf-8 -*-
# @Time    : 2021/2/15 06:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com

import requests,json,time,re,login,logging,traceback,os,random,notify

#用户登录
client = login.login()

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
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【沃之树】: 错误，原因为: ' + str(e))

#经多次测试，都可加倍成功了
#每日签到，1积分 +4 积分(翻倍)，第七天得到 1G 日包
#位置: 我的 --> 我的金币
def daySign_task():
    try:
        #参考同类项目 HiCnUnicom 待明日验证是否能加倍成功
        client.headers.update({'referer': 'https://img.client.10010.com/activitys/member/index.html'})
        param = 'yw_code=&desmobile=' + os.environ.get('USERNAME_COVER') + '&version=android@$8.0100'
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
        doubleAd = client.post('https://act.10010.com/SigninApp/signin/bannerAdPlayingLogo')
        client.headers.pop('referer')
        doubleAd.encoding='utf-8'
        res1 = daySign.json()
        res2 = doubleAd.json()
        if res1['status'] == '0000':
            logging.info('【每日签到】: ' + '打卡成功,' + res2['data']['statusDesc'])
        elif res1['status'] == '0002':
            logging.info('【每日签到】: ' + res1['msg'])
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
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日签到】: 错误，原因为: ' + str(e))

#游戏任务中心每日打卡领积分，游戏任务自然数递增至7，游戏频道每日1积分
#位置: 首页 --> 游戏 --> 每日打卡
def gameCenterSign_Task():
    data1 = {
        'methodType': 'signin',
        'clientVersion': '8.0100',
        'deviceType': 'Android'
    }
    data2 = {
        'methodType': 'iOSIntegralGet',
        'gameLevel': '1',
        'deviceType': 'iOS'
    }
    try:
        #游戏任务积分
        gameCenter = client.post('https://m.client.10010.com/producGame_signin', data=data1)
        gameCenter.encoding='utf-8'
        res = gameCenter.json()
        if res['respCode'] == '0000' and res['respDesc'] == '打卡并奖励成功':
            logging.info('【游戏中心签到】: ' + '获得' + str(res['currentIntegral']) + '积分')
        elif res['respCode'] == '0000':
            logging.info('【游戏中心签到】: ' + res['respDesc'])
        
        #游戏频道积分
        gameCenter_exp = client.post('https://m.client.10010.com/producGameApp',data=data2)
        gameCenter_exp.encoding='utf-8'
        res1 = gameCenter_exp.json()
        if res1['code'] == '0000':
            logging.info('【游戏频道打卡】: 获得' + str(res1['integralNum']) + '积分')
        else:
            logging.info('【游戏频道打卡】: ' + res1['msg'])
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【游戏中心签到】: 错误，原因为: ' + str(e))

#开宝箱，赢话费任务 100M 流量
#位置: 首页 --> 游戏 --> 每日打卡 --> 宝箱任务
def openBox_task():
    data1 = {
        'thirdUrl': 'https://img.client.10010.com/shouyeyouxi/index.html#/youxibaoxiang'
    }
    data2 = {
        'methodType': 'reward',
        'deviceType': 'Android',
        'clientVersion': '8.0100',
        'isVideo': 'Y'
    }
    data3 = {
        'methodType': 'taskGetReward',
        'taskCenterId': '187',
        'clientVersion': '8.0100',
        'deviceType': 'Android'
    }
    try:
        #在分类中找到宝箱并开启
        box = client.post('https://m.client.10010.com/mobileService/customer/getShareRedisInfo.htm', data=data1)
        box.encoding='utf-8'
        #观看视频领取更多奖励
        watchAd = client.post('https://m.client.10010.com/game_box', data=data2)
        watchAd.encoding='utf-8'
        #完成任务领取100M流量
        drawReward = client.post('https://m.client.10010.com/producGameTaskCenter', data=data3)
        drawReward.encoding='utf-8'
        res = drawReward.json()
        if res['code'] == '0000':
            logging.info('【100M寻宝箱】: ' + '获得100M流量')
        else:
            logging.info('【100M寻宝箱】: ' + '任务失败')
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【100M寻宝箱】: 错误，原因为: ' + str(e))

#领取 4G 流量包任务，看视频、下载软件每日可获得 240M 流量
#位置: 我的 --> 我的金币 --> 4G流量包
def collectFlow_task():
    data1 = {
        'stepflag': '22'
    }
    
    data2 = {
        'stepflag': '23'
    }
    try:
        for i in range(3):
            #看视频
            watchVideo = client.post('https://act.10010.com/SigninApp/mySignin/addFlow',data1)
            watchVideo.encoding='utf-8'
            res1 = watchVideo.json()
            if res1['reason'] == '00':
                logging.info('【4G流量包-看视频】: 获得' + res1['addNum'] + 'M流量 x' + str(i+1))
            elif res1['reason'] == '01':
                logging.info('【4G流量包-看视频】: 已完成' + ' x' + str(i+1))
            #下软件
            downloadProg = client.post('https://act.10010.com/SigninApp/mySignin/addFlow',data2)
            downloadProg.encoding='utf-8'
            res2 = downloadProg.json()
            if res2['reason'] == '00':
                logging.info('【4G流量包-下软件】: 获得' + res2['addNum'] + 'M流量 x' + str(i+1))
            elif res2['reason'] == '01':
                logging.info('【4G流量包-下软件】: 已完成' + ' x' + str(i+1))
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【4G流量包】: 错误，原因为: ' + str(e))

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
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【100定向积分】: 错误，原因为: ' + str(e))

#积分抽奖，可在环境变量中设置抽奖次数，否则每天将只会抽奖一次
#需要注意的是，配置完抽奖次数，程序每运行一次都将触发积分抽奖，直至达每日30次抽奖用完或积分不够(测试过程中未中过奖)
#位置: 发现 --> 定向积分 --> 小积分，抽好礼
def pointsLottery_task():
    try:
        numjsp = get_encryptmobile()
        #每日首次免费
        oneFree = client.post('https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp)
        oneFree.encoding = 'utf-8'
        res1 = oneFree.json()
        logging.info("【积分抽奖】: " + res1['RspMsg'] + ' x免费')
        num = 0
        #如果用户未设置此值，将不会自动抽奖
        if len(os.environ.get('LOTTERY_NUM')) != 0:
            num = int(os.environ.get('LOTTERY_NUM'))
        for i in range(num):
            #用积分兑换抽奖机会
            client.get('https://m.client.10010.com/dailylottery/static/integral/duihuan?goldnumber=10&banrate=30&usernumberofjsp=' + numjsp)
            #进行抽奖
            payx = client.post('https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp + '&flag=convert')
            payx.encoding = 'utf-8'
            res2 = payx.json()
            logging.info("【积分抽奖】: " + res2['RspMsg'] + ' x' + str(i+1))
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【积分抽奖】: 错误，原因为: ' + str(e))

#冬奥积分活动，第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底
#位置: 发现 --> 定向积分 --> 每日领积分超值兑东奥特许商品
def dongaoPoints_task():
    data = {
        'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
    }
    trance = [0,600,300,300,300,300,300,600]
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
            logging.info('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + str(trance[int(res2['resdata']['signDays'])]) + '积分')
        else:
            logging.info('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + res2['resdata']['desc'])
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【东奥积分活动】: 错误，原因为: ' + str(e))

if __name__ == '__main__':
    if client != False:
        daySign_task()
        luckDraw_task()
        pointsLottery_task()
        gameCenterSign_Task()
        day100Integral_task()
        dongaoPoints_task()
        woTree_task()
        openBox_task()
        collectFlow_task()
    if len(os.environ.get('EMAIL_COVER')) != 0:
        notify.sendEmail()