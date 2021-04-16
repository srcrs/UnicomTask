<div align="center">
<h1 align="center">UnicomTask</h1>
<img src="https://img.shields.io/github/issues/srcrs/UnicomTask?color=green">
<img src="https://img.shields.io/github/stars/srcrs/UnicomTask?color=yellow">
<img src="https://img.shields.io/github/forks/srcrs/UnicomTask?color=orange">
<img src="https://img.shields.io/github/license/srcrs/UnicomTask?color=ff69b4">
<img src="https://img.shields.io/github/search/srcrs/UnicomTask/main?color=blue">
<img src="https://img.shields.io/github/v/release/srcrs/UnicomTask?color=blueviolet">
<img src="https://img.shields.io/github/languages/code-size/srcrs/UnicomTask?color=critical">
</div>

# 简介

👯✨😄📫

联通手机营业厅自动完成每日任务，领流量、签到获取积分等，月底流量不发愁。

开源不易，如果本项目对你有帮助，那么就请给个star吧。😄

# 目录

- [简介](#简介)
- [目录](#目录)
- [功能](#功能)
- [使用方式](#使用方式)
  - [Github Actions（推荐）](#github-actions推荐)
    - [1.fork本项目](#1fork本项目)
    - [2.准备需要的参数](#2准备需要的参数)
    - [3.将参数填到Secrets](#3将参数填到secrets)
    - [4.开启Actions](#4开启actions)
    - [5.进行一次push操作](#5进行一次push操作)
  - [腾讯云函数（推荐）](#腾讯云函数推荐)
    - [1.fork本项目](#1fork本项目-1)
    - [2.准备需要的参数](#2准备需要的参数-1)
    - [3.将参数填到Secrets](#3将参数填到secrets-1)
    - [4.部署](#4部署)
- [通知推送方式](#通知推送方式)
- [同步上游代码](#同步上游代码)
- [申明](#申明)
- [参考项目](#参考项目)

# 功能

* [x] 沃之树领流量、浇水(12M日流量)
* [x] 每日签到(1积分)
* [x] 天天抽奖，每天三次免费机会(随机奖励)
* [x] 游戏中心每日打卡(连续打卡，积分递增至最高7，第七天1G流量日包)
* [x] 游戏中心宝箱100M任务(任务过期)
* [x] 4G流量包看视频任务(失效)
* [x] 每日领取100定向积分 
* [x] 积分抽奖，每天最多抽30次(中奖几率渺茫)
* [x] 冬奥积分活动(第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底)
* [x] 获取每日1G流量日包(截止日期暂时不知道)
* [x] 邮件、钉钉、Tg、企业微信等推送运行结果
* [x] 自动激活即将过期流量包（到期时间1天内）
* [X] 每月领取1G流量包（过期）
* [X] 王卡每月自动激活福利二选一(需在配置项中配置需要激活哪个，每月3号) 

# 使用方式

## Github Actions（推荐）

### 1.fork本项目

项目地址：[srcrs/UnicomTask](https://github.com/srcrs/UnicomTask)

![](https://draw-static.vercel.app/UnicomTask/fork本项目.gif)

### 2.准备需要的参数

手机号、服务密码、`appId`。

其中`appId`的获取:

+ 安卓用户可在文件管理 --> `Unicom/appid` 文件中获取。

+ 苹果用户可抓取客户端登录接口获取。

> `https://m.client.10010.com/mobileService/login.htm`（解绑重新登录，在响应体中）

> `https://m.client.10010.com/mobileService/onLine.htm`（退出客户端重新进入，在请求体中）

> `http://m.client.10010.com/mobileService/customer/getclientconfig.htm?appId=xxx&mobile=yyy`（退出客户端重新进入，xxx就是）

> `https://m.client.10010.com/mobileService/customer/accountListData.htm`（退出客户端重新进入，在请求体中）

其中，后三个链接在安卓也是适用的。
 
### 3.将参数填到Secrets

在`Secrets`中的`Name`和`Value`格式如下：

Name | Value
-|-
USERS_COVER | config.json中内容

将`config.json`中内容复制下来，按照要求填写添加到`Secrets`中，如若选填内容不想配置，需将该行删除。如只想基本功能，无需通知和用积分抽奖，应填写如下内容：

```json
[
    {
        "username": "18566669999",
        "password": "123456",
        "appId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
]
```

填写之前完后，建议本地保存一份，方便下次填写。

注意`json`格式，最后一个要删掉逗号。建议在填写之前，使用[json校验工具](https://www.bejson.com/)进行校验。

注意：不要将个人信息填写到仓库`config.json`文件中（不要动这个文件就没事），以免泄露。

多账号，参考[关于多账号的使用方式](https://github.com/srcrs/UnicomTask/discussions/16)

![](https://draw-static.vercel.app/UnicomTask/将参数填到Secrets中.gif)

### 4.开启Actions

默认`Actions`处于禁止状态，在`Actions`选项中开启`Actions`功能，把那个绿色的长按钮点一下。如果看到左侧工作流上有黄色`!`号，还需继续开启。

![](https://draw-static.vercel.app/UnicomTask/开启Actions.gif)

### 5.进行一次push操作

`push`操作会触发工作流运行。

删除掉`README.md`中的😄即可。完成后，每天早上`6:30`将自动完成每日任务。

![](https://draw-static.vercel.app/UnicomTask/进行一次push操作.gif)

## 腾讯云函数（推荐）

### 1.fork本项目

项目地址：[srcrs/UnicomTask](https://github.com/srcrs/UnicomTask)

### 2.准备需要的参数

* 开通云函数 `SCF` 的腾讯云账号，在[访问秘钥页面](https://console.cloud.tencent.com/cam/capi)获取账号的 `TENCENT_SECRET_ID`，`TENCENT_SECRET_KEY`

> 注意！为了确保权限足够，获取这两个参数时不要使用子账户！此外，腾讯云账户需要[实名认证](https://console.cloud.tencent.com/developer/auth)。

* 依次登录 [SCF 云函数控制台](https://console.cloud.tencent.com/scf) 和 [SLS 控制台](https://console.cloud.tencent.com/sls) 开通相关服务，确保您已开通服务并创建相应[服务角色](https://console.cloud.tencent.com/cam/role) **SCF_QcsRole、SLS_QcsRole**

* 手机号，服务密码，appId等等（参考[2.准备需要的参数](#2准备需要的参数)）

### 3.将参数填到Secrets

`Name`和`Value`格式如下：
  
Name | Value
-|-
TENCENT_SECRET_ID | 腾讯云用户SecretID(需要主账户，子账户可能没权限)
TENCENT_SECRET_KEY | 腾讯云账户SecretKey
USERS_COVER | config.json中内容

如对于`Secrets`不知如何添加，参考[3.将参数填到Secrets](#3将参数填到secrets)

![](https://draw-static.vercel.app/UnicomTask/云函数添加Secrets.png)

### 4.部署

* 添加完上面`3`个`Secrets`后，进入`Actions`(上面那个不是`Secrets`下面那个) --> `deploy for serverless`，点击右边的`Run workflow`即可部署至腾讯云函数(如果出错请在红叉右边点击`deploy for serverless`查看部署任务的输出信息找出错误原因)。

* 首次`fork`可能要去`Actions`里面同意使用`Actions`条款，如果`Actions`里面没有`deploy for serverless`，点一下右上角的`star`，`deploy for serverless`就会出现在`Actions`里面。（参考[4.开启Actions](#4开启actions)）

还可本地部署到腾讯云，详情见 [云函数本地部署](https://github.com/srcrs/UnicomTask/discussions/140)。

# 通知推送方式

## 1.邮箱

本方式较简单，只需要填写邮箱即可，由于使用的是公共`API`接口，稳定性不高

## 2.钉钉机器人

钉钉群组自定义机器人，配置稍微复杂一些，但是稳定性高，使用方式参考如下：

[钉钉自定义机器人使用方式](https://developers.dingtalk.com/document/app/custom-robot-access)，注意安全设置部分，选择自定义关键词，填写`UnicomTask`。

## 3.TgBot机器人

类似于钉钉机器人，只需要一个`token`和`userId`，自行搜索这两个参数的获取方式。

## 4.pushplus机器人

类似于钉钉机器人，只需要一个`token`，参考[获取pushplus的token](http://www.pushplus.plus/login?redirectUrl=/message)。注意，升级到了新接口，要重新申请`token`。详情见：[更新推送加推送接口](https://github.com/srcrs/UnicomTask/issues/134)

## 5.企业微信应用通知

企业微信自建应用，可发送消息，并且可以不借助第三方，将消息转发到普通微信。用电脑，进行[企业微信登录](https://work.weixin.qq.com/wework_admin/loginpage_wx)，普通微信扫码也可登录，，按照[此教程](https://note.youdao.com/ynoteshare1/index.html?id=351e08a72378206f9dd64d2281e9b83b&type=note#/)获取需要的三个值。

## 6.IFTTT通知

通过触发IFTTT的Webhook Trigger来通知到其它任意服务，具体可以参照[IFTTT文档](https://ifttt.com/maker_webhooks)。

## 7.Bark通知

类似于钉钉机器人，只需要一个`Key`，IOS安装Bark即可获取Key[使用文档](https://github.com/Finb/Bark/blob/master/README.md)。

# 同步上游代码

## 将参数填到Secrets

> 注意！为了确保 Push 权限足够，需要 Github Personal access tokens

`token`获取方式如下：

1. [生成新的token](https://github.com/settings/tokens/new)，点击这个链接。
2. 为`token`设置名字，然后把`workflow`勾选上，点击最下方`Generate token`即可生成`token`。

在`Secrets`中的`Name`和`Value`格式如下：

Name | Value
-|-
TOKEN | Github Personal access tokens

在最新的代码中，已经加上自动同步上游代码的`Action`，将会定时在每周五`16`点执行，文件地址在`.github/workflows/auto_merge.yml`。

同时您也可以安装[pull](https://github.com/apps/pull)应用，也可实现自动同步上游代码。

# 申明

本项目仅用于学习。

# 参考项目

[mixool/HiCnUnicom](https://github.com/mixool/HiCnUnicom)，感谢该项目对于登录部分的思路

[happy888888/BiliExp](https://github.com/happy888888/BiliExp)，参考了该项目的云函数实现
