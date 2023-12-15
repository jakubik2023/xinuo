### chatgpt-on-wechat  插件

```
目前有
linkai积分签到
linkai总积分查看
翻译   // 逆向破解有道翻译接口   翻译+要翻译的内容 + 是连接起来不是添加+这个符号
       // 需要安装 pip install fake-useragent、  pycryptodome


配合定时任务timetask 运行  完美!!!
```

```
克隆代码到插件目录 或者

安装仓库源记录的插件：#installp xinuo
安装指定仓库的插件：#installp https://github.com/wang-zhibo/xinuo.git 


cp config.example.json config.json

修改 config.json 文件
填入 帐号密码

{
  "linkai_user": "xxxxxxxxxxxxxx",
  "linkai_pwd": "xxxxxxxxxx"
}

```

```
#scanp

#enablep xinuo


log

[INFO][2023-11-28 10:04:16][Xinuo.py:214] - linkai token 不存在将执行登录操作
[INFO][2023-11-28 10:04:17][Xinuo.py:146] - linkai登录成功token: xxxxxxxxxxxxxxxxxxxxxxxx
[INFO][2023-11-28 10:04:17][Xinuo.py:240] - linkai总积分:23411
[INFO][2023-11-28 10:04:17][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=[🫶] linkai积分
linkai总积分:23411), receiver=@1d6231b36d7eb3b0fc35d5458ceae3478113062683aa812c12f69790017d0655
[INFO][2023-11-28 10:04:38][Xinuo.py:194] - linkai签到失败 req content:{"success":false,"code":834,"message":"今日已签到，请明日再来！","data":null}
[INFO][2023-11-28 10:04:39][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=[🫶] linkai签到
linkai签到失败:今日已签到，请明日再来！), receiver=@1d6231b36d7eb3b0fc35d5458ceae3478113062683aa812c12f69790017d0655



[INFO][2023-12-15 16:20:47][Xinuo.py:89] - 有道翻译: 翻译一只桔黄色的猫
[INFO][2023-12-15 16:20:47][Xinuo.py:227] - 有道翻译: [[{'tgt': 'An orange cat', 'src': '一只桔黄色的猫', 'srcPronounce': 'yī zhī jié huáng sè demāo'}]]
[INFO][2023-12-15 16:20:47][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=[🫶] 翻译
原始本文:一只桔黄色的猫
翻译后文本:An orange cat), receiver=@ee2a5dbeb0895072ec88005c9bcc36c68af9a959847ff3b1c325fbbcb3bc5449




1: 
input->
    linkai签到
output->
    linkai签到失败:今日已签到，请明日再来！
    linkai签到成功获得积分:123

2:
input->
    linkai积分
output->
    linkai积分
    linkai总积分:10405
```
