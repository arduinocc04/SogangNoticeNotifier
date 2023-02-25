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

    cseImp = Crawling.SogangCSE(Crawling.CSE_IMPORTANT_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseImportant.txt", "<[컴공과]주요공지>")
    cseBa = Crawling.SogangCSE(Crawling.CSE_BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseBa.txt", "<[컴공과]학사공지>")
    cseGrad = Crawling.SogangCSE(Crawling.CSE_GRADUATE_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseGrad.txt", "<[컴공과]대학원공지>")
    cseGen = Crawling.SogangCSE(Crawling.CSE_GENERAL_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseGen.txt", "<[컴공과]일반공지>")
    cseEmIn = Crawling.SogangCSE(Crawling.CSE_EMPLOY_INTERN_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseEmIn.txt", "<[컴공과]취업인턴십공지>")
    cseCls = Crawling.SogangCSE(Crawling.CSE_CLASS_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/cseCls.txt", "<[컴공과]학과공지>")


    posts = [Bachelor, Scholar, General, Onestop, cseImp, cseBa, cseGrad, cseGen, cseEmIn, cseCls]

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