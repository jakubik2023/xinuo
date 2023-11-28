### chatgpt-on-wechat  插件

```
目前有
linkai积分签到
linkai总积分查看
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
