# -*- coding: utf-8 -*-
# @Time    : 2021/2/15 06:00
# @Author  : srcrs
# @Email   : srcrs@foxmail.com

import base64,rsa,time,requests,logging,traceback,os

#日志基础配置
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('log.txt', mode='w', encoding='utf-8')
fh.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(fh)
# 创建一个handler，输出到控制台
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("[%(asctime)s]:%(levelname)s:%(message)s"))
logger.addHandler(ch)

#自动保存会话
session = requests.Session()

#获取公钥的key
def str2key(s):
    # 对字符串解码
    b_str = base64.b64decode(s)

    if len(b_str) < 162:
        return False

    hex_str = ''

    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]

    return modulus,exponent

#对手机号和登录密码进行加密
def encryption(message,key):
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    crypto = rsa.encrypt(message, rsa_pubkey)
    b64str = base64.b64encode(crypto)
    return b64str

#进行登录
#手机号和密码加密代码，参考自这篇文章 http://www.bubuko.com/infodetail-2349299.html?&_=1524316738826
def login():
    #rsa 公钥
    pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB"
    #获取公钥的 key
    key = str2key(pubkey)
    #这里对手机号和密码加密，传入参数需是 byte 类型
    username = encryption(str.encode(os.environ.get('USERNAME_COVER')),key)
    password = encryption(str.encode(os.environ.get('PASSWORD_COVER')),key)
    #appId 联通后端会验证这个值,如不是常登录设备会触发验证码登录
    appId = os.environ.get('APPID_COVER')
    #设置一个标志，用户是否登录成功
    flag = False
    
    cookies = {
        'c_sfbm': '234g_00',
        'logHostIP': 'null',
        'route': 'cc3839c658dd60cb7c25f6c2fe6eb964',
        'channel': 'GGPD',
        'city': '076|776',
        'devicedId': 'B97CDE2A-D435-437D-9FEC-5D821A012972',
        'mobileService1': 'ProEsSI6SM4DbWhaeVsPtve9pu7VWz0m94giTHkPBl40Gx8nebgV!-1027473388',
        'mobileServiceAll': 'a92d76b26705a45a087027f893c70618',
    }
    
    headers = {
        'Host': 'm.client.10010.com',
        'Accept': '/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': 'ChinaUnicom4.x/3.0 CFNetwork/1197 Darwin/20.0.0',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'deflate, br',
        'Content-Length': '891',
    }
    
    data = {
        'reqtime': round(time.time()*1000),
        'simCount': '1',
        'version': 'iphone_c@8.0004',
        'mobile': username,
        'netWay': 'wifi',
        'isRemberPwd': 'false',
        'appId': appId,
        'deviceId': 'b61f7efcba733583170df52d8f2f9f87521b3844d01ccbc774bbfa379eaeb3fa',
        'pip': '192.168.1.4',
        'password': password,
        'deviceOS': '14.0.1',
        'deviceBrand': 'iphone',
        'deviceModel': 'iPad',
        'remark4': '',
        'keyVersion': '',
        'deviceCode': 'B97CDE2A-D435-437D-9FEC-5D821A012972'
    }
    
    response = session.post('https://m.client.10010.com/mobileService/login.htm', headers=headers, cookies=cookies, data=data)
    response.encoding='utf-8'
    try:
        result = response.json()
        if result['code'] == '0':
            logger.info('【登录】: ' + result['default'][-4:])
            session.headers.update({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 unicom{version:iphone_c@8.0100}{systemVersion:dis}{yw_code:}'})
            flag = True
        else:
            logger.info('【登录】: ' + result['dsc'])
    except Exception as e:
        print(traceback.format_exc())
        logger.error('【登录】: 发生错误，原因为: ' + str(e))
    if flag:
        return session
    else:
        return False
    
