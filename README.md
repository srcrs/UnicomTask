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
  - [1.邮箱](#1邮箱)
  - [2.钉钉机器人](#2钉钉机器人)
  - [3.TgBot机器人](#3tgbot机器人)
- [同步上游代码](#同步上游代码)
- [申明](#申明)
- [参考项目](#参考项目)

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
