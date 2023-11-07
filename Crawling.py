import typing
import hashlib

from bs4 import BeautifulSoup, ResultSet
import requests

HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
COOKIES = {'session_id': 'sorryidontcare'}

BACHELOR_NOTICE_LINK = "https://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=2"
SCHOLARSHIP_NOTICE_LINK = "https://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=141"
GENERAL_SUPPORT_NOTICE_LINK = "https://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=34"
ONESTOP_SOGANG_LINK = "https://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=3"

CSE_IMPORTANT_NOTICE_LINK = "https://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=cs&bbsConfigFK=1905"
CSE_BACHELOR_NOTICE_LINK = "https://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=cs&bbsConfigFK=1745"
CSE_GRADUATE_NOTICE_LINK = "https://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=cs&bbsConfigFK=1747"
CSE_GENERAL_NOTICE_LINK = "https://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=cs&bbsConfigFK=1746"
CSE_EMPLOY_INTERN_NOTICE_LINK = "https://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=cs&bbsConfigFK=1748"
CSE_CLASS_NOTICE_LINK = "https://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=cs&bbsConfigFK=1749"

PEM_FILE_LOCATION = "NoticeUpdateData/verify.pem"



def numWithCommaToInt(n:str) -> int:
    res = ""
    for c in n:
        if not 48 <= ord(c) <= 57: continue
        res += c
    return int(res)

def ifLeftDateIsRecentThanRight(a:str, b:str) -> bool:
    ay, am, ad = int(a[:4]), int(a[5:7]), int(a[-2:])
    by, bm, bd = int(b[:4]), int(b[5:7]), int(b[-2:])
    if ay > by: return True
    elif ay < by: return False

    if am > bm: return True
    elif am < bm: return False

    if ad > bd: return True
    return False

def textToHash(text:str) -> str:
    h = hashlib.sha256()
    h.update(text.encode('utf-8'))
    return h.hexdigest()

def noticesToHash(notices:typing.List[typing.Tuple[str, str]]) -> str:
    a = ""
    for n in notices:
        a += n[0]
    return textToHash(a)

class Sogang:
    def __init__(self, url:str, verifyFile:str, headers:dict, dataFileName:str, name:str) -> None:
        self.url:str = url
        self.verifyFile:str = verifyFile
        self.headers:dict = headers
        self.dataFileName:str = dataFileName
        self.name:str = name
        self.soup:BeautifulSoup = None #type:ignore

    def getPostCount(self) -> int:
        assert(self.soup != None)
        cnt = numWithCommaToInt(self.soup.select_one("em").get_text()) #type:ignore
        return cnt

    def getSoup(self) -> None:
        page = requests.get(self.url, verify = False, headers = self.headers)
        self.soup = BeautifulSoup(page.text, "html.parser")

    def getNotices(self) -> typing.List[BeautifulSoup]:
        assert(self.soup != None)
        return self.soup.find_all('tr', 'notice')

    def getMostRecentNotice(self) -> typing.List[typing.Tuple[str, str]]:
        assert(self.soup != None)
        notices = self.getNotices()

        mostRecentDate = "-123.-1.-1"
        for n in notices:
            date = n.find_all("td")[4].get_text().rstrip().lstrip()
            if ifLeftDateIsRecentThanRight(date, mostRecentDate):
                mostRecentDate = date
        res:typing.List[typing.Tuple[str, str]] = []
        for n in notices:
            if n.find_all("td")[4].get_text().rstrip().lstrip() == mostRecentDate:
                titleSoup:BeautifulSoup = n.find_all("td")[1]
                titleLink = "https://www.sogang.ac.kr" + titleSoup.select("div > a")[0]['href'].replace('¤', '&') #type:ignore
                title = self.name + titleSoup.select("div > a > span")[0].get_text()
                res.append((title, titleLink))
        return res
    
    def getTopCount(self) -> int:
        assert(self.soup != None)
        notices = self.getNotices()
        cnt = 0
        for n in notices:
            if n.select("td > span")[0].get_text() == "TOP":
                cnt += 1
        return cnt
    
    def getCountAll(self) -> int:
        return self.getTopCount() + self.getPostCount()

    def saveDataFile(self, num:int) -> None:
        with open(self.dataFileName, 'w+t') as f:
            f.write(str(num))

    def readDataFile(self) -> int:
        with open(self.dataFileName, 'r') as f:
            return int(f.readline())

    def existDifference(self) -> bool:
        return self.getCountAll() != self.readDataFile()

    def runAll(self) -> None:
        cnt = self.getCountAll()
        if self.existDifference(): self.saveDataFile(cnt)

class SogangCSE:
    def __init__(self, url:str, verifyFile:str, headers:dict, dataFileName:str, name:str) -> None:
        self.url:str = url
        self.verifyFile:str = verifyFile
        self.headers:dict = headers
        self.dataFileName:str = dataFileName
        self.name:str = name
        self.soup:BeautifulSoup = None #type:ignore

    def getSoup(self) -> None:
        page = requests.get(self.url, verify = False, headers = self.headers)
        self.soup = BeautifulSoup(page.text, "html.parser")

    def getNotices(self) -> ResultSet:
        assert(self.soup != None)
        noticeListSoup = self.soup.select("div.list_box")[0]
        noticeSoups = noticeListSoup.select("ul > li > div")
        return noticeSoups

    def getMostRecentNotice(self) -> typing.List[typing.Tuple[str, str]]:
        assert(self.soup != None)
        notices = self.getNotices()

        mostRecentDate = "-123.-1.-1"
        for n in notices:
            date = n.select("div")[0].find_all("span")[1].get_text().rstrip().lstrip()
            if ifLeftDateIsRecentThanRight(date, mostRecentDate):
                mostRecentDate = date
        res:typing.List[typing.Tuple[str, str]] = []
        for n in notices:
            if n.select("div")[0].find_all("span")[1].get_text().rstrip().lstrip() == mostRecentDate:
                titleSoup:BeautifulSoup = n.select("a")[0]
                titleLink = "https://scc.sogang.ac.kr" + titleSoup['href'].replace('¤', '&') #type:ignore
                title = self.name + titleSoup.get_text()
                res.append((title, titleLink))
        return res

    def saveDataFile(self, text:str) -> None:
        with open(self.dataFileName, 'w+t') as f:
            f.write(text)

    def readDataFile(self) -> str:
        with open(self.dataFileName, 'r') as f:
            return f.readline()

    def existDifference(self) -> bool:
        return noticesToHash(self.getMostRecentNotice()) != self.readDataFile()

    def runAll(self) -> None:
        mostRecent = noticesToHash(self.getMostRecentNotice())
        if self.existDifference(): self.saveDataFile(mostRecent)
