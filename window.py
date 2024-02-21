from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from re import search, compile
from PyQt5 import sip
from download import *
import XmlToAss as xta



class BPlainTextEdit(QtWidgets.QPlainTextEdit):
    """ 自定义的PlainTextEdit类,重新改写了原本的dropEvent函数
    使得拖拽进区域后显示的文件路径不包含file:///,并且每次新的拖拽都
    会另起一行显示文件路径
    D:/B站视频/video1.MP4
    D:/B站视频/video2.MP4
    D:/B站视频/video3.MP4 """
    def dropEvent(self, event):
        filename = event.mimeData().urls()[0].toLocalFile()
        _, suffix = path.splitext(filename) # .mp4
        presentText = self.toPlainText()
        if not presentText or suffix in presentText:
            self.appendPlainText(filename)


class BLabel(QtWidgets.QLabel):
    ''' 自定义Label类,重新改写了原本的dragEnterEvent和dropEvent函数
    使得新的Label类接受拖拽操作,文件路径将被显示(注意设置setAcceptDrops为True) '''
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    

    def dropEvent(self, event):
        filename=event.mimeData().urls()[0].toLocalFile()
        #TODO
        self.setText(filename)
        event.accept()


class Windows(object):
    def SetUi(self,myWindow):
        # 设置 myWindow 主窗口的布局和基础属性
        # 保存窗口部件命名
        #主窗口的样式和大小
        myWindow.setObjectName('myWindow')
        myWindow.resize(882,801)
        myWindow.setMinimumSize(QtCore.QSize(880,800))
        myWindow.setWindowTitle('BiliDownload')
        #设置主窗口的字体大小为 13
        font=QtGui.QFont()
        font.setPointSize(13)
        myWindow.setFont(font)
        #设置图标
        icon=QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('resource/images/loong.png'),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        myWindow.setWindowIcon(icon)

        #设置中心容器
        self.cWidget=QtWidgets.QWidget(myWindow)
        self.cWidget.setObjectName('cWidget')
        myWindow.setCentralWidget(self.cWidget)
        #设置中心容器的布局为cHLayout 水平
        self.cHLayout=QtWidgets.QHBoxLayout(self.cWidget)
        self.cHLayout.setObjectName('cHLayout')

        #引入一个新的垂直布局，我们将在里面放置部件
        self.cVLayout=QtWidgets.QVBoxLayout()
        self.cVLayout.setObjectName('cVLayout')

        #引入一个水平布局用于放置bv好输入和确定框
        self.tHLayout=QtWidgets.QHBoxLayout()
        self.tHLayout.setObjectName('tHLayout')
        #
        #我们在水平布局tHLayout中放入三个部件
        #分别为一个显示提示输入的labelBV
        #一个用于输入的lineBV框
        #一个确定按钮okbuttonBV
        self.labelBV=QtWidgets.QLabel(self.cWidget)
        self.labelBV.setObjectName('labelBV')
        self.labelBV.setText('输入BV号')
        self.tHLayout.addWidget(self.labelBV)

        self.lineBV=QtWidgets.QLineEdit(self.cWidget)
        self.lineBV.setObjectName('lineBV')
        self.tHLayout.addWidget(self.lineBV)

        self.okbuttonBV=QtWidgets.QPushButton(self.cWidget)
        self.okbuttonBV.setObjectName('okbuttonBV')
        self.okbuttonBV.setText('确定')
        self.tHLayout.addWidget(self.okbuttonBV)

        #我们将布局tHLayout放入垂直布局cVLayout中
        #我们将布局cVLayout放入垂直布局cHLayout中
        self.cVLayout.addLayout(self.tHLayout)
        self.cHLayout.addLayout(self.cVLayout)

        #我们构建一个分页部件partWidget
        self.partWidget=QtWidgets.QTabWidget(self.cWidget)
        self.partWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.partWidget.setObjectName('partWidget')
        #设置分页的字体大小
        font=QtGui.QFont()
        font.setPointSize(15)
        self.partWidget.setFont(font)
        #设置鼠标行为
        self.partWidget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #将这个分页部件放入到cVLayout中
        self.cVLayout.addWidget(self.partWidget)
        #下面我们构建第一个分页内容，用来展示视频信息
        self.videoInfo=QtWidgets.QWidget()
        self.videoInfo.setObjectName('videoInfo')
        #添加到分页中去,并取名为信息
        self.partWidget.addTab(self.videoInfo,'信息')

        #引入水平布局一个放视频信息，另一个放图片
        self.iHLayout=QtWidgets.QHBoxLayout(self.videoInfo)
        self.iHLayout.setObjectName('iHLayout')

        #引入一个窗口部件，用于放置视频信息
        self.showInfo=QtWidgets.QWidget(self.videoInfo)
        self.showInfo.setMinimumSize(QtCore.QSize(300,0))
        self.showInfo.setObjectName('showInfo')
        #在showInfo中引入垂直布局放置三个组件
        self.showVLayout=QtWidgets.QVBoxLayout(self.showInfo)
        self.showVLayout.setObjectName('showVLayout')
        #视频信息表格showChart
        self.showChart=QtWidgets.QTableWidget(self.showInfo)
        #设置表格样式
        self.showChart.setMinimumSize(QtCore.QSize(278,300))
        self.showChart.setFrameShape(QtWidgets.QFrame.Box)
        self.showChart.setFrameShadow(QtWidgets.QFrame.Raised)
        self.showChart.setMidLineWidth(2)
        self.showChart.setAlternatingRowColors(True)
        self.showChart.setProperty('showDropIndicator',True)
        self.showChart.setShowGrid(True)
        self.showChart.setGridStyle(QtCore.Qt.DashLine)
        self.showChart.setCornerButtonEnabled(True)
        self.showChart.setObjectName('showChart')
        self.showChart.setWordWrap(True)
        #设置表为7行1列
        self.showChart.setColumnCount(1)
        self.showChart.setRowCount(7)
        #初始化行表头
        item=QtWidgets.QTableWidgetItem()
        item.setText('av号')
        self.showChart.setVerticalHeaderItem(0,item)
        item=QtWidgets.QTableWidgetItem()
        item.setText('标题')
        self.showChart.setVerticalHeaderItem(1,item)
        item=QtWidgets.QTableWidgetItem()
        item.setText('up主')
        self.showChart.setVerticalHeaderItem(2,item)
        item=QtWidgets.QTableWidgetItem()
        item.setText('分p数')
        self.showChart.setVerticalHeaderItem(3,item)
        item=QtWidgets.QTableWidgetItem()
        item.setText('播放量')
        self.showChart.setVerticalHeaderItem(4,item)
        item=QtWidgets.QTableWidgetItem()
        item.setText('弹幕数')
        self.showChart.setVerticalHeaderItem(5,item)
        item=QtWidgets.QTableWidgetItem()
        item.setText('视频尺寸')
        self.showChart.setVerticalHeaderItem(6,item)
        #初始化列表头
        item=QtWidgets.QTableWidgetItem()
        self.showChart.setHorizontalHeaderItem(0,item)
        #隐藏列表头
        self.showChart.horizontalHeader().setVisible(False)
        #设置表格大小
        self.showChart.horizontalHeader().setDefaultSectionSize(220)
        self.showChart.verticalHeader().setDefaultSectionSize(42)
        #将表showchart放入布局showVLayout
        self.showVLayout.addWidget(self.showChart)
        #引入一个标签来显示描述两字
        self.videoDesc=QtWidgets.QLabel(self.showInfo)
        self.videoDesc.setMaximumSize(QtCore.QSize(278,38))
        self.videoDesc.setText('视频描述')
        self.videoDesc.setObjectName('videoDesc')
        self.showVLayout.addWidget(self.videoDesc)
        #引入一个展览板用于显示视频描述信息
        self.DescBrower=QtWidgets.QTextBrowser(self.showInfo)
        sizePolicy=QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DescBrower.sizePolicy().hasHeightForWidth())
        self.DescBrower.setSizePolicy(sizePolicy)
        self.DescBrower.setMaximumSize(QtCore.QSize(278, 16777215))
        self.DescBrower.setLineWrapColumnOrWidth(25)
        self.DescBrower.setReadOnly(True)
        self.DescBrower.setObjectName('DescBrower')
        # 放入垂直布局
        self.showVLayout.addWidget(self.DescBrower)
        # 引入放图片的展览框
        self.showPic=QtWidgets.QLabel(self.videoInfo)
        sizePolicy=QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showPic.sizePolicy().hasHeightForWidth())
        self.showPic.setSizePolicy(sizePolicy)
        self.showPic.setMinimumSize(QtCore.QSize(493, 0))
        # 引入图片
        self.showPic.setText('')
        #self.showPic.setPixmap(QtGui.QPixmap(':/PNG/tlj1.png'))
        self.showPic.setPixmap(QtGui.QPixmap('resource/images/ifo0.jpg'))
        self.showPic.setScaledContents(True)
        self.showPic.setObjectName('showPic')
        #放入水平布局
        self.iHLayout.addWidget(self.showInfo)
        self.iHLayout.addWidget(self.showPic)


        #引入第二个视频分页
        self.download=QtWidgets.QWidget()
        self.download.setObjectName('download')
        #设置为垂直布局，并引入到主分页中
        self.dVLayout=QtWidgets.QVBoxLayout(self.download)
        self.dVLayout.setContentsMargins(-1,11,-1,-1)
        self.dVLayout.setObjectName('dVLayout')
        self.partWidget.addTab(self.download,'下载')
        # 引入放置弹幕和线程选项的水平布局
        self.dHLayout=QtWidgets.QHBoxLayout()
        self.dHLayout.setContentsMargins(-1,0,-1,-1)
        self.dHLayout.setObjectName('dHLayout')
        
        # 引入弹幕下载选择按钮
        self.XMLButton=QtWidgets.QRadioButton(self.download)
        self.XMLButton.setObjectName('XMLButton')
        self.XMLButton.setText('无弹幕')
        self.dHLayout.addWidget(self.XMLButton)
        self.XMLButton.setChecked(True)

        self.ASSButton=QtWidgets.QRadioButton(self.download)
        self.ASSButton.setObjectName('ASSButton')
        self.ASSButton.setText('ASS弹幕')
        self.dHLayout.addWidget(self.ASSButton)

        # 引入线程标签
        self.labelThreads=QtWidgets.QLabel(self.download)
        # 设置为垂直居中右对齐
        self.labelThreads.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelThreads.setObjectName('labelThreads')
        self.labelThreads.setText('线程数')
        self.dHLayout.addWidget(self.labelThreads)
        # 引入数值选择框
        self.numThreads=QtWidgets.QSpinBox(self.download)
        self.numThreads.setMinimum(2)
        self.numThreads.setMaximum(10)
        self.numThreads.setProperty('value',2)
        self.numThreads.setObjectName('numThreads')
        self.dHLayout.addWidget(self.numThreads)
        # 调整各个部件间的间距
        self.dHLayout.setStretch(0, 2)
        self.dHLayout.setStretch(1, 2)
        self.dHLayout.setStretch(2, 3)
        self.dHLayout.setStretch(3, 1)
        # 将水平布局加入垂直布局
        self.dVLayout.addLayout(self.dHLayout)
        # 引入滚动区域
        self.scroll=QtWidgets.QScrollArea(self.download)
        self.scroll.setMinimumSize(QtCore.QSize(769,441))
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('scroll')
        self.dVLayout.addWidget(self.scroll)
        # 放入容器
        self.scrollContents=QtWidgets.QWidget()
        self.scrollContents.setGeometry(QtCore.QRect(0,0,806,496))
        self.scrollContents.setObjectName('scrollContents')
        self.scroll.setWidget(self.scrollContents)
        # 设置水平布局
        self.sVLayout=QtWidgets.QVBoxLayout(self.scrollContents)
        self.sVLayout.setObjectName('sVLayout')

        # 引入图片修饰标签
        self.dlabel=QtWidgets.QLabel(self.scrollContents)
        self.dlabel.setText('')
        self.dlabel.setPixmap(QtGui.QPixmap('resource/images/video0.jpg'))
        self.dlabel.setScaledContents(True)
        self.dlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dlabel.setObjectName('dlabel')
        # 将其放入到布局中
        self.sVLayout.addWidget(self.dlabel)
        # 引入全部下载按键
        self.allDown=QtWidgets.QPushButton(self.download)
        self.allDown.setText('下载全部')
        self.allDown.setEnabled(False)
        self.allDown.setObjectName('allDown')
        self.dVLayout.addWidget(self.allDown)
        self.allDown.clicked.connect(myWindow.doAllDownload)
        # 引入第三个图片分页
        self.Picture=QtWidgets.QWidget()
        self.Picture.setObjectName('Picture')
        self.partWidget.addTab(self.Picture,'图片')
        # 引入一盒部件
        # 在这个盒子里面我们放一个开关和图片展览框
        self.boxPic=QtWidgets.QGroupBox(self.Picture)
        self.boxPic.setGeometry(QtCore.QRect(0,0,860,710))
        self.boxPic.setObjectName('boxPic')
        # 设置布局
        self.boxHLayout=QtWidgets.QHBoxLayout(self.boxPic)
        self.boxHLayout.setObjectName('boxHLayout')

        # 放入开关
        self.tBox=QtWidgets.QToolBox(self.boxPic)
        self.tBox.setMaximumSize(QtCore.QSize(145,16777215))
        self.tBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tBox.setObjectName('tBox')
        self.boxHLayout.addWidget(self.tBox)
        self.tBox1=QtWidgets.QWidget()
        self.tB1VLayout=QtWidgets.QVBoxLayout(self.tBox1)
        self.tBox1.setGeometry(QtCore.QRect(0, 0, 141, 300))
        self.tBox1.setObjectName('tBox1')
        self.tBox2=QtWidgets.QWidget()
        self.tBox2.setGeometry(QtCore.QRect(0, 0, 141, 300))
        self.tBox2.setObjectName('tBox2')
        self.tB2VLayout=QtWidgets.QVBoxLayout(self.tBox2)
        self.tBox.addItem(self.tBox1,'展开')
        self.tBox.addItem(self.tBox2,'收起')
        self.pSmall=QtWidgets.QPushButton(self.tBox1)
        #self.pSmall.setGeometry(QtCore.QRect(0, 60, 140, 40))
        self.pSmall.setText('缩小')
        self.pSmall.setObjectName('pSmall')
        self.pBig=QtWidgets.QPushButton(self.tBox1)
        #self.pBig.setGeometry(QtCore.QRect(0, 220, 140, 40))
        self.pBig.setText('放大')
        self.pBig.setObjectName('pBig')
        self.dialrotation=QtWidgets.QDial(self.tBox1)
        #self.dialrotation.setGeometry(QtCore.QRect(40, 130, 50, 64))
        self.dialrotation.setObjectName('dialrotation')
        self.tB1VLayout.addWidget(self.pBig)
        self.tB1VLayout.addWidget(self.dialrotation)
        self.tB1VLayout.addWidget(self.pSmall)
        # 引入图片下载按钮
        self.pDownload=QtWidgets.QPushButton(self.tBox2)
        self.pDownload.setMinimumSize(QtCore.QSize(0,550))
        self.pDownload.setObjectName('pDownload')
        self.pDownload.setText('下载图片')
        self.tB2VLayout.addWidget(self.pDownload)
        self.graphicsView=QtWidgets.QGraphicsView(self.boxPic)
        self.graphicsView.setObjectName('graphicsView')
        self.boxHLayout.addWidget(self.graphicsView)
        self.tBox.setCurrentIndex(1)
        ###
        self.KouDai = QtWidgets.QWidget()
        self.KouDai.setObjectName("KouDai")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.KouDai)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.kdLabel = QtWidgets.QLabel(self.KouDai)
        self.kdLabel.setObjectName("newLB")
        self.kdLabel.setText('视频分享链接')
        self.gridLayout_2.addWidget(self.kdLabel, 0, 0, 1, 1)
        self.kdLineEdit = QtWidgets.QLineEdit(self.KouDai)
        self.kdLineEdit.setObjectName("kdLineEdit")
        self.kdLineEdit.setPlaceholderText('https://xxx.com/xxxxx')
        self.gridLayout_2.addWidget(self.kdLineEdit, 0, 1, 1, 1)
        self.kdDownLoad = QtWidgets.QPushButton(self.KouDai)
        self.kdDownLoad.setObjectName("kdDownLoad")
        self.kdDownLoad.setText('下载')
        self.gridLayout_2.addWidget(self.kdDownLoad, 0, 2, 1, 1)
        self.kdpBar = QtWidgets.QProgressBar(self.KouDai)
        self.kdpBar.setProperty("value", 0)
        self.kdpBar.setObjectName("kdpBar")
        self.gridLayout_2.addWidget(self.kdpBar, 1, 0, 1, 3)
        self.kdTextBrowser = QtWidgets.QTextBrowser(self.KouDai)
        self.kdTextBrowser.setOpenExternalLinks(True)
        self.kdTextBrowser.setObjectName("kdTextBrowser")
        self.kdTextBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';text-decoration: underline; color:#ee82ee;\">使用方法</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';text-decoration: underline; color:#008B8B;\">1.在口袋48app将视频分享到微博</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';text-decoration: underline; color:#008B8B;\">2.点开微博分享连接,将弹出一个新窗口例如:</span><a href=\"https://h5.48.cn/2019appshare/memberLiveShare/?id=455489351445188608\"><span style=\" font-family:\'SimSun\'; text-decoration: underline; color:#0000ff;\">点我</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';text-decoration: underline; color:#008B8B;\">3.复制此新窗口的网址</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';text-decoration: underline; color:#008B8B;\">4.将网址黏贴到连接输入框</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';text-decoration: underline; color:#FF0000;\">5.注意：视频回放生成后才能下载</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"resource/images/tlj3.png\" /></p></body></html>")
        self.gridLayout_2.addWidget(self.kdTextBrowser, 2, 0, 1, 3)
        self.kdDownLoad.clicked.connect(myWindow.dkoudai)
        self.partWidget.addTab(self.KouDai,"口袋")
        ###
        # 引入第三个工具分页
        # 设置栅格布局
        self.vTool=QtWidgets.QWidget()
        self.vTool.setObjectName('vTool')
        self.partWidget.addTab(self.vTool,'工具')
        self.gridLayout=QtWidgets.QGridLayout(self.vTool)
        self.gridLayout.setObjectName('gridLayout')
        # 引入合并水平布局和标签
        self.CBHLayout=QtWidgets.QHBoxLayout()
        self.CBHLayout.setObjectName('CBHLayout')
        self.labelCB=QtWidgets.QLabel(self.vTool)
        self.labelCB.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCB.setText('拖拽合并视频到下方')
        self.labelCB.setObjectName('labelCB')
        self.CBHLayout.addWidget(self.labelCB)
        # 加入确认合并的按钮
        self.okCBbutton=QtWidgets.QPushButton(self.vTool)
        self.okCBbutton.setObjectName('okCBbutton')
        self.okCBbutton.setText('确认合并')
        self.okCBbutton.clicked.connect(myWindow.VideoTogther)
        self.CBHLayout.addWidget(self.okCBbutton)
        # 将上述布局放入栅格子中去
        self.gridLayout.addLayout(self.CBHLayout, 0, 0, 2, 1)
        # 引入合并盒子来接受文件,myPlainText是自己重写的类
        self.CBbox=BPlainTextEdit(self.vTool)
        self.CBbox.setObjectName('CBbox')
        self.gridLayout.addWidget(self.CBbox, 2, 0, 1, 1)
        # 引入剪切布局
        self.cutHLayout=QtWidgets.QHBoxLayout()
        self.cutHLayout.setObjectName('cutHLayout')
        #引入接受文件拖拽的标签
        self.cutLabel=BLabel(self.vTool)
        self.cutLabel.setObjectName('cutLabel')
        self.cutLabel.setText('拖拽文件到此处')
        self.cutLabel.setAcceptDrops(True)
        self.cutHLayout.addWidget(self.cutLabel)
        self.cutOpen=QtWidgets.QPushButton(self.vTool)
        self.cutOpen.setText('打开')
        self.cutOpen.setObjectName('cutOpen')
        self.cutOpen.clicked.connect(myWindow.OpenFile)
        self.cutHLayout.addWidget(self.cutOpen)
        self.gridLayout.addLayout(self.cutHLayout, 0, 1, 1, 1)
        # 剪切时间显示框和输入框
        # 引入垂直布局
        self.cutVLayout=QtWidgets.QVBoxLayout()
        self.cutVLayout.setObjectName('cutVLayout')
        # 起始标签
        self.startLabel=QtWidgets.QLabel(self.vTool)
        self.startLabel.setObjectName('startLabel')
        self.startLabel.setText('起始时间')
        self.cutVLayout.addWidget(self.startLabel)
        # 起始输入框
        self.startLine=QtWidgets.QLineEdit(self.vTool)
        self.startLine.setObjectName('startLine')
        self.startLine.setPlaceholderText('hour.minute.second')
        self.cutVLayout.addWidget(self.startLine)
        # 结束时间标签
        self.endLabel=QtWidgets.QLabel(self.vTool)
        self.endLabel.setObjectName('endLabel')
        self.endLabel.setText('结束时间')
        self.cutVLayout.addWidget(self.endLabel)
        # 结束时间输入框
        self.endLine=QtWidgets.QLineEdit(self.vTool)
        self.endLine.setObjectName('endLine')
        self.endLine.setPlaceholderText('hour.minute.second')
        self.cutVLayout.addWidget(self.endLine)
        # 确认按钮
        self.okCutbutton=QtWidgets.QPushButton(self.vTool)
        self.okCutbutton.setObjectName('okCutbutton')
        self.okCutbutton.setText('开始剪切')
        self.cutVLayout.addWidget(self.okCutbutton)
        self.okCutbutton.clicked.connect(myWindow.videoCut)
        self.gridLayout.addLayout(self.cutVLayout, 1, 1, 2, 1)
        # 引入转码功能
        self.tranCHLayout=QtWidgets.QHBoxLayout()
        self.tranCHLayout.setObjectName('tranCHLayout')
        # 引入可接受文件的标签
        self.tranCLabel=BLabel(self.vTool)
        self.tranCLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tranCLabel.setObjectName('tranCLabel')
        self.tranCLabel.setText('拖拽文件到此')
        self.tranCLabel.setAcceptDrops(True)
        self.tranCHLayout.addWidget(self.tranCLabel)
        # 引入打开文件按钮
        self.tranCopen=QtWidgets.QPushButton(self.vTool)
        self.tranCopen.setText('打开')
        self.tranCopen.setObjectName('tranCopen')
        self.tranCopen.clicked.connect(myWindow.OpenFile)
        self.tranCHLayout.addWidget(self.tranCopen)
        # 引入复选框
        self.multiBox=QtWidgets.QComboBox(self.vTool)
        self.multiBox.setObjectName('multiBox')
        self.multiBox.addItem('mp4')
        self.multiBox.addItem('flv')
        self.multiBox.addItem('wav')
        self.tranCHLayout.addWidget(self.multiBox)
        # 引入确认按钮
        self.okTranscode=QtWidgets.QPushButton(self.vTool)
        self.okTranscode.setObjectName('okTranscode')
        self.okTranscode.setText('转码')
        self.tranCHLayout.addWidget(self.okTranscode)
        self.okTranscode.clicked.connect(myWindow.convertto)
        self.gridLayout.addLayout(self.tranCHLayout, 3, 0, 1, 2)
        # 引入导出gif的工具盒
        self.gifBox=QtWidgets.QGroupBox(self.vTool)
        self.gifBox.setObjectName('gifBox')
        self.gifVLayout=QtWidgets.QVBoxLayout(self.gifBox)
        self.gifVLayout.setObjectName('gifVLayout')
        self.gifHLayout=QtWidgets.QHBoxLayout()
        self.gifHLayout.setObjectName('gifHLayout')
        # giflabel接受文件
        self.gifLabel=BLabel(self.gifBox)
        self.gifLabel.setAcceptDrops(True)
        self.gifLabel.setObjectName('gifLabel')
        self.gifLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gifLabel.setText('拖拽文件于此')
        self.gifHLayout.addWidget(self.gifLabel)
        # gifokButton 确认导出gif
        self.gifokButton=QtWidgets.QPushButton(self.gifBox)
        self.gifokButton.setObjectName('gifokButton')
        self.gifokButton.setText('导出')
        self.gifokButton.clicked.connect(myWindow.ExportGif)
        self.gifHLayout.addWidget(self.gifokButton)
        self.gifVLayout.addLayout(self.gifHLayout)
        # 引入第二个gifBox中的水平布局
        self.gifHLayout2=QtWidgets.QHBoxLayout()
        self.gifHLayout2.setObjectName('gifHLayout2')
        self.gifStart=QtWidgets.QLabel(self.gifBox)
        self.gifStart.setObjectName('gifStart')
        self.gifStart.setText('开始时间')
        self.gifHLayout2.addWidget(self.gifStart)
        self.giflineStart=QtWidgets.QLineEdit(self.gifBox)
        self.giflineStart.setObjectName('giflineStart')
        self.giflineStart.setPlaceholderText('hour.minute.second.')
        self.gifHLayout2.addWidget(self.giflineStart)
        self.gifduration=QtWidgets.QLabel(self.gifBox)
        self.gifduration.setObjectName('gifduration')
        self.gifduration.setText('持续时间')
        self.gifHLayout2.addWidget(self.gifduration)
        self.lineduration=QtWidgets.QLineEdit(self.gifBox)
        self.lineduration.setObjectName('lineduration')
        self.lineduration.setPlaceholderText('秒(s)')
        self.gifHLayout2.addWidget(self.lineduration)
        self.gifVLayout.addLayout(self.gifHLayout2)
        # 引入第三层水平布局，主要是一些gif质量选项
        self.gifHLayout3=QtWidgets.QHBoxLayout()
        self.gifHLayout3.setObjectName('gifHLayout3')
        self.lineSize=QtWidgets.QLineEdit(self.gifBox)
        self.lineSize.setObjectName('lineSize')
        self.lineSize.setPlaceholderText('输入尺寸,格式(300x400)')
        self.gifHLayout3.addWidget(self.lineSize)
        self.frameLabel=QtWidgets.QLabel(self.gifBox)
        self.frameLabel.setObjectName('frameLabel')
        self.frameLabel.setText('帧数')
        self.gifHLayout3.addWidget(self.frameLabel)
        self.frameChoice=QtWidgets.QSpinBox(self.gifBox)
        self.frameChoice.setMinimum(1)
        self.frameChoice.setProperty('value', 10)
        self.frameChoice.setObjectName('frameChoice')
        self.gifHLayout3.addWidget(self.frameChoice)
        self.gifVLayout.addLayout(self.gifHLayout3)
        self.gridLayout.addWidget(self.gifBox, 4, 0, 1, 2)
        # 调整布局间的比例
        self.gridLayout.setColumnStretch(0, 4)
        self.gridLayout.setColumnStretch(1, 2)
        # 引入安利布局
        self.TabAnLi=QtWidgets.QWidget()
        self.TabAnLi.setObjectName('TabAnLi')
        self.AnliVLayout=QtWidgets.QVBoxLayout(self.TabAnLi)
        self.AnliVLayout.setObjectName('AnliVLayout')
        self.labelshowliga=QtWidgets.QLabel(self.TabAnLi)
        self.labelshowliga.setText('')
        #self.labelshowliga.setPixmap(QtGui.QPixmap(':/PNG/tlj2.png'))
        self.labelshowliga.setPixmap(QtGui.QPixmap('resource/images/note0.png'))
        self.labelshowliga.setScaledContents(True)
        self.labelshowliga.setObjectName('labelshowliga')
        self.NoteBrowser=QtWidgets.QTextBrowser(self.TabAnLi)
        self.NoteBrowser.setOpenExternalLinks(True)
        self.NoteBrowser.setObjectName('NoteBrowser')
        self.NoteBrowser.setMinimumSize(QtCore.QSize(0,150))
        self.AnliVLayout.setStretch(0, 4)
        self.AnliVLayout.setStretch(1, 3)
        self.AnliVLayout.addWidget(self.labelshowliga)
        self.AnliVLayout.addWidget(self.NoteBrowser)
        self.NoteBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; text-decoration: underline; color:#c71585;\">欢迎关注</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-weight:600;\">1.</span><a href=\"https://space.bilibili.com/14574654\"><span style=\" font-family:\'SimSun\'; text-decoration: underline; color:#0000ff;\">作者B站主页</span></a></p>\n"
"</body></html>")
        self.partWidget.addTab(self.TabAnLi,'说明')


        # 剪切板事件捕获
        self.clipboard=QtWidgets.QApplication.clipboard()
        self.clipboard.dataChanged.connect(myWindow.copyEvent)
        #self.okbuttonBV.clicked.connect(myWindow.okbuttonBV)
        # 允许通过objectname 触发信息传递
        QtCore.QMetaObject.connectSlotsByName(myWindow)


class myui(QtWidgets.QMainWindow):
    # flp这个变量在程序第一次运行时防止clearAll函数运行
    flp=False
    # 下面三个变量也是同样的效果
    flp_video=False
    flp_picture=False
    flp_No_download=True
    # 定义两个信号分别在新老视频下载完成后发送
    VideoCombine=QtCore.pyqtSignal(int)
    #OldVideoCombine=QtCore.pyqtSignal(int)
    # 记录已经开始下载的项目
    down_list=[]
    T1=0
    T2=0
    T3=0
    total=0

    def __init__(self, filetmp, filesave):
        super().__init__()
        self.ui=Windows()
        self.ui.SetUi(self)
        #self.OldVideoCombine.connect(self.OldCB)
        self.VideoCombine.connect(self.do_Combine)
        # 引入一个定时器，监视下载进度
        self.CompleteTimer=QtCore.QTimer()
        self.CompleteTimer.stop()
        self.CompleteTimer.setInterval(1000)
        self.CompleteTimer.timeout.connect(self.showProgress)
        self.filetmp = filetmp
        self.filesave = filesave


    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_F1:
            if self.ui.partWidget.currentIndex()==0:
                self.T1+=1
                self.ui.showPic.setPixmap(QtGui.QPixmap(f'resource/images/ifo{self.T1%3}.jpg'))
            elif self.ui.partWidget.currentIndex()==1:
                self.T2+=1
                self.ui.dlabel.setPixmap(QtGui.QPixmap(f'resource/images/video{self.T2%3}.jpg'))
            elif self.ui.partWidget.currentIndex()==5:
                self.T3+=1
                self.ui.labelshowliga.setPixmap(QtGui.QPixmap(f'resource/images/note{self.T3%3}.png'))


    def copyEvent(self):
        """ 获取剪切板内容 """
        content=self.ui.clipboard.text()
        if (len(content)<10) or ('BV' not in content):
            if 'av' in content:
                content=search('av[0-9]+',content).group()[2:]
                content=BiliDecoder(int(content))
            else:
                return None
        
        content=search(compile(r'BV\w+'),content).group()
        self.ui.lineBV.setText(content[2:])


    @QtCore.pyqtSlot(bool)
    def on_okbuttonBV_clicked(self):
        self.bv=self.ui.lineBV.text()
        if not self.bv:
            return None
        self.ui.partWidget.setCurrentIndex(0)
        if self.flp:
            self.clearAll()
        self.dgrouplist=[]
        # 一些信号翻转
        self.flp=True
        self.flp_picture=True
        self.flp_video=True
        # 存储bv号
        self.url_1=PLAY_URL+self.bv
        self.cidlist,*_rest,dim,self.picurl=apiget(API_URL+self.bv)
        self.num_video=len(self.cidlist)
        self.dimx=dim[0][0]
        self.dimy=dim[0][1]
        self.ui.showChart.setItem(0,0,QtWidgets.QTableWidgetItem(f'{_rest[0]}'))
        self.ui.showChart.setItem(1,0,QtWidgets.QTableWidgetItem(f'{_rest[1]}'))
        self.ui.showChart.setItem(2,0,QtWidgets.QTableWidgetItem(f'{_rest[2]}'))
        self.ui.showChart.setItem(3,0,QtWidgets.QTableWidgetItem(f'{_rest[3]}'))
        self.ui.showChart.setItem(4,0,QtWidgets.QTableWidgetItem(f'{_rest[4]}'))
        self.ui.showChart.setItem(5,0,QtWidgets.QTableWidgetItem(f'{_rest[5]}'))
        self.ui.showChart.setItem(6,0,QtWidgets.QTableWidgetItem(f'{self.dimx}x{self.dimy}'))
        self.ui.DescBrower.setText(_rest[6])


    @QtCore.pyqtSlot(int)
    def on_partWidget_currentChanged(self,n):
        if n==1 and self.flp_video:
            self.flp_video=False
            self.ui.allDown.setEnabled(True)
            num=0
            for i in self.cidlist:
                container.append([])
                dgroup=QtWidgets.QGroupBox(self.ui.scrollContents)
                dgroup.setTitle(f'{num+1}')
                dgroup.setObjectName(f'dgroup{num}')
                dgVLayout=QtWidgets.QVBoxLayout(dgroup)
                dgVLayout.setObjectName(f'dgVLayout{num}')
                labeltitle=QtWidgets.QLabel(dgroup)
                labeltitle.setObjectName(f'labeltitle{num}')
                labeltitle.setText(f'{i}')
                dgHLayout=QtWidgets.QHBoxLayout()
                dgHLayout.setObjectName(f'dgHLayout{num}')
                dgHLayout.addWidget(labeltitle)
                dButton=QtWidgets.QPushButton(dgroup)
                dButton.setMinimumSize(QtCore.QSize(72,0))
                dButton.setObjectName(f'dButton{num}')
                dButton.setText('下载')
                dgHLayout.addWidget(dButton)
                dgHLayout.setStretch(0,5)
                dgHLayout.setStretch(1,2)
                dgVLayout.addLayout(dgHLayout)
                pBar=QtWidgets.QProgressBar(dgroup)
                pBar.setProperty('value',0)
                pBar.setObjectName(f'pBar{num}')
                dgVLayout.addWidget(pBar)
                self.ui.sVLayout.addWidget(dgroup)
                num+=1
                dButton.clicked.connect(self.down_start)
                self.pBarlist=self.ui.scrollContents.findChildren(QtWidgets.QProgressBar)
                self.dgrouplist=self.ui.scrollContents.findChildren(QtWidgets.QGroupBox)
        elif n==2 and self.flp_picture:
            self.flp_picture=False
            data=Fetch(self.picurl,default_headers).content
            img=QtGui.QImage.fromData(data)
            piximg=QtGui.QPixmap.fromImage(img)
            self.picContent=QtWidgets.QGraphicsPixmapItem(piximg)
            self.scene=QtWidgets.QGraphicsScene()
            self.scene.addItem(self.picContent)
            self.ui.graphicsView.setScene(self.scene)


    def clearAll(self):
        global counts
        if self.dgrouplist==[]:
            return None
        for i in self.dgrouplist:
            self.ui.sVLayout.removeWidget(i)
            sip.delete(i)
        for i in range(len(container)):
            container.pop()
        self.down_list=[]
        self.CompleteTimer.stop()
        counts=-1
        self.flp_No_download=True
        # self.ui.allDown.setEnabled(False)
        self.ui.allDown.setText('下载全部')
        self.total=0


    def down_start(self):
        self.total+=1
        sender=self.sender()
        index=int(sender.objectName().replace('dButton',''))
        pbar=self.pBarlist[index]
        pbar.setMaximum(0)
        sender.setEnabled(False)
        sender.setText('下载中..')
        threadnum=self.ui.numThreads.value()
        pbar.threadnum=threadnum
        self.down_list.append(index)
        if self.ui.ASSButton.isChecked():
            if self.num_video>1:
                self.damku=downloadAss(self.cidlist[index],self.filesave+self.bv+'_'+f'{index}',self.dimx,self.dimy)
            else:
                self.damku=downloadAss(self.cidlist[index],self.filesave+self.bv,self.dimx,self.dimy)
            self.damku.start()
        if self.num_video==1:
            # 1Ct411u7Yr
            self.t=downThread(self.url_1,self.bv,threadnum,0, self.filetmp)
            self.t.start()
        else:
            # 1Ct411u7Yr_i
            self.t=downThread(self.url_1+f'?p={index+1}',self.bv+f'_{index}',threadnum,index, self.filetmp)
            self.t.start()
        if self.flp_No_download:
            # 当没有下载任务时才重启计数器
            self.CompleteTimer.start()
            self.flp_No_download=False


    def doAllDownload(self):
        self.ui.allDown.setEnabled(False)
        self.ui.allDown.setText('全部下载中...')
        self.timerAllDownload = QtCore.QTimer()
        self.timerAllDownload.stop()
        self.timerAllDownload.setInterval(5000)
        self.timerAllDownload.timeout.connect(self.do_all_download)
        self.timerAllDownload.start()
        self.do_all_download()


    def do_all_download(self):
        if len(self.down_list) < 2:
            if self.total >= self.num_video:
                # 所有下载项目已经触发
                # 看是否已经下载完成
                if not self.down_list:
                    # 关闭计时器
                    self.timerAllDownload.stop()
                    self.ui.allDown.setText('下载完成!!!')
            else:
                pushbutton_list = self.ui.scrollContents.findChildren(QtWidgets.QPushButton)
                for i in pushbutton_list:
                    if i.isEnabled():
                        i.click()
                        break


    def showProgress(self):
        if not self.down_list:
            # 如果没有下载任务则关闭计时器
            self.flp_No_download=True
            self.CompleteTimer.stop()
        else:
            for i in self.down_list:
            #仅仅对已经加入下载列表的项目改变进度条
                if contain:=len(container[i]):
                    # contain>0说明已经有一部分下载完成
                    # 我们修改对应进度条的值
                    tpBar=self.pBarlist[i]
                    todu=2*tpBar.threadnum
                    # 因子2是包含了视频和音频
                    tpBar.setMaximum(100)
                    tpBar.setValue(100*contain//(todu))
                    if contain==todu:
                        #下载完成,从下载列表中删除
                        self.down_list.remove(i)
                        self.VideoCombine.emit(i)


    # 合并新视频的音源和画面源
    def do_Combine(self,index):
        if self.num_video>1:
            title=self.bv+f'_{index}'
        else:
            title=self.bv
        self.CB=ThreadCombine(
            index,
            self.filetmp+title+'_video.flv',
            self.filetmp+title+'_audio.flv',
            self.filesave+title+'.flv'
        )
        self.CB.Combine_Signal.connect(self.Complete)
        self.CB.start()


    # 合并视频完成
    def Complete(self,index):
        self.ui.scrollContents.findChildren(QtWidgets.QPushButton)[index].setText('完成')


    def convertcomplete(self):
        self.ui.okTranscode.setEnabled(True)
        self.ui.okTranscode.setText('转码')


    # 图片处理
    ############
    @QtCore.pyqtSlot(bool)
    def on_pDownload_clicked(self):
        formatp=self.picurl.split('.')[-1]
        filename=self.filesave+self.bv+'.'+formatp
        self.pd=ThreadPicDownload(self.picurl,filename)
        self.pd.start()


    @QtCore.pyqtSlot(bool)
    def on_pBig_clicked(self):
        self.picContent.setScale(self.picContent.scale()+0.2)


    @QtCore.pyqtSlot(bool)
    def on_pSmall_clicked(self):
        self.picContent.setScale(self.picContent.scale()-0.2)


    @QtCore.pyqtSlot(int)
    def on_dialrotation_valueChanged(self,v):
        degree=v*180//99
        if degree>90:
            self.picContent.setRotation(degree-180)
        else:
            self.picContent.setRotation(degree)


    def dkoudai(self):
        self.timerkd = QtCore.QTimer()
        self.timerkd.stop()
        self.timerkd.setInterval(1000)
        self.timerkd.timeout.connect(self.putprogressbar1)
        url = self.ui.kdLineEdit.text().strip()
        self.timerkd.start()
        self.ui.kdpBar.setMaximum(0)
        self.kou = koudaigo(url)
        self.kou.start()


    def putprogressbar1(self):
        if DownLoad_M3U8.isCompl:
            pass
        else:
            self.timerkd.stop()
            DownLoad_M3U8.ck = []
            DownLoad_M3U8.koudaicc = []
            DownLoad_M3U8.Counts = 0
            self.ui.kdLineEdit.clear()
            self.ui.kdpBar.setValue(0)
            self.ui.kdLineEdit.setText('视频回放还未生成,少侠请稍安勿躁')
            return None
        if not DownLoad_M3U8.ck:
            pass
        else:
            total = DownLoad_M3U8.ck[0]
            lc = len(DownLoad_M3U8.koudaicc)
            self.ui.kdpBar.setMaximum(100)
            self.ui.kdpBar.setValue(100*lc//total)
            if lc == total:
                self.timerkd.stop()
                DownLoad_M3U8.ck = []
                DownLoad_M3U8.koudaicc = []
                DownLoad_M3U8.Counts = 0
                self.ui.kdLineEdit.clear()
                self.ui.kdpBar.setValue(0)


    def VideoTogther(self):
        text=self.ui.CBbox.toPlainText()
        if not text:
            return None
        self.ui.okCBbutton.setEnabled(False)
        self.ui.okCBbutton.setText('合并中')
        tt = text.split('\n')[0]
        _, formatp = path.splitext(tt)
        basep = path.dirname(tt)
        self.uv = ThreadVideoTogther(text, basep, formatp)
        self.uv.signac.connect(self.videoTogtherdo)
        self.uv.start()


    def videoTogtherdo(self):
        self.ui.okCBbutton.setEnabled(True)
        self.ui.okCBbutton.setText('开始')


    def OpenFile(self):
        if (sender:=self.sender()) == self.ui.cutOpen:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", './', "Video(*.mp4 *.flv *mkv *mpeg)")
            self.ui.cutLabel.setText(filename.strip())
        elif sender == self.ui.tranCopen:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", './', "Video(*.mp4 *.flv *mkv *mpeg)")
            self.ui.tranCLabel.setText(filename.strip())


    def ExportGif(self):
        filename = self.ui.gifLabel.text().strip()
        if not filename:
            return None
        starttime = Tconvert(self.ui.giflineStart.text())
        endtime = Tconvert(self.ui.lineduration.text())
        resize = self.ui.lineSize.text()
        framerate = self.ui.frameChoice.value()
        self.gif = ThreadGifExport(filename, starttime, endtime, resize, framerate)
        self.gif.start()


    def videoCut(self):
        ff = self.ui.cutLabel.text().strip()
        if not ff:
            return None
        _, formatp = path.splitext(ff)
        starttime = Tconvert(self.ui.startLine.text())
        endtime = Tconvert(self.ui.endLine.text())
        self.ct = ThreadCutVideo(ff, starttime, endtime, formatp)
        self.ct.start()


    def convertto(self):
        ff = self.ui.tranCLabel.text().strip()
        if not ff:
            return None
        self.ui.okTranscode.setEnabled(False)
        self.ui.okTranscode.setText('转码中..')
        filepath = path.dirname(ff)
        toformat = self.ui.multiBox.currentText()
        fileout = filepath + '/' + f'output.{toformat}'
        self.myconv = ThreadtransfVideo(ff,fileout)
        self.myconv.signcv.connect(self.convertcomplete)
        self.myconv.start()


class koudaigo(QtCore.QThread):
    def __init__(self, url):
        super(koudaigo, self).__init__()
        self.url = url
    def run(self):
        DownLoad_M3U8(self.url).begin()


class ThreadtransfVideo(QtCore.QThread):
    signcv = QtCore.pyqtSignal()
    def __init__(self, inputf, outputf):
        super().__init__()
        self.filename = inputf
        self.outfile = outputf
        self.formatv = outputf.split('.')[-1]
    def run(self):
        if self.formatv == 'mp4':
            cmd(['ffmpeg', '-i', self.filename, '-c:v', 'h264_qsv', '-preset:v', 'faster', '-y', self.outfile,'-loglevel','quiet'])
        else:
            cmd(['ffmpeg', '-i', self.filename, '-y', self.outfile,'-loglevel','quiet'])
        self.signcv.emit()


# 合并新视频进程
class ThreadCombine(QtCore.QThread):
    Combine_Signal=QtCore.pyqtSignal(int)
    def __init__(self,index,f1,f2,f3):
        super().__init__()
        self.index=index
        self.f1=f1
        self.f2=f2
        self.f3=f3
    def run(self):
        #'-loglevel','quiet'
        cmd(['ffmpeg','-i',self.f1,'-i',self.f2,'-map','0:v','-map','1:a','-c:a','copy','-c:v','copy','-y',self.f3,'-loglevel','quiet'])
        # cmd(['ls', '-l'])
        self.Combine_Signal.emit(self.index)


class ThreadCutVideo(QtCore.QThread):
    def __init__(self, filename, x, y, z):
        super().__init__()
        self.filename = filename
        self.starttime = x
        self.endtime = y
        self.outfile = path.dirname(filename)+'/'+f'cut{z}'
    def run(self):
        cmd(['ffmpeg', '-ss', self.starttime, '-i', self.filename, '-to', self.endtime, '-c', 'copy', '-copyts', '-y', self.outfile,'-loglevel','quiet'])


# 下载弹幕进程
class downloadAss(QtCore.QThread):
    def __init__(self,cid,filename,x,y):
        super().__init__()
        self.cid=cid
        self.file=filename
        self.x=int(x)
        self.y=int(y)
    def run(self):
        tmp='https://api.bilibili.com/x/v1/dm/list.so?oid='+str(self.cid)
        data=Fetch(tmp,default_headers).content
        with open(self.file+'.xml','wb') as f:
            f.write(data)
        if self.x:
            xta.Danmaku2ASS(self.file+'.xml','autodetect',self.file+'.ass',self.x,self.y,font_size=float(45),text_opacity=0.7,duration_marquee=float(7))
        else:
            print('视频尺寸缺省！')


# 下载视频进程
class downThread(QtCore.QThread):
    def __init__(self,url,title,threadnum,index, filetmp):
        super().__init__()
        self.url=url
        self.title=title
        self.threadnum=threadnum
        self.index=index
        self.filetmp = filetmp
    def run(self):
        download(self.url,self.title,self.threadnum,self.index, self.filetmp)


# 图片下载
class ThreadPicDownload(QtCore.QThread):
    def __init__(self,url,filename):
        super().__init__()
        self.url=url
        self.file=filename
    def run(self):
        data=Fetch(self.url,default_headers).content
        with open(self.file,'wb') as fileob:
            fileob.write(data)


class ThreadVideoTogther(QtCore.QThread):
    signac = QtCore.pyqtSignal()
    def __init__(self,filetext, outpath, formatp):
        super().__init__()
        self.filetext = 'file ' + filetext.replace('\n', '\nfile ')
        self.outfile = outpath + '/' + f'combine{formatp}'
    def run(self):
        with open('combine.txt', 'w') as f:
            f.write(self.filetext)
        cmd(['ffmpeg','-f','concat','-safe','0','-i','combine.txt','-c','copy','-y',self.outfile,'-loglevel','quiet'])
        self.signac.emit()


class ThreadGifExport(QtCore.QThread):
    def __init__(self, filename, starttime, endtime, resize, framerate):
        super().__init__()
        self.filename = filename
        self.starttime = starttime
        self.endtime = endtime
        self.resize = resize
        self.framerate = framerate
    def run(self):
        _path, _ = path.splitext(self.filename)
        outfile = _path + '.gif'
        print(self.endtime,self.starttime)
        cmd(['ffmpeg', '-ss', self.starttime, '-i', self.filename, '-t', str(self.endtime), '-s', self.resize, '-r', f'{self.framerate}', '-y', outfile,'-loglevel','quiet'])


def init():
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('fusion'))
    app=QtWidgets.QApplication([])
    return app