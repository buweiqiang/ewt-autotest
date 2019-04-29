开发环境准备
安装python：需要3.6以上的版本
安装开发工具：推荐pycharm

安装Git：https://git-scm.com/download
安装好Git后，配置用户名和用户邮箱
git config --global user.name "your_name"
git config --global user.email "your_email@gmail.com"

关于windows和linux系统提交代码的兼容问题：windows下的换行符为crlf（即\r\n），liunx和mac系统的换行符为lf（即\n）
Git默认配置中的core.autocrlf=ture，含意检出时将lf转化为crlf，提交将crlf转为lf，目的是在windows下开发时自动兼容在linux上开发和运行的工程
如果是针对windows操作系统开发的工程（如.net工程），则要关闭自动转换，即设置core.autocrlf=false
本自动化框架的目标运行环境是linux和windows系统，所以请保持core.autocrlf=ture
或者core.autocrlf=input，即提交时转换为lf，检出时不转换为crlf
操作命令为：git config core.autocrlf true/false/input

Git默认是大小写不敏感的，也就是说，将一个文件名某个字母做了大小写转换的修改Git是忽略这个改动的，导致在同步代码时候会出现错误，所以建议大小把Git设置成大小写敏感
git config core.ignorecase false

为了避免每次拉代码或提交都需要输入密码，需要配置密钥，提供公钥给远程仓库，本地保留私钥，用下面的命令生产密钥对（如果本地已有，不需要再次生成，直接用就可以）：
ssh-keygen -t rsa -C "your_email@youremail.com"
生成密钥后，在本地的/Users/当前电脑用户/.ssh目录下会生成两个文件id_rsa、id_rsa.pub，id_rsa文件保存的是私钥，保存于本地，id_rsa.pub文件保存的是公钥，需要将里面内容添加到远端仓库。

自动化框架设计
conf下面放所有的配置文件
conf/config.py封装了读取config的类和方法，采用单例加工厂的模式，不同的config类会依次读取global.cfg和相应cfg里的内容
global.cfg里面的配为全局配置，其他配置文件中的配置会继承和覆盖global.cfg里的配置
common下面放所有的公共方法
common/log.py封装了初始化logger的方法
common/helper里是常用的公共方法，如生成随机串，计算文件md5，字符串加密等
xxx_lib是具体业务线的接口库
xxx.py用来实现具体的接口请求，主要是参数，请求方法，请求结果的处理逻辑
*_urls.py用来存储接口的请求地址

测试用例都遵守*_test.py的命名规则，测试方法都遵守test_开头的规则
尽量不要改动TestData文件夹下的文件，因为git对每次改动都保留副本，频繁改动数据文件会导致git占用空间过多

HtmlRunner.py是用来执行测试用例的入口，使用示例如下：
python HtmlRunner.py tests/study_tests -p *test.py -m test_p1 -e sit
第一个参数tests/study_tests是指定测试用例所在的文件夹
第二个参数-p含义是指定测试用例文件名的匹配格式
第三个参数-m含义是指定测试方法名的匹配格式
第四个参数-e含义是指定测试执行的环境

有两种方式切换测试环境：
1. 在HtmlRunner.py执行时传入-e参数，这个只适用于用HtmlRunner启动测试的场景
2. 先切换环境：python conf/config.py {env}，再执行测试，这个适合任何方式启动的测试

依赖包安装：
首先确保已经安装了pip，如果没有，可以用sudo easy_intall pip安装
一键安装所有依赖的包：pip install -r requirements.txt

requests是必装的包：pip install requests
上传文件可安装requests帮助包requests-toolbelt
pip install requests-toolbelt
加解密需要安装pycrypto，但是pycrypto已经停止维护了，而且windows环境依赖Microsoft VC++ build tool才能安装成功
推荐安装pycryptodome，是pycrypto的延伸版，而且没有过分的依赖，十分好用
pip install pycryptodome
如果缺少其他的包，安装方法同上pip install package_name

有些包安装的比较慢，可以指定源安装：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
出错请尝试：pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
网上找到的国内源：
http://pypi.douban.com/simple/  豆瓣
http://pypi.hustunique.com/simple/  华中理工大学
http://pypi.sdutlinux.org/simple/  山东理工大学
http://pypi.mirrors.ustc.edu.cn/simple/  中国科学技术大学
http://pypi.v2ex.com/simple/simple/
http://mirrors.aliyun.com/pypi/simple/ 阿里云

升级包：pip install --upgrade package_name
卸载包：pip uninstall package_name

如果测试websocket长链接需要安装websocket-client，注意，不是websocket
pip install websocket-client

解析网页内容推荐安装BeautifulSoup4(bs4)，可选，只有很少的case用到
pip install beautifulsoup4
或先从这里下载：htps://www.crummy.com/software/BeautifulSoup/bs4/download/
再安装：python setup.py install
据说如果安装了lxml，beautifulsoup4解析html的效率会更好，可以选择性安装lxml
easy install lxml

数据库操作推荐安装mysql-connector
pip install mysql-connector==2.1.4
或从git下载安装mysql-connector-python
$  git clone https://github.com/mysql/mysql-connector-python.git
$  cd mysql-connector-python
$  python ./setup.py build
$  sudo python ./setup.py install

关于pyopenssl
有同学经常遇到https请求报ssl相关的Error，安装pyopenssl后有可能解决问题：sudo pip install pyopenssl
如果pip安装不成功，可以尝试下载tar包可whl包安装，我目前用的版本是：https://pypi.python.org/pypi/pyOpenSSL/16.2.0
下载tar包后解压，到解压目录，执行安装：sudo python setup.py install
whl包安装需先安装wheel: sudo pip install wheel
wheel安装成功后可以安装whl包： sudo pip install xxx.whl


关于分支管理
*_prod分支代表已经在预生产上执行通过的自动化测试代码，与研发的上线流程类似：master分支可以持续提交新的测试代码，只有稳定通过的测试代码才会到ci_*分支，只有发布上线后的测试代码才会到*_prod分支，如此轮回
当开发将一个新功能在master上时，测试同步更新master分支的测试代码
应用持续集成后，会每天执行自动化测试，master上通过的测试代码会自动reset到ci_*分支，不通过则不会reset
理论上上线前需要jenkins上执行发布测试，成功后会自动reset ci_*分支到prod（目前只有开放平台实现了在预生产执行发布测试，其他产品线有有局限性）

为了保证master的稳定性，初级测试开发建议建代码提交至xxx_dev分支，经过高级测试开发review后，可将代码合并至master分支，合并时尽量采用rebase的方式，尽量避免merge

push代码到远程前，请先git pull –rebase，目的是尽量避免merge

reset master分支到prod分支的操作命令如下：
git checkout *_prod
git reset --hard origin/master

