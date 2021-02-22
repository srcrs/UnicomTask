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

👯✨📫

联通手机营业厅自动完成每日任务，领流量、签到获取积分等，月底流量不发愁。

# 功能

* [x] 沃之树领流量、浇水(12M日流量)
* [x] 每日签到(1积分+翻倍4积分+第七天1G流量日包)
* [x] 天天抽奖，每天三次免费机会(随机奖励)
* [x] 游戏中心每日打卡(连续打卡，积分递增至最高7，第七天1G流量日包)
* [x] 游戏中心宝箱100M任务(100M日流量+随机奖励并翻倍)
* [x] 4G流量包看视频、下软件任务(90M+150M七日流量)
* [x] 每日领取100定向积分 
* [x] 积分抽奖，每天最多抽30次(中奖几率渺茫)
* [x] 冬奥积分活动(第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底)
* [x] 邮件、钉钉推送运行结果

# Github Actions 部署方法

## 1.fork本项目

项目地址：[srcrs/UnicomTask](https://github.com/srcrs/UnicomTask)

![](https://draw-static.vercel.app/UnicomTask/fork本项目.gif)

## 2.准备需要的参数

手机号、服务密码、appID。

其中appId的获取:

+ 安卓用户可在文件管理 --> Unicom/appid 文件中获取。

+ 苹果用户可抓取客户端登录接口获取。
> `https://m.client.10010.com/mobileService/login.htm`
 
## 3.将必要参数填到Secrets

在`Secrets`中的`Name`和`Value`格式如下：

Name | Value | 说明
-|-|-
USERNAME_COVER | 18566669999 | 手机号(必须)
PASSWORD_COVER | 123456 | 服务密码(必须)
APPID_COVER | xxxxxxxxx | appId(必须)
EMAIL_COVER | xxxxx@qq.com | 邮箱(可选)
LOTTERY_NUM | 填写正整数 | 抽奖次数(可选)
DINGTALK_WEBHOOK | https://oapi.dingtalk.com/robot/send?access_token=xxxx | 钉钉自定义机器人webhook(可选)

[钉钉自定义机器人使用方式](https://developers.dingtalk.com/document/app/custom-robot-access)，注意安全设置部分，选择自定义关键词，填写`UnicomTask`。

![](https://draw-static.vercel.app/UnicomTask/将参数填到Secrets中.gif)

## 4.开启Actions

默认`Actions`处于禁止状态，在`Actions`选项中开启`Actions`功能，把那个绿色的长按钮点一下。如果看到左侧工作流上有黄色`!`号，还需继续开启。

![](https://draw-static.vercel.app/UnicomTask/开启Actions.gif)

## 5.进行一次push操作

`push`操作会触发工作流运行。

删除掉`README.md`中的😄即可。完成后，每天早上`7:30`将自动完成每日任务。

![](https://draw-static.vercel.app/UnicomTask/进行一次push操作.gif)

# 同步上游代码

在最新的代码中，已经加上自动同步上游代码的action，将会定时在每周五16点执行，文件地址在`.github/workflows/auto_merge.yml`。

同时您也可以安装[pull](https://github.com/apps/pull)应用，也可实现自动同步上游代码。

# 申明

本项目仅用于学习。

# 参考项目

[mixool/HiCnUnicom](https://github.com/mixool/HiCnUnicom)，感谢该项目对于登录部分的思路
