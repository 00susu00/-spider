import requests
from bs4 import BeautifulSoup#美味汤
import re#正则表达式库
import jieba#引入结巴库
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def getHTMLText(url):
    try:
        r=requests.get(url)#get方法取到数据
        r.encoding=r.apparent_encoding#修改编码保证解析UTF-8
        r.raise_for_status()#status确保web返回
        return r.text#返回get法取到的数据，数据类型为标签集
    except:
        return("shit")
    
def parsePage(ilt,html):#页面有效信息提取函数，输入值分别为储存字符串ilt和页面信息html
    soup=BeautifulSoup(html,"lxml")#煲汤
    end=soup.find_all(name=re.compile('ul'))#find_all取出标签ul中的字符串
    for end in end:
        ilt=ilt+str(end.text)#循环取不同页面的有效信息
    return(ilt)#返回有效信息

def settleList(ilt,DS):#结巴处理有效信息
    mm="".join(ilt.split('\n'))
    words=jieba.lcut(mm)#先把所有数据都变成列表
    DS.extend(words)#将每一次循环出的列表都加入新的列表中
    return(DS)
    
def settleStr(ilt):
    mm="".join(ilt.split('\n'))
    wordlist_after_jieba = jieba.cut(mm, cut_all=True)
    dsstr = " ".join(wordlist_after_jieba)
    return(dsstr)

def stopwordslist(dsstrs):
    print(dsstrs)
    stopwords=[]
    stopwords = [line.strip() for line in open('C:/Users/ASUS/Desktop/stopwords.txt').readlines()]
    print(stopwords)
    words=jieba.cut(dsstrs,cut_all=True)
    stayed_line=""
    for word in words:
        if word in stopwords:
            pass
        else:
            stayed_line+=word+" "
    return(stayed_line)
    
def printdic(ds):
    counts = {}
    for d in ds:
        if len(d) == 1:    # 单个词语不计算在内
            continue
        else:
            counts[d] = counts.get(d, 0) + 1#计数
    print(list(counts.items()))
    file_handle=open('C:/Users/ASUS/Desktop/1.txt',mode='w')
    file_handle.write(str(counts.items()))#将列表写成元组存入
    
def printpic(outstr):
    my_wordcloud = WordCloud(background_color="white",width=1000,height=860, font_path="C:\\Windows\\Fonts\\STFANGSO.ttf").generate(outstr)
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()
    my_wordcloud.to_file("C:/Users/ASUS/Desktop/temp.png")
    
def main():
    depth=41
    start_url="https://news.bupt.edu.cn/jxky/"#初始网址
    ilt=""
    DS=[]
    for i in range(depth):
        try:
            url=start_url+str(i+17)+".htm"
            html=getHTMLText(url)
            m=parsePage(ilt,html)
            dsstrs=settleStr(m)
            ds=settleList(m,DS)
        except:
            continue
    outstr=stopwordslist(dsstrs)
    printdic(ds)
    printpic(outstr)
    
    
main()