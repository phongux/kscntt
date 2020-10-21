import requests
url = 'http://10.127.50.111/j_security_check'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'vi,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '49',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '15061RequestsshowThreadedReq=showThreadedReqshow; 15061RequestshideThreadedReq=hideThreadedReqhide; JSESSIONID=CB6C00D512DB0A30E6673434FA79DBAD; JSESSIONIDSSO=797E23CB95D833966E38BEB10E7F8A14; _rem=true; febbc30d=12f0c776804546df9b4c50ee39949cb7; mesdp4594afaa2c=450567fcd49d15a1fa119ce788f965b0de6157c1',
    'Host': '10.127.50.111',
    'Origin': 'http://10.127.50.111',
    'Referer': 'http://10.127.50.111/WOListView.do',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
}
data = {
    'requestViewChanged': 'true',
    'viewName': 'All_Requests',
    'globalViewName': 'All_Requests'
}

headers1 = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://10.127.50.111',
    'Referer': 'http://10.127.50.111/HomePage.do?logout=true&logoutSkipNV2Filter=true',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
}
data1 = {
    'j_username': 'vsa05',
    'j_password': 'abc@123',
    'domain': '1',
    'DOMAIN_NAME': 'VINGROUP.LOCAL',
    'LDAPEnable': 'false',
    'hidden': 'Chọn một miền',
    'hidden': 'Đối Với Miền',
    'AdEnable': 'true',
    'DomainCount': '0',
    'LocalAuth': 'No',
    'LocalAuthWithDomain': 'VINGROUP.LOCAL',
    'dynamicUserAddition_status': 'true',
    'localAuthEnable': 'true',
    'logonDomainName': 'VINGROUP.LOCAL',
    'loginButton': 'Đăng nhập Hệ thống',
    'checkbox': 'checkbox'
}

with requests.Session() as s:
    s.post(url, headers=headers1, data=data1)
    print(0)

print(0)