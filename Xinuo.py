#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author : zhibo.wang
# E-mail : gm.zhibo.wang@gmail.com
# Date   :
# Desc   :



import requests
import json
import re
import plugins
from bridge.reply import Reply, ReplyType
from plugins import *


@plugins.register(
    name="Xinuo",                         # 插件的名称
    desire_priority=1,                    # 插件的优先级
    hidden=False,                         # 插件是否隐藏
    desc="个人开发的一些常用工具",        # 插件的描述
    version="0.0.2",                      # 插件的版本号
    author="xinuo",                       # 插件的作者
)


class Xinuo(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        try:
            self.conf = super().load_config()
            self.authorization = self.conf["linkai_authorization"]
            self.cookie = self.conf["linkai_cookie"]
            print("[Xinuo] inited")
        except:
            raise self.handle_error(e, "[Xinuo] init failed, ignore ")


    def on_handle_context(self, e_context: EventContext):
        content = e_context["context"].content
        if content == "linkai签到":
            msg = self.linkai_sign_in()
            reply = Reply()  # 创建回复消息对象
            reply.type = ReplyType.TEXT  # 设置回复消息的类型为文本
            reply.content = "linkai签到\n"  # 设置回复消息的内容
            reply.content += f"{msg}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content == "linkai积分":
            msg = self.linkai_balance()
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "linkai积分\n"
            reply.content += f"{msg}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS


    def get_help_text(self, **kwargs):
        help_text = "发送关键词执行对应操作\n"
        help_text += "输入 'linkai签到'， 将进行linkai每日积分签到操作\n"
        help_text += "输入 'linkai积分'， 将进行linkai积分获取操作\n"
        return help_text


    def linkai_sign_in(self):
        msg = ""
        try:
            url = "https://chat.link-ai.tech/api/chat/web/app/user/sign/in"
            payload = {}
            headers = {
              'Accept': 'application/json, text/plain, */*',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Authorization': self.authorization,
              'Connection': 'keep-alive',
              'Cookie': self.cookie,
              'Referer': 'https://chat.link-ai.tech/home',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
              'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
              'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"Linux"'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("code") == 200:
                    score = res_json.get("data").get("score")
                    msg = f"linkai签到成功获得积分:{score}"
                    logger.info(msg)
                else:
                    message = res_json.get("message")
                    msg = f"linkai签到失败:{message}"
                    logger.info("linkai签到失败 req content:{}".format(response.text))
            else:
                r_code = response.status_code
                msg = f"linkai签到失败 response status_code:{r_code}"
                logger.info(msg)
        except:
            msg = "linkai签到失败 服务器内部错误"
        return msg

    def linkai_balance(self):
        msg = ""
        try:
            url = "https://chat.link-ai.tech/api/chat/web/app/user/get/balance"
            payload = {}
            headers = {
              'Accept': 'application/json, text/plain, */*',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Authorization': self.authorization,
              'Connection': 'keep-alive',
              'Host': 'chat.link-ai.tech',
              'Cookie': self.cookie,
              'Referer': 'https://chat.link-ai.tech/console/account',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
              'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
              'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"Linux"'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("code") == 200:
                    score = res_json.get("data").get("score")
                    msg = f"linkai总积分:{score}"
                    logger.info(msg)
                else:
                    message = res_json.get("message")
                    msg = f"linkai获取积分失败:{message}"
                    logger.info("linkai获取积分失败 req content:{}".format(response.text))
            else:
                r_code = response.status_code
                msg = f"linkai获取积分失败 response status_code:{r_code}"
                logger.info(msg)
        except:
            msg = "linkai获取积分失败 服务器内部错误"
        return msg
