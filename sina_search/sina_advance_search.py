# _*_ coding: utf-8 _*_

import re
import rsa
import time
import json
import base64
import logging
import binascii
import requests
import urllib
import urllib2
from lxml import etree

import sys

reload(sys) 
sys.setdefaultencoding('utf8')


class WeiBoLogin(object):
    """
    class of WeiBoLogin, to login weibo.com
    """

    def __init__(self):
        """
        constructor
        """
        self.user_name = None
        self.pass_word = None
        self.user_uniqueid = None
        self.user_nick = None

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})
        self.session.get("http://weibo.com/login.php")
        return

    def login(self, user_name, pass_word):
        """
        login weibo.com, return True or False
        """
        self.user_name = user_name
        self.pass_word = pass_word
        self.user_uniqueid = None
        self.user_nick = None

        # get json data
        s_user_name = self.get_username()   # 得到的加密用户名
        json_data = self.get_json_data(su_value=s_user_name)
        if not json_data:
            return False
        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"]) # 得到的加密密码

        # make post_data
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": json_data["rsakv"],
            "servertime": json_data["servertime"],
            "nonce": json_data["nonce"],
            "su": s_user_name,
            "sp": s_pass_word,
            "returntype": "TEXT",
        }

        # get captcha code
        if json_data["showpin"] != 1:
            
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            with open("captcha.jpeg", "wb") as file_out:
                file_out.write(self.session.get(url).content)
            code = input("请输入验证码:")
            post_data["pcid"] = json_data["pcid"]
            post_data["door"] = code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time()*1000),
            }
            response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                logging.warning("WeiBoLogin succeed: %s", json_data_2)

                keyword = "台风梅花"
                startTime = "2015-06-09"
                interval = 50
                cd = CollectData(self.session,keyword, startTime, interval)
                url = cd.getURL()  
                cd.download(url)


            else:
                logging.warning("WeiBoLogin failed: %s", json_data_2)
        else:
            logging.warning("WeiBoLogin failed: %s", json_data_1)
        return True if self.user_uniqueid and self.user_nick else False

    def get_username(self):
        """
        get legal username
        """
        username_quote = urllib.quote_plus(self.user_name)  # 对用户名进行编码
        username_base64 = base64.b64encode(username_quote.encode("utf-8")) # 用户名加密方式：encode + base64
        

        # print(username_base64)
        return username_base64.decode("utf-8")

    def get_json_data(self, su_value):
        """
        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc

        该函数发送request请求，需要使用到 加密后的 用户名su

        整个流程：
            根据用户名username得到加密后的用户名 su
            根据su得到一个json串，里面包含加密密码用到的各种参数 servertime nonce等
            根据json串和密码得到加密后的密码，然后就可以进行登录

        """
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": su_value,
            "_": int(time.time()*1000),
        }
        try:
            response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
            json_data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except Exception as excep:
            json_data = {}
            logging.error("WeiBoLogin get_json_data error: %s", excep)

        logging.debug("WeiBoLogin get_json_data: %s", json_data)
        return json_data

    def get_password(self, servertime, nonce, pubkey):
        """
        get legal password

        对密码进行加密操作，在加密操作之前，我们要先取得以下参数 servertime nonce pubkey
        """

        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()


class CollectData():
    """
    该类进行数据收集工作
    params：
        begin_url_per：地址固定部分
        keyword：关键词
        startTime：搜索开始时间
        interval：临近的两次网页请求之间的基础时间间隔，过于频繁会被认为是机器人
    """
    def __init__(self,session, keyword, startTime, interval='50', flag=True, begin_url_per = "http://s.weibo.com/weibo/"):
        
        self.begin_url_per = begin_url_per
        self.session = session

        self.setKeyword(keyword)
        self.setStartTimescope(startTime)
        self.setInterval(interval)
        self.setFlag(flag)    
        self.logger = logging.getLogger('main.CollectData') #初始化日志 

    def setKeyword(self, keyword): # 关键字需要进行两次解码为utf-8
        self.keyword = keyword
        print 'twice encode:',self.getKeyWord() 

    def getKeyWord(self): #关键字需要进行两次urlencode
        once = urllib.urlencode({"kw":self.keyword})[3:]
        return urllib.urlencode({"kw":once})[3:] 

    ##设置起始范围，间隔为1天  
    ##格式为：yyyy-mm-dd  
    def setStartTimescope(self, startTime):  
        if not (startTime == '-'):  
            self.timescope = startTime + ":" + startTime  
        else:  
            self.timescope = '-'
    
    ##设置搜索地区  
    #def setRegion(self, region):  
    #    self.region = region

    # 设置邻近网页请求之间的基础时间间隔  
    def setInterval(self, interval):  
        self.interval = int(interval)

    # 设置是否被认为机器人的标志。若为False，需要进入页面，手动输入验证码  
    def setFlag(self, flag):  
        self.flag = flag 


    # 进行url构建   这里省略了限制区域搜索
    def getURL(self):
        return self.begin_url_per + self.getKeyWord() + "&typeall=1&suball=1&Refer=g&page="
        # return self.begin_url_per + self.getKeyWord() + "&typeall=1&suball=1&timescope=custom:" + self.timescope + "&page="
        #  http://s.weibo.com/weibo/%25E4%25B8%25AD%25E5%25B1%25B1%25E5%25A4%25A7%25E5%25AD%25A6&region=custom:44:1&typeall=1&suball=1&timescope=custom:2015-08-07-0:2015-08-08-0&Refer=g


    #爬取一次请求中的所有网页，最多返回50页  axTryNum 当网络不佳时 设置最大请求次数
    def download(self, url, maxTryNum=4):
        hasMore = True  #某次请求可能少于50页，设置标记，判断是否还有下一页  
        isCaught = False

        name_filter = set([])    #过滤重复的微博ID  
          
        i = 2   #记录本次请求所返回的页数

        while hasMore and i < 3 and (not isCaught):
            source_url = url + str(i)   #构建某页的URL  
            data = ''          # 存储该页的网页数据  
            goon = True      # 网络中断标记  

            # 网络不好的情况，试着尝试请求三次  
            for tryNum in range(maxTryNum):
                # try:  
                print "开始页面下载" 
                print "source_url:",source_url
                # html = urllib2.urlopen(source_url,timeout=12)
                html = self.session.get(source_url)

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html.text,'lxml')
                scripts =  soup.find_all("script")           
                # html = requests.get(source_url)

                # data = html.read()
                # print(data)

                # lines = data.splitlines()
                
                for line in scripts:
                    
                    line_str = str(line)
                    
                    # line_str = line.decode("utf-8")
                    if line_str.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
                        # ee = 'html":"'.encode(encoding="utf-8")
                        n = line_str.find('html":"')
                        if n > 0:
                            j = line_str[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
                            if (j.find(b'<div class="search_noresult">') == 0):
                                print "111"
                            else:
                                j = j.decode('utf-8')
                                from bs4 import BeautifulSoup
                                soup = BeautifulSoup(j,'lxml')
                                units = soup.find_all("div",class_="WB_feed_detail clearfix")
                                
                                print len(units)
                                for unit in units:
                                    content = unit.find("div",class_="feed_content wbcon")
                                    name = content.find("a",class_="W_texta W_fb").text
                                    name = name.replace("\t","").replace("\n","")
                                    print "name:",name
                                    # info = content.find("p",class_="comment_txt").text
                                    # info = info.replace("\t","")
                                    

                                    unit_parent = unit.parent
                                    info_url = 'https://s.weibo.com/ajax/direct/morethan140?mid=' + unit_parent['mid']
                                    info_html = self.session.get(info_url)

                                    import json
                                     
                                    info_dict = json.loads(info_html.text)
                                    ff = info_dict['data']['html']
                                    qq = BeautifulSoup(ff,'lxml')
                                    info = qq.text
                                    print "info:",info

                                    timestrap_pre = unit.find("div",class_="feed_from W_textb")
                                    timestrap = timestrap_pre.find("a").text
                                    print "time:",timestrap

                    # else:
                    #     print("失败")


                break
                # except:  
                #     if tryNum < (maxTryNum-1):  
                #         time.sleep(10)  
                #     else:  
                #         print('Internet Connect Error!')
                #         self.logger.error('Internet Connect Error!')  
                #         self.logger.info('url: ' + source_url)  
                        
                #         self.logger.info('page: ' + str(i))  
                #         self.flag = False  
                #         goon = False  
                #         break
            break
            i = i + 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    # python 的 logging 模块将日志打印到屏幕上，日志级别为 debug 表示 日志级别高于debug的日志信息才会输出
    # 日志输出格式如下：
    # WARNING(日志级别) : root(logger实例名称) : warn message(日志消息内容)
    # 日志的级别有 DEBUG INFO WARNING ERROR CRITICAL
    weibo = WeiBoLogin()
    weibo.login("username", "password")


    
