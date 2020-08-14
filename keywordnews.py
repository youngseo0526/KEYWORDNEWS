# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5 import uic
import feedparser
import newspaper
from konlpy.tag import Mecab
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gtts import gTTS
import os
from PIL import Image

MainUI = 'main.ui'
MenuUI = 'menu.ui'
OpenUI = 'opening.ui'

def rss_link(num):
    rss = ['http://www.khan.co.kr/rss/rssdata/total_news.xml',
           'http://www.khan.co.kr/rss/rssdata/politic_news.xml',
           'http://www.khan.co.kr/rss/rssdata/economy_news.xml',
           'http://www.khan.co.kr/rss/rssdata/society_news.xml',
           'http://www.khan.co.kr/rss/rssdata/kh_world.xml',
           'http://www.khan.co.kr/rss/rssdata/kh_sports.xml',
           'http://www.khan.co.kr/rss/rssdata/culture_news.xml',
           'http://www.khan.co.kr/rss/rssdata/kh_entertainment.xml',
           'http://www.khan.co.kr/rss/rssdata/it_news.xml']
    return rss[num-1]

def links_crawling(rss):
    feeds = feedparser.parse(rss)
    links = [entry['link'] for entry in feeds['entries']]
    return links

def news_makefile():
    global links
    global num
    global newstext
    article = newspaper.Article(links[num], language='ko')
    article.download()
    article.parse()
    newstext = article.text
    engine = Mecab()
    nouns = engine.nouns(newstext)
    nouns = [n for n in nouns if len(n) > 1]
    count = Counter(nouns)
    tags = count.most_common(20)
    text = " 제목은  " + article.title + " 입니다.  " + "키워드는  " + str(tags[0][0]) + "  " + str(tags[1][0]) + "  " + str(tags[2][0]) + "  " + str(tags[3][0]) + "  " + str(tags[4][0])
    tts = gTTS(text + "입니다.  이 기사를 읽으려면 2번, 다음 기사의 키워드는 3번, 분야선택(홈)은 1번 입니다", lang='ko')
    if os.path.isfile('keyword.mp3') == True:
        os.remove('keyword.mp3')
    tts.save('keyword.mp3')
    wc = WordCloud(font_path='c:\\windows\\fonts\\NanumSquareR.ttf', background_color='white', width=500, height=400)
    cloud = wc.generate_from_frequencies(dict(tags))
    fig = plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    fig.savefig('keyword.jpg')
    Image.open('keyword.jpg').resize((700, 650)).save('keyword.jpg')


class PopUp(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        global newstext
        global area
        uic.loadUi(MenuUI, self)
        self.textBrowser.close()
        self.show()
        self.label_4.setText('분야 : ' + area)
        self.keywordplay()
        self.show_img()
        self.num_pushButton_1.setShortcut("1")
        self.num_pushButton_2.setShortcut("2")
        self.num_pushButton_3.setShortcut("3")
        self.num_pushButton_1.clicked.connect(lambda: self.keywordoff())
        self.num_pushButton_1.clicked.connect(lambda: self.close())
        self.num_pushButton_2.clicked.connect(lambda: self.keywordoff())
        self.num_pushButton_2.clicked.connect(lambda: self.newsread())
        self.num_pushButton_2.clicked.connect(lambda: self.textBrowser.setText(newstext))
        self.num_pushButton_2.clicked.connect(lambda: self.textBrowser.show())
        self.num_pushButton_3.clicked.connect(lambda: self.textBrowser.close())
        self.num_pushButton_3.clicked.connect(lambda: self.keywordoff())
        self.num_pushButton_3.clicked.connect(lambda: self.nextkeyword())
        self.num_pushButton_3.clicked.connect(lambda: self.show_img())
        self.num_pushButton_3.clicked.connect(lambda: self.keywordplay())

    def nextkeyword(self):
        global num
        num = num + 1
        news_makefile()

    def newsread(self):
        global newstext
        tts2 = gTTS("선택하신 기사 내용은   " + newstext, lang='ko')
        if os.path.isfile('news_all.mp3') == True:
            os.remove('news_all.mp3')
        tts2.save("news_all.mp3")
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("news_all.mp3")))
        self.player.play()

    def keywordplay(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("keyword.mp3")))
        self.player.play()

    def keywordoff(self):
        self.player.stop()

    def show_img(self):
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("keyword.jpg")
        self.label_view.setPixmap(self.qPixmapVar)


class MainDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        uic.loadUi(MainUI, self)
        self.show()
        self.menuplay()
        self.num_pushButton_1.setShortcut("1")
        self.num_pushButton_2.setShortcut("2")
        self.num_pushButton_3.setShortcut("3")
        self.num_pushButton_4.setShortcut("4")
        self.num_pushButton_5.setShortcut("5")
        self.num_pushButton_6.setShortcut("6")
        self.num_pushButton_7.setShortcut("7")
        self.num_pushButton_8.setShortcut("8")
        self.num_pushButton_9.setShortcut("9")
        self.num_pushButton_0.setShortcut("0")
        self.num_pushButton_1.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_1.clicked.connect(lambda state, button = 1: self.NumClicked(state, button))
        self.num_pushButton_1.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_2.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_2.clicked.connect(lambda state, button = 2: self.NumClicked(state, button))
        self.num_pushButton_2.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_3.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_3.clicked.connect(lambda state, button = 3: self.NumClicked(state, button))
        self.num_pushButton_3.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_4.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_4.clicked.connect(lambda state, button = 4: self.NumClicked(state, button))
        self.num_pushButton_4.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_5.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_5.clicked.connect(lambda state, button = 5: self.NumClicked(state, button))
        self.num_pushButton_5.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_6.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_6.clicked.connect(lambda state, button = 6: self.NumClicked(state, button))
        self.num_pushButton_6.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_7.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_7.clicked.connect(lambda state, button = 7: self.NumClicked(state, button))
        self.num_pushButton_7.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_8.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_8.clicked.connect(lambda state, button = 8: self.NumClicked(state, button))
        self.num_pushButton_8.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_9.clicked.connect(lambda: self.menuoff())
        self.num_pushButton_9.clicked.connect(lambda state, button = 9: self.NumClicked(state, button))
        self.num_pushButton_9.clicked.connect(lambda: PopUp(self))
        self.num_pushButton_0.clicked.connect(self.close)

    def NumClicked(self, state, button):
        global links
        global num
        global area
        num = 0
        arealist = ['전체','정치', '경제', '사회', '국제', '스포츠', '문화', '연예', 'IT']
        links = links_crawling(rss_link(button))
        area = arealist[button-1]
        news_makefile()


    def menuplay(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("menu.mp3")))
        self.player.play()

    def menuoff(self):
        self.player.stop()


class Opening(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        uic.loadUi(OpenUI, self)
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("opening.mp3")))
        self.player.play()
        self.btn_start.clicked.connect(lambda: self.player.stop())
        self.btn_start.clicked.connect(lambda: MainDialog(self))

# 메뉴.mp3 만드는 코드
def menu_make():
    tts = gTTS(text=" 분야를 골라주세요. 1번은 전체 2번은 정치 3번은 경제 4번은 사회 5번은 국제 6번은 스포츠 7번은 문화 8번은 연예 9번은 IT입니다.", lang='ko')
    tts.save("menu.mp3")
# menu_make()

def opening_tts():
    tts = gTTS(text="  반갑습니다. keywordnews 프로그램에 오신 것을 환영합니다.", lang='ko')
    tts.save("opening.mp3")
# opening_tts()

links = []
num = 0
newstext = ''
text = ''
area = ''

app = QApplication(sys.argv)
Program = Opening()
Program.show()
app.exec_()