## 微博模拟登陆
开启Charles后，打开并登陆新浪微博，输入用户名和密码，验证码。这时候会在Charles留下整个登录的流程，后边慢慢分析。

* 微博用户名加密方式：

  先进行encode，然后紧跟着base64
* 微博密码加密方式：

  密码加密的时候需要传递参数：nonce、servertime、rsakv。

  上述参数在 prelogin的请求的返回中，prelogin需要加密后的用户名。

整个加密流程：
1. 根据用户名 username 得到加密后的用户名
2. 根据 su 发送prelogin请求，得到一个json串，里面包含加密密码用到的各种参数 servertime nonce等
3. 根据json串和密码得到加密后的密码，然后进行登录(登录请求login.php里面)

根据该请求的request，自己构建 postdata，发送请求即可。

验证码问题
根据上边得到的json串中的showpin参数得知。获取到验证码的图片，可以人工手动输入验证码，也可以调用在线验证码识别接口。

构造postdata，发送请求，即便是请求成功了，其实还没登录成功。
还有一步跳转请求，wbsso.login。构建postdata，并发送请求即可。

这里还有一个问题没有说到，就是Cookie问题。本文中一直没有提到Cookie，是因为Python中的Cookiejar会帮我们自动处理所有的cookie问题。你只需要在模拟登陆之前，首先声明一个cookiejar和opener即可，具体这两个东西的用法，大家自行百度。