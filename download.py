import threading
from sys import exit
from re import search,match,sub
from requests import get,post,exceptions
from bs4 import BeautifulSoup as bs
from json import loads,dumps
from utils import *

container = []

def BiliDecoder(x):
	table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
	ss=[11,10,3,8,4,6]
	xors=177451812
	addss=8728348608
	x=(x^xors)+addss
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[ss[i]]=table[x//58**i%58]
	return ''.join(r)


class MyException(Exception):
    """ 自定义错误基类 """
    pass


class ConnectError(MyException):
    """ 连接不上服务器 """
    def __init__(self):
        self.args=('连接不上目标服务器',)


class NoneResourceError(MyException):
    def __init__(self):
        self.args = ('没有有效资源',)


PLAY_URL='https://www.bilibili.com/video/BV'
API_URL="https://api.bilibili.com/x/web-interface/view?bvid="

api_headers={
    'Host': 'api.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
}

default_headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
}

page_headers = {
    'Host': 'www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


def Fetch(url, headers, *, timeout=60, **kwargs):
    num = 0
    while num < 3:
        try:
            response = get(url, headers=headers, timeout=timeout, **kwargs)
        except exceptions.RequestException:
            num += 1
        else:
            return response
    raise ConnectError()


def apiget(URL, HEADERS=api_headers)->list:
    """ cid,aid,name,videos,view,danmaku,desc,dimension,picurl"""
    data=Fetch(URL, HEADERS).json()['data']
    aid = data["aid"]
    videos = data["videos"]
    desc = data["desc"]
    picurl = data["pic"]
    name = data["owner"]["name"]
    view = data["stat"]["view"]
    danmaku = data["stat"]["danmaku"]
    title =data['title']
    cid = []
    dimension = []
    for item in data['pages']:
        cid.append(item["cid"])
        dimension.append([item["dimension"]["width"], item["dimension"]["height"]])
    return cid,aid,title,name,videos,view,danmaku,desc,dimension,picurl


def playget(URL,HEADERS=page_headers):
    """视频播放页面信息获取"""
    html_text=Fetch(URL,HEADERS).text
    html_lxml=bs(html_text, 'lxml')
    data=html_lxml.head.find_all('script')
    # window.__playinfo__
    for i in data:
        if (t:=i.string) is not None:
            if match('window\.__playinfo',t) is None:
                pass
            else:
                break
    data_play=loads(t[20:])['data']
    if 'dash' in data_play:
        video_new_url=data_play['dash']['video'][0]['baseUrl']
        audio_new_url=data_play['dash']['audio'][0]['baseUrl']
        return video_new_url, audio_new_url
    else:
        return False


def file_part(url, head,threadnum)->tuple:
    data= Fetch(url, head)
    content=int(search('/[0-9]+',data.headers["Content-Range"]).group()[1:])
    block = content//threadnum
    range_list = []
    write_list = []
    for i in range(threadnum):
        range_list.append([i*block,(i+1)*block-1])
        write_list.append(i*block)
    range_list[-1][-1] = content - 1
    return range_list, write_list


def download(page_url, title, threadnum, index, filetmp):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Origin': 'https://www.bilibili.com',
        'Connection': 'keep-alive',
        'Range': 'bytes=0-900',
        'Referer': f'{page_url}'
    }
    filebox=(
        filetmp + title + "_video.flv",
        filetmp + title + "_audio.flv",
    )
    j = 0
    page_video_url = playget(page_url)
    if page_video_url==False:
        #TODO
        exit(1)
    for url in page_video_url:
        filename = filebox[j]
        with open(filename,"wb") as _:
            pass
        lock = threading.Lock()
        range_list, write_list = file_part(url, head, threadnum)
        j += 1
        threads = []
        for i in range(len(write_list)):
            threads.append(threading.Thread(target=downloadcore,
                    args=(url, filename, lock, head, range_list[i], write_list[i], index)))
        for i in threads:
            i.start()


def downloadcore(url, filename, lock, headers, rangex, writex, index):
    head = ValueCopy(headers)
    head.update({'Range':f"bytes={rangex[0]}-{rangex[1]}"})
    data = Fetch(url, head).content
    lock.acquire()
    with open(filename, 'rb+') as file:
        file.seek(writex)
        file.write(data)
    container[index].append(1)
    lock.release()


def hostget(url:str)->str:
    """ 通过输入连接🔗获取服务器主机域名 """
    return '/'.join(url.split('/')[:3])


class DownLoad_M3U8:
    koudaicc = [] # 进度容器
    Counts = 0 # 计数变量
    ck = []
    isCompl=True
    def __init__(self, url):
        self.url = url
        self.uid = search('id=[0-9]+', self.url).group()[3:] # 也用这个视频编号来命名
        self.filename = self.uid

    def rename_ts_file(self, _):
        self.Counts += 1
        return f"./temp/{self.Counts}.ts" # 生成的x.ts流文件保存在当前目录下文件temp中


    def get_m3u8(self):
        PlayLoadData = {"liveId": self.uid}
        head={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            "Referer": f"{self.url}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        url_live = "https://pocketapi.48.cn/live/api/v1/live/getLiveOne"
        url_open_live = 'https://pocketapi.48.cn/live/api/v1/live/getOpenLiveOne'
        try:
            data = post(url_live, data=dumps(PlayLoadData), headers=head).json()
            data = data['content']
        except Exception:
            data = post(url_open_live, data=dumps(PlayLoadData), headers=head).json()
            data = data['content']
        finally:
            if 'playStreamPath' in data:
                lrc_url = data['msgFilePath']
                m3u8_url = data['playStreamPath']
            elif 'playStreams' in data:
                m3u8_url = data['playStreams'][0]['streamPath']
                lrc_url = None
            else:
                raise NoneResourceError()
            self.m3u8_url = m3u8_url;self.lrc_url = lrc_url

    def ts_url_list(self, host48):
        self.host48 = host48
        def TS_Url(lst):
            url_list = []
            for i in lst:
                url_list.append(self.host48 + i)
            return url_list, len(url_list)
        data_text = Fetch(self.m3u8_url,default_headers).text
        self.save_m3u8(data_text)
        data_list = data_text.split('\n')
        data_list1=[]
        for item in data_list:
            if "/fragments" in item:
                data_list1.append(item.strip())
        self.TsUrlList, self.UrlLength = TS_Url(data_list1)
        self.ck.append(self.UrlLength)
    def save_m3u8(self, txt):
        txt = sub("/fragments.+?ts", self.rename_ts_file, txt)
        with open('me.m3u8', 'w', encoding='utf-8') as file:
            file.write(txt)
    
    def download(self, url, lock, index):
        lock.acquire()
        data = Fetch(url,default_headers).content
        with open(f"./temp/{index}.ts", 'wb') as file:
            file.write(data)
        self.koudaicc.append(1)
        lock.release()

    def begin(self):
        threads = []
        mylock = threading.Semaphore(value=5)
        j = 0
        self.get_m3u8()
        if 'http' not in self.m3u8_url:
            self.isCompl=False
            return None
        self.ts_url_list(hostget(self.m3u8_url))
        if self.lrc_url:
            with open(f'{self.uid}.lrc', 'wb') as fileobject:
                fileobject.write(Fetch(self.lrc_url,default_headers).content)
        for urlx in self.TsUrlList:
            j += 1
            threads.append(threading.Thread(target=self.download, args=(urlx, mylock, j)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()
        self.combineTS()
        with open(f'{self.uid}.lrc', encoding='utf-8') as file:
            data = file.readlines()
        lstmm = prettify(list(data))
        if (tt:=lineset(lstmm)) is None:
            return None
        with open(f'./video/{self.uid}.srt', 'w', encoding='utf-8') as file:
            j = 0
            lt = list(tt)
            num = len(lt)
            for i in lt:
                j +=1
                if j<num:
                    file.write(i)
                    file.write('\n')
                else:
                    file.write(i.strip())
        removefile(f'{self.uid}.lrc')
    def combineTS(self):
        cmd(['ffmpeg','-allowed_extensions','ALL','-i',
             'me.m3u8','-c','copy', f"./video/{self.uid}.mp4",
             '-loglevel', 'quiet'])

