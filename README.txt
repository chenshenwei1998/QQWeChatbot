QQ群微信群消息转发机器人
本程序基于Mojo-WebQQ和Mojo-Weixin提供的API运行
环境为Ubuntu16.04和Python3.5（其他环境亦可运行）

实现功能：
1.微信QQ群聊消息转发，可以连接任意数量的群

2.群发消息，可以选择任意数量的群进行通知转发

3.添加/删除特别关心功能，若关注对象在任意群中发送消息，则会以QQ消息形式提醒管理员

4.保存聊天记录，机器人启动后所有群的聊天记录将保存在群昵称.txt文件中

5.管理员可通过消息形式与机器人交互

使用方法
1.首先需要准备QQ和微信的机器人账号，QQ注册新账号即可，微信由于腾讯官方限制新注册账号已无法使用基于Web微信的Mojo-Weixin，因此只能使用老账号，机器人必须加入需要转发消息的群

2.安装Mojo-WebQQ和Mojo-Weixin(请在root用户环境下安装)

（1）安装Perl（一般Linux会自带）
apt-get install perl

（2）安装cpanm包管理工具
cpan -i App::cpanminus

（3）安装依赖包
apt-get install libssl-dev

（4）安装Mojo-WebQQ和Mojo-Weixin
cpanm Mojo::Webqq
cpanm Mojo::Weixin

（5）官方包可能不是最新，需要下载最新源码更新一下
git clone https://github.com/sjdy521/Mojo-Webqq
cd Mojo-Webqq
perl Makefile.PL
make install

3.本程序中用到了wsgiref库，而在python3中此库有bug，需要修正（需要在root环境下）
找到python的库文件所在位置，一般在/usr/lib/python中
vi /usr/usr/python/wsgiref/handlers.py

大约在169行左右，finish_response()方法中，在self.write(data)上面加上data=data.encode(),保存退出
（修改过的handlers.py已经放在代码文件夹中，也可以直接复制过去覆盖原文件）

4.运行mojoqq.pl和mojoweixin.pl，扫描二维码登录QQ和微信的机器人账号，二维码图片在/tmp文件夹中，如使用远程服务器，建议使用FileZilla等软件从远程服务器上下载二维码进行扫描登录

perl mojoqq.pl
###略去登录信息###

perl mojoweixin.pl
###略去登录信息###

5.运行main.py，开启机器人

python main.py
输入qq管理员昵称，回车，即可启动机器人