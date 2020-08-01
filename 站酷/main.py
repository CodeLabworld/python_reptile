import os
import re
import jsonpath
from lxml import etree
import requests

# 退出程序
def quit():
    exit()

# 图片下载（urls页面全部主题的链接）
def download(urls):
    for url in urls:
            # 发送请求
            reponse = requests.get(url).text
            html = etree.HTML(reponse)
            titles = html.xpath('//h2')
            titles = re.sub(' |\n', '', titles[0].text)
            # 获取图片下载的所需的参数objectid
            objectid = html.xpath('//input[@id="dataInput"]/@data-objid')
            if len(objectid) != 0:
                y = 0
                titles = titles.replace('\\', '').replace('/', '').replace(':', '').replace('：', '') \
                    .replace('*', '').replace('?', '').replace('？', '').replace('“', '') \
                    .replace('"', '').replace('<', '').replace('>', '').replace('|', '_').replace('【', '').replace('】', '') \
                    .replace(' ', '')
                img_urls = []
                # 判断文件夹是否存在，不存在就创建一个
                if not os.path.exists(r'{}\{}'.format(path, titles)):
                    os.mkdir(r'{}\{}'.format(path, titles))
                else:
                    y = len(os.listdir(r'{}\{}'.format(path, titles)))
                # 构造图片下载链接
                url__ = 'https://www.zcool.com.cn/work/content/show?p=1&objectId={}'.format(objectid[0])
                reponse = requests.get(url__)
                html = reponse.json()
                z = len(jsonpath.jsonpath(html, '$..allImageList')[0])
                for x in range(z):
                    img_urls1 = jsonpath.jsonpath(html, '$..allImageList[{}]'.format(x))[0]['url']
                    img_urls.append(img_urls1)
                for img_url in img_urls:
                    with open(r'{}\{}\{}.jpg'.format(path,titles, y), 'wb') as f:
                        content = requests.get(img_url).content
                        f.write(content)
                    y += 1
            else:
                pass
    print('下载完成')


while True:
    print(
        '''
----------------------------------------------------------------------------
        站酷网站图片下载器                                                                                                      
        命令：                                                                  
        输入1，下载具体某页的内容（一个主题的具体页）（链接以=.html结尾的网页）     
        输入2，下载某一页内容（多个主题的目录页）                                
        输入3，下载某个酷主的全部设计图 （含多页）
        退出命令：q
        ps:自动创建文件夹                                            
----------------------------------------------------------------------------
        '''
    )
    command  = input('输入命令：')

    if command == '1':
        url = input('输入该页的链接：')
        path = input('输入保存路径：')
        print('开始下载->>>>>>>>>>>>>>>>>>>>>')
        reponse = requests.get(url).text
        html = etree.HTML(reponse)
        titles = html.xpath('//h2')
        titles = re.sub(' |\n', '', titles[0].text)
        objectid = html.xpath('//input[@id="dataInput"]/@data-objid')[0]
        url = 'https://www.zcool.com.cn/work/content/show?p=1&objectId={}'.format(objectid)
        reponse = requests.get(url)
        html = reponse.json()
        z = len(jsonpath.jsonpath(html, '$..allImageList')[0])
        img_urls = []
        y = 0
        if not os.path.exists(r'{}\{}'.format(path, titles)):
            os.mkdir(r'{}\{}'.format(path, titles))
        for x in range(z):
            img_urls1 = jsonpath.jsonpath(html, '$..allImageList[{}]'.format(x))[0]['url']
            img_urls.append(img_urls1)
        for img_url in img_urls:
            with open(r'{}\{}\{}.jpg'.format(path,titles, y), 'wb') as f:
                content = requests.get(img_url).content
                f.write(content)
            y += 1
        print('下载完成')

    elif command == '2':
        url_ = input('输入该页的链接：')
        path = input('输入保存路径：')
        response = requests.get(url_)
        text = response.text
        html = etree.HTML(text)
        urls = html.xpath('//p[@class="card-info-title"]/a/@href')
        print('开始下载->>>>>>>>>>>>>>>>>>>>>')
        # 下载
        download(urls)

    elif command == '3':
        url_ = input('输入该酷主的首页链接(点到第二页再点回第一页时末尾是p=1的链接)：')
        path = input('输入保存路径：')
        response = requests.get(url_)
        text = response.text
        html = etree.HTML(text)
        print('开始下载>>>>>>>>>>>>>>>>>')
        try:
            pages = html.xpath('//div[@name="laypage1.3"]/a')
            pages = int(pages[len(pages)-2].text)
            url_ = re.sub('p=\d+','',url_)
            for page in range(1,pages+1):
                print('正在下载第' + str(page) + '页')
                url_ = url_ +'p={}'.format(page)
                response = requests.get(url_)
                text = response.text
                html = etree.HTML(text)
                urls = html.xpath('//p[@class="card-info-title"]/a/@href')
                download(urls)
        except:
            urls = html.xpath('//p[@class="card-info-title"]/a/@href')
            download(urls)
    elif command == 'q':
        quit()
    else:
        print('命令输入有误，请重新输入')



