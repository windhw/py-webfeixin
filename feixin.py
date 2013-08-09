import requests
import random
s = requests.Session()
browser_header =  {'x-test': 'true',
                  'Accept' : 'application/json, text/javascript, */*; q=0.01',
                  'Accept-Encoding' : 'gzip,deflate,sdch',
                  'Accept-Language' : 'zh-CN,zh;q=0.8',
                  'Connection' : 'keep-alive',
                  'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8' ,
                  'Host' : 'webim.feixin.10086.cn' ,
                  "Origin" : "https://webim.feixin.10086.cn" ,
                  "Referer" : "https://webim.feixin.10086.cn/loginform.aspx" ,
                  'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36' ,
                  'X-Requested-With' : 'XMLHttpRequest'}


username = raw_input("input username:")
passwd = raw_input("input password:")
login_data = {'UserName': username,
              'Pwd' : passwd, 
              'OnlineStatus' : '0',
              'AccountType' : '1'}

login_url = "https://webim.feixin.10086.cn/WebIM/Login.aspx"
ccp_url = "https://webim.feixin.10086.cn/WebIM/GetPicCode.aspx?Type=ccpsession&%s" % random.random()
contact_url = "https://webim.feixin.10086.cn/WebIM/GetContactList.aspx?Version=3"
connect_url = "https://webim.feixin.10086.cn/WebIM/GetConnect.aspx?Version="
ssid = ""

s.headers.update(browser_header)
r = s.post(login_url,data=login_data)
print r.headers
rj =  r.json()
rtcode = rj[u'rc']
print "content:"
print r.content
if rtcode  != 200:
    if rtcode == 999:
        print "999"
        r = s.get(ccp_url, headers = {"Accept":"image/webp,*/*;q=0.8",
                                      "Content-Type": None,
                                      "X-Requested-With" : None})
        print r.url
        f=file("ccp.jpg","w")
        f.write(r.content)
        f.close()
        ccp_code = raw_input("input code:")
        login_data["Ccp"] = ccp_code
        r = s.post(login_url,data=login_data)
        print "After CCP:"
        print r.content
        if (r.json()[u'rc'] != 200):
            print "CCP Bad"
            exit()
	print "OK"
        ssid =  r.cookies['webim_sessionid']
    else:
        print "Bad"
        exit()
else:
    ssid =  r.cookies['webim_sessionid']
    print "OK!!"

browser_header["Referer"] = "https://webim.feixin.10086.cn/main.aspx"
s.headers.update(browser_header)

print r.cookies
r = s.post(contact_url,data={"ssid":s.cookies['webim_sessionid']} )
print r.content
print s.cookies['webim_sessionid']
version = 4

while(1):
    version += 1
    r = s.post(connect_url + str(version) ,data={"ssid":s.cookies['webim_sessionid']} )
    print r.url
    print r.json()
