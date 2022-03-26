import requests
from lxml import etree
import json
import time


areas=['','jian']

def getHtml(area):

    url=f'http://www.chinasydw.org/jiangxi/{area}'

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    res=requests.get(url=url,headers=headers,verify=False)
    res.encoding=res.apparent_encoding
    data=res.text
    return data


def getInfo(html):

    ele=etree.HTML(html)
    # /html/body/div[4]/div[1]/div[2]/div[3]/ul/li[1]/span[2]
    date=ele.xpath('//body/div[4]/div[1]/div[2]/div[3]/ul/li/span/text()')

    title=ele.xpath('//body/div[4]/div[1]/div[2]/div[3]/ul/li/a/text()')

    infos=[]
    for i,j in zip(date,title):
        # print(i,j)
        if i[:10]==date[0][:10]:
            # info.append(i[:10])
            infos.append(j)
            pass
        pass
    return date[0][5:10],infos


def get_token():
    CORP_ID = "ww1ceb3d50852c60cd"
    SECRET = "etdJRhaznvs_7oZ5JTWnw7gy1IQi4d1hOGIRF_krhrI"
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
    }
    rep = requests.get(url,headers=headers,verify=False)
    if rep.status_code != 200:
        print("request failed.")
        pass
    else:
        rep=json.loads(rep.text).get('access_token')
        return rep


def sendWxMsg(title,content,Url):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_token()
    header = {
        "Content-Type": "application/json"
    }
    form_data = {
        "touser": "@all",
        "toparty": " PartyID1 | PartyID2 ",
        "totag": " TagID1 | TagID2 ",
        "msgtype": "textcard",
        "agentid": 1000004,
        "textcard": {
            "title": title,
            "description": content,
            "url": Url,
            "btntxt": "更多"
        },
        "safe": 0
    }
    res=requests.post(url=url,headers=header,data=json.dumps(form_data).encode('utf-8'),verify=False)
    # print(res.text)
    pass


def main():

    for area in areas:
        U=f'http://www.chinasydw.org/jiangxi/{area}'
        data=getHtml(area)
        # print(data)
        infos=getInfo(data)
        # print(infos)
        msg="\n".join(infos[1])
        if area=='':
            title=f'江西事业单位（{infos[0]}）'
            pass
        else:
            title=f'吉安事业单位（{infos[0]}）'
            pass
        # print(U)
        sendWxMsg(title,msg,U)
        time.sleep(3)
        # print(infos)
        pass
    pass

main()
