from os import path,mkdir,remove
from re import sub
import subprocess
from time import sleep
from sys import platform
from typing import Generator, Union

color_list=[
    '{\\1c&HdC1B6FF&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hd3c14dc&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hd82004b&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hdb469ff&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hdff901e&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hd008000&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hd6bb7bd&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hdc4e4ff&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hdcdfaff&}{\\fn华文仿宋\\fs6}',
    '{\\1c&Hddcf5f5&}{\\fn华文仿宋\\fs6}',
]


def endwithSlash(path):
    if path[-1] != '/':
        return path + '/'
    else:
        return path


def detect_os():  
    if platform.startswith('win'):
        return 'Windows'
    elif platform.startswith('darwin'):
        return 'MacOS'
    elif platform.startswith('linux'):
        return 'Linux'
    elif platform.startswith('freebsd'):
        return 'FreeBSD'
    elif platform.startswith('sunos'):
        return 'Solaris'
    else:
        return 'Unknown'

OSType = detect_os()

def cmd_for_windows(cmdPrompt:list):
    st=subprocess.STARTUPINFO()
    st.dwFlags=subprocess.STARTF_USESHOWWINDOW
    st.wShowWindow=subprocess.SW_HIDE
    string=' '.join(cmdPrompt)
    p=subprocess.Popen(string,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
    while True:
        if p.poll() is not None:
            break
        sleep(1)


def cmd_for_linux(cmdPrompt:list):
    # string=' '.join(cmdPrompt)
    p=subprocess.Popen(cmdPrompt,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        if p.poll() is not None:
            break
        sleep(1)


def cmd(cmdPrompt:list):
    if OSType == 'Windows':
        cmd_for_windows(cmdPrompt)
    elif OSType == 'Linux':
        cmd_for_linux(cmdPrompt)
    else:
        assert 0, "unsupported platform"
        pass


def hour(string:str)->int:
    return int(string[0])*36000 + int(string[1])*3600


def minute(string:str)->int:
    return int(string[0])*600 + int(string[1])*60


def cto(string:str)->int:
    tem = string.split(":")
    return hour(tem[0])+minute(tem[1])+float(tem[2])


def vto(flo:float)->str:
    tem1 = int(flo//36000)
    flo = flo-tem1*36000
    tem2 = int(flo//3600)
    flo = flo-tem2*3600
    tem3 = int(flo//600)
    flo = flo-tem3*600
    tem4 = int(flo//60)
    flo = flo-tem4*60
    return f"{tem1}{tem2}:{tem3}{tem4}:{flo:.3f}"


def setf(int1:int, int2:int)->int:
    if int1+4<=int2:
        int1 = int1+3
    elif int1+0.05>=int2:
        int1=int2
    else:
        int1=int2-0.05
    return int1


def prettify(x:list)->list:
	con = []
	for i in x:
		if i[0]=='[':
			con.append(i)
	return con


def lineset(lst:list) -> Generator[str, str, str]:
    l = len(lst)
    if l < 2:
        return None
    for i in range(l-1):
        tem1, tem2 = lst[i:i+2]
        num1, *con = tem1.split(']')
        con = sub(r'\t',':',con[0])
        num1 = num1.replace('[', '')
        num2, *_= tem2.split(']')
        num2 = num2.replace('[', '')
        num3 = vto(setf(cto(num1), cto(num2)))
        style=color_list[i%10]
        yield f"{i+1}\n{num1} --> {num3}\n{style}\n{con}"


def Tconvert(string):
    if not '.' in string:
        return string
    else:
        aa = string.split('.')
        ab = []
        for i in aa:
            ab.append(i.rjust(2, '0'))
        return ':'.join(ab)


def MakeDir(PATH)->int:
    """ 存在文件则返回1,否则创建并返回0 """
    if not path.exists(PATH):
        mkdir(PATH)
        return 0
    return 1


def ValueCopy(SEQUENCE)->list: # 也可以用copy.deepcopy()
    """对列表和字典进行完全的值拷贝,不受原先对象改变的影响"""
    INITIALLIST,INITIALDIRECTORY=[],{}
    if type(SEQUENCE)==list:
        for item in SEQUENCE:
            INITIALLIST.append(ValueCopy(item))
        return INITIALLIST
    elif type(SEQUENCE)==dict:
        for key,value in SEQUENCE.items():
            key=ValueCopy(key);value=ValueCopy(value)
            INITIALDIRECTORY[key]=value
        return INITIALDIRECTORY
    else:
        return SEQUENCE


def removefile(files:Union[str,list[str]])->None:
    """ 移除文件📄 """
    if type(files) == list:
        for i in files:
            remove(i)
    elif type(files) == str:
        remove(files)