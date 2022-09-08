# Raspberry-Pi-garbage-sorting

**树莓派垃圾分类**

## 树莓派拍照

```python
def get_photo():
    #os.system('sudo raspistill -t 2000 -o image.jpg -w 320 -h 240')
    os.system('sudo raspistill -o image.jpg -w 1024 -h 768 -v')
```

直接调用系统命令，其中`-w 1024 -h 768`为宽和高，这里可以设置为自己需要的分辨率，如`-w 320 -h 240`。

## 百度识图

先得到token。其中`client_id`，`client_secret`需要自己去[百度开放平台](https://console.bce.baidu.com/ai/?_=&fromai=1#/ai/imagerecognition/app/list)创建应用之后获取。

```python
def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = 'jbTi9uAGB9oxOaBat4EN3jUd'
    client_secret = 'PknlPLB6C2YfYR91uFluTK7SM1vRKcez'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
    response = requests.get(host)
    if response:
        return response.json()['access_token']
```

`get_token()`函数直接在百度识图的`baidu_photo()`函数里调用。

```python
def baidu_photo():
    #先读取图片的base64编码
    f = open('image.jpg', 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    
    #得到token
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
        #打印结果
        print(list_text)
        #直接调用微信推送
        pushplus(list_text)
```

## 垃圾分类

垃圾分类我们找了两个api，只启用了免费的一个。

```python
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
```

## 微信推送

微信推送调用的是[pushplus](http://pushplus.hxtrip.com/)的api，想要自己的微信收到消息，需要自己去申请并换为自己的Token。

```python
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
```



