import Crawling
import Slack
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler('log/noticeNotifier.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def noticeNotifier() -> None:
    logger.info("executed noticeNotifier.")
    Bachelor = Crawling.Sogang(Crawling.BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/bachelor.txt", "<학사공지>")
    Scholar = Crawling.Sogang(Crawling.SCHOLARSHIP_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/scholarship.txt", "<장학공지>")
    General = Crawling.Sogang(Crawling.GENERAL_SUPPORT_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/generalSupport.txt", "<일반지원>")
    Onestop = Crawling.Sogang(Crawling.ONESTOP_SOGANG_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/onestopSogang.txt", "<onestop>")
    Gen = Crawling.Sogang(Crawling.GENERAL_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/general.txt", "<일반공지>")
    Fes = Crawling.Sogang(Crawling.FEST_SPLEC_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/fest.txt", "<행사특강>")

    cseImp = Crawling.SogangOther(Crawling.CSE_IMPORTANT_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseImportant.txt", "<[컴공과]주요공지>", "https://cs.sogang.ac.kr")
    cseBa = Crawling.SogangOther(Crawling.CSE_BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseBa.txt", "<[컴공과]학사공지>", "https://cs.sogang.ac.kr")
    cseGrad = Crawling.SogangOther(Crawling.CSE_GRADUATE_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseGrad.txt", "<[컴공과]대학원공지>", "https://cs.sogang.ac.kr")
    cseGen = Crawling.SogangOther(Crawling.CSE_GENERAL_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseGen.txt", "<[컴공과]일반공지>", "https://cs.sogang.ac.kr")
    cseEmIn = Crawling.SogangOther(Crawling.CSE_EMPLOY_INTERN_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseEmIn.txt", "<[컴공과]취업인턴십공지>", "https://cs.sogang.ac.kr")
    cseCls = Crawling.SogangOther(Crawling.CSE_CLASS_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseCls.txt", "<[컴공과]학과공지>", "https://cs.sogang.ac.kr")

    wholeBa = Crawling.SogangOther(Crawling.WHOLEEDU_BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/wholeBa.txt", "<[전인교육원]학사공지>", "https://scc.sogang.ac.kr")
    wholeStu = Crawling.SogangOther(Crawling.WHOLEEDU_STUDENT_CONTEST_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/wholeStu.txt", "<[전인교육원]학생참여대회>", "https://scc.sogang.ac.kr")
    wholeGen = Crawling.SogangOther(Crawling.WHOLEEDU_GENERAL_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/wholeGen.txt", "<[전인교육원]일반공지>", "https://scc.sogang.ac.kr")
    wholeNews = Crawling.SogangOther(Crawling.WHOLEEDU_NEWS_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/wholeNews.txt", "<[전인교육원]뉴스>", "https://scc.sogang.ac.kr")

    chaCen = Crawling.SogangOther(Crawling.CHARACTERDEV_CENTER_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/chaCen.txt", "<[인성교육센터]센터공지>", "https://character.sogang.ac.kr")
    chaCha = Crawling.SogangOther(Crawling.CHARACTERDEV_CHARACTERDEV_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/chaCha.txt", "<[인성교육센터]인성교육원공지>", "https://character.sogang.ac.kr")

    globalNotice = Crawling.SogangOther(Crawling.GLOBAL_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/globalNotice.txt", "<[국제학생교육센터]공지>", "https://globaledu.sogang.ac.kr")
    globalNews = Crawling.SogangOther(Crawling.GLOBAL_NEWS_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/globalNews.txt", "<[국제학생교육센터]뉴스>", "https://globaledu.sogang.ac.kr")
    globalActivity = Crawling.SogangOther(Crawling.GLOBAL_GLOBALSTUDENT_ACTIVITY_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/globalActivity.txt", "<[국제학생교육센터]국제학생활동정보>", "https://globaledu.sogang.ac.kr")

    converNotice = Crawling.SogangOther(Crawling.CONVERGENCEEDU_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/converNotice.txt", "<[융합교육원]공지사항>", "https://convedu.sogang.ac.kr")

    posts = [Bachelor, Scholar, General, Onestop, Gen, Fes, cseImp, cseBa, cseGrad, cseGen, cseEmIn, cseCls, wholeBa, wholeStu, wholeGen, wholeNews, chaCen, chaCha, globalNotice, globalNews, globalActivity, converNotice]

    for p in posts:
        p.getSoup()
        if p.existDifference():
            logger.info(f"{p.name} is changed.")
            mostRecentNotices = p.getMostRecentNotice()
            for title, url in mostRecentNotices:
                Slack.sendTextWithLink(title, url)
            p.runAll()

if __name__ == "__main__":
    noticeNotifier()