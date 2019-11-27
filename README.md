# CMS
flask内容管理系统项目

1.redis服务器安装目录 H:\常用软件\Redis-x64-3.2.100

2.每个包里面要加上__init__.py文件

3.
from flask import session
from flask_session import Session区别
当然，在flask项目中也要实现状态保持，把Cookie存储在浏览器，session存储到服务器，但是当我们的用户量较大时，各种状态保持信息（用户信息，浏览历史信息等）都放到session中，就会大大的增加服务器的负荷，为了减轻服务器的压力，我们就把session放到redis数据库中，另外，redis数据库读取数据也是更快的，这个功能的实现靠的就是flask-session扩展中的Session;  即session是基于浏览器的cookie进行保存在服务器上的，flask_session可以把session的值存储在redis数据库中。这个session无论用户登录还是退出，只要不过期，就一直存在，与框架无关，与语言无关，便于用户在浏览器端再次便捷登录。

from flask import session  这个sesssion是flask框架内置的请求上下文对象，用来操作记录http请求的数据或session信息，在请求过程中存在，请求结束后就被销毁；比如只有登录的用户并且发送http请求时,它才被唤醒存储内容，用户退出时，它又被销毁；在本flask项目的应用场景：

在登录接口，用户用过mobile 和password验证后(用户存在且密码正确)，我们就通过mobile查询出该用户对象user, 再把该登录用户的name,user_id, mobile 保存到上下文session中，方便其他模块接口的调用当前登陆的用户信息。

在登录接口实现登陆以后，我们如何在其他接口判断用户是否登录呢？很简单，我们只需用user_id = session.get("user_id")，如果user_id存在，就说明用户已经通过了登录接口的验证和session信息的保存。因为很多接口都要判断登录状态，我们通常把这个功能放到装饰其中(即重写flask_login的login_required方法)，方便各接口调用

4.<RedisSession {'_permanent': True, 'csrf_token': '96ab8eb1d9c22e3e5f92075a173d7d9ae2b04e7e', 'image': '2597'}>
<SecureCookieSession {'csrf_token': 'a0f3b8b55b5e0e6489329564ea3eae01571e8964', 'image': '9286'}>


5.
URL反转：根据视图函数名称得到当前所指向的url
url_for() 函数最简单的用法是以视图函数名作为参数，返回对应的url，还可以用作加载静态文件，如