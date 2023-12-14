#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author : zhibo.wang
# E-mail : gm.zhibo.wang@gmail.com
# Date   :
# Desc   :



import re
import json
import time
import base64
import random
import hashlib
import plugins
import requests
from Crypto.Cipher import AES
from fake_useragent import UserAgent
from bridge.reply import Reply, ReplyType
from plugins import *


@plugins.register(
    name="Xinuo",                         # 插件的名称
    desire_priority=1,                    # 插件的优先级
    hidden=False,                         # 插件是否隐藏
    desc="个人开发的一些常用工具",        # 插件的描述
    version="0.0.3",                      # 插件的版本号
    author="xinuo",                       # 插件的作者
)


class Xinuo(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        try:
            self.conf = super().load_config()
            self.linkai_user = self.conf["linkai_user"]
            self.linkai_pwd = self.conf["linkai_pwd"]
            self.linkai_authorization = ""
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
        elif content[:2] == "翻译":
            fanyi_text = content[2:]
            msg = self.youdao_fanyi()
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "翻译\n"
            reply.content += f"{msg}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content == "测试":
            # msg = self.linkai_balance()
            msg = "测试"
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "测试\n"
            reply.content += f"{msg}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def get_help_text(self, verbose=False, **kwargs):
        help_text = "发送关键词执行对应操作\n"
        if not verbose:
            return help_text
        help_text += "输入 'linkai签到'， 进行签到\n"
        help_text += "输入 'linkai积分'， 进行总积分获取\n"
        help_text += "输入 '测试'， 测试\n"
        return help_text


    def random_user_agent(self):
        U = UserAgent()
        return U.random

    def random_youdao_cookie(self):
        user_id = random.randrange(100000000, 999999999)
        ip_address = ".".join(str(random.randrange(0, 256)) for _ in range(4))
        cookie = f"OUTFOX_SEARCH_USER_ID={user_id}@{ip_address}"
        return cookie

    def youdao_fanyi(self, fanyi_text):
        msg = ''
        try:
            cookie = self.random_youdao_cookie()
            ua = self.random_user_agent()
            headers = {
                'user-agent': ua,
                'Cookie': cookie,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://fanyi.youdao.com',
                'Referer': 'https://fanyi.youdao.com/',
                'Host': 'dict.youdao.com',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
            mysticTime = str(int(time.time() * 1000))
            url = 'https://dict.youdao.com/webtranslate'
            client = "fanyideskweb"
            keyid = "webfanyi"
            pointParam = "client,mysticTime,product"
            appVersion = "1.0.0"
            vendor = "web"
            keyfrom = "fanyi.web"
            key_ = 'fsdsogkndfokasodnaso'
            encoding='gb18030'
            md5_text = f'client={client}&mysticTime={mysticTime}&product={keyid}&key={key_}'
            md5 = hashlib.md5(md5_text.encode(encoding)).hexdigest()
            payload = {
                'i': fanyi_text,
                'from': 'auto',
                'to': '',
                'domain': '0',
                'dictResult': 'true',
                'keyid': keyid,
                'sign': md5,
                'client': client,
                'product': keyid,
                'appVersion': appVersion,
                'vendor': vendor,
                'pointParam': pointParam,
                'mysticTime': mysticTime,
                'keyfrom': keyfrom,
                'mid': '1',
                'screen': '1',
                'model': '1',
                'network': 'wifi',
                'abtest': '0',
                'yduuid': 'abcdefg',
            }
            response = requests.post(url, data=payload, headers= headers)
            r_code = response.status_code
            if r_code == 200:
                res_text = response.text
                decodeiv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
                decodekey = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
                key = hashlib.md5(decodekey.encode(encoding=encoding)).digest()
                iv = hashlib.md5(decodeiv.encode(encoding=encoding)).digest()
                aes_en = AES.new(key, AES.MODE_CBC, iv)
                data_new = base64.urlsafe_b64decode(res_text)
                result_text = aes_en.decrypt(data_new).decode('utf-8')
                remove_text = "}".join(result_text.split("}")[:-1]) + "}"
                res_json = json.loads(remove_text)
                """
                {
                   "code":0,
                   "dictResult":{

                   },
                   "translateResult":[
                       [
                           {
                               "tgt":"Automatic production test",
                               "src":"自动生编测试",
                               "srcPronounce":"zì dòng shēng biān cèshì"
                           }
                       ]
                   ],
                   "type":"zh-CHS2en"
               }
                """
                r_json_code = res_json.get("code")
                if r_json_code == 0:
                    translateResult = res_json.get("translateResult")
                    if len(translateResult) > 0:
                        end_fanyi  = translateResult[0].get("tgt")
                        if end_fanyi:
                            msg = f"数据解析失败: {translateResult[0]}"
                        else:
                            msg = f"数据解析失败: {translateResult}"
                    else:
                        msg = f"原始本文:{fanyi_text}\n翻译后文本:{end_fanyi}"
                else:
                    msg = f"返回状态码异常 code:{r_json_code}"
            else:
                msg = f"请求状态码异常 code:{r_code}"
        except Exception as e:
            logger.error(f"有道翻译 {e}")
            msg = "有道翻译 服务器内部错误"
        return msg


    def link_ai_login(self):
        # linkai 登录
        token = ""
        try:
            url = "https://link-ai.tech/api/login"
            payload = f"username={self.linkai_user}&password={self.linkai_pwd}"
            headers = {
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
              'Accept': 'application/json, text/plain, */*',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Accept-Encoding': 'gzip, deflate, br',
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
              'Authorization': 'Bearer',
              'Origin': 'https://link-ai.tech',
              'Connection': 'keep-alive',
              'Referer': 'https://link-ai.tech/console/factory',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin'
            }
            response = requests.request("POST", url, headers=headers,
                                        data=payload, timeout=20)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("code") == 200:
                    token = res_json.get("data").get("token")
                    if token:
                        msg = f"linkai登录成功token: {token}"
                        self.linkai_authorization = f"Bearer {token}"
                        logger.info(msg)
                else:
                    message = res_json.get("message")
                    msg = f"linkai登录失败:{message}"
                    logger.info("linkai登录失败 req content:{}".format(response.text))
            else:
                r_code = response.status_code
                msg = f"linkai登录失败 response status_code:{r_code}"
                logger.info(msg)
        except Exception as e:
            logger.error(f"linkai 登录 {e}")
        return token


    def linkai_sign_in(self):
        # linkai 每日签到
        msg = ""
        try:
            if self.linkai_authorization == "":
                logger.info("linkai token 不存在将执行登录操作")
                self.link_ai_login()
            for i in range(2):
                url = "https://chat.link-ai.tech/api/chat/web/app/user/sign/in"
                payload = {}
                headers = {
                  'Accept': 'application/json, text/plain, */*',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Authorization': self.linkai_authorization,
                  'Connection': 'keep-alive',
                  'Referer': 'https://chat.link-ai.tech/home',
                  'Sec-Fetch-Dest': 'empty',
                  'Sec-Fetch-Mode': 'cors',
                  'Sec-Fetch-Site': 'same-origin',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                  'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Linux"'
                }
                response = requests.request("GET", url, headers=headers,
                                            data=payload, timeout=20)
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
                    break
                else:
                    r_code = response.status_code
                    msg = f"linkai签到失败 response status_code:{r_code}"
                    logger.info(msg)
                    # 重新获取 token
                    time.sleep(2)
                    self.link_ai_login()
                time.sleep(2)
        except Exception as e:
            logger.error(f"linkai 积分签到 {e}")
            msg = "linkai签到失败 服务器内部错误"
        return msg

    def linkai_balance(self):
        # linkai 总积分查看
        msg = ""
        try:
            if self.linkai_authorization == "":
                logger.info("linkai token 不存在将执行登录操作")
                self.link_ai_login()
            for i in range(2):
                url = "https://chat.link-ai.tech/api/chat/web/app/user/get/balance"
                payload = {}
                headers = {
                  'Accept': 'application/json, text/plain, */*',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Authorization': self.linkai_authorization,
                  'Connection': 'keep-alive',
                  'Host': 'chat.link-ai.tech',
                  'Referer': 'https://chat.link-ai.tech/console/account',
                  'Sec-Fetch-Dest': 'empty',
                  'Sec-Fetch-Mode': 'cors',
                  'Sec-Fetch-Site': 'same-origin',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                  'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Linux"'
                }
                response = requests.request("GET", url, headers=headers,
                                            data=payload, timeout=20)
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
                    break
                else:
                    r_code = response.status_code
                    msg = f"linkai获取积分失败 response status_code:{r_code}"
                    logger.info(msg)
                    # 重新获取 token
                    time.sleep(2)
                    self.link_ai_login()
                time.sleep(2)
        except Exception as e:
            logger.error(f"linkai 总积分查看 {e}")
            msg = "linkai获取积分失败 服务器内部错误"
        return msg
