# -*- coding: UTF-8 -*-
import requests
import base64
import os
import json

#得到百度api的Token
def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = 'jbTi9uAGB9oxOaBat4EN3jUd'
    client_secret = 'PknlPLB6C2YfYR91uFluTK7SM1vRKcez'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
    response = requests.get(host)
    if response:
        return response.json()['access_token']

#用树莓派拍照
def get_photo():
    #os.system('sudo raspistill -t 2000 -o image.jpg -w 320 -h 240')
    os.system('sudo raspistill -o ugi.jpg -w 1024 -h 768 -v')

#百度识图
def baidu_photo():
    f = open('image.jpg', 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = get_token()
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data = params, headers=headers)
    if response:
        #对识别的结果进行筛选
        list_text = ""
        for res in response.json()['result']:
            root = res['root'].split("-")[1]
            r = classification(root)
            if r != "0":
                list_text = list_text + root +" : "+ r + "\n"
        print(list_text)
        pushplus(list_text)
        #return response.json()['result'][0]['keyword']
        

#垃圾分类
def classification(name):
    #付费api
    # url = 'http://api.tianapi.com/txapi/lajifenlei/index?key=28f6485d14221efeeead38fbc6173e34&word='+ name
    # r = requests.get(url)
    # print(r.text)

    #这是一个免费的api，但是识别容易出问题
    url = "https://api.66mz8.com/api/garbage.php?name="+name
    r = requests.get(url,name)
    dict_data = json.loads(r.text)
    if "data" in dict_data.keys():
        return dict_data["data"]
    else:
        return "0"


#微信推送结果
def pushplus(content):
    token = 'a6265a189e994e74bf6ab24587bb8891' #在pushpush网站中可以找到http://pushplus.hxtrip.com/
    title = '的垃圾分类结果' #改成你要的标题内容
    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token":token,
        "title":title,
        "content":content
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)


if __name__ == "__main__":
    get_photo()
    baidu_photo()
