import typing
import logging

import azure.functions as func

import Crawling
import Slack

app = func.FunctionApp()

def debug(func):
    def wrapper():
        try:
            func()
        except Exception as e:
            Slack.sendTextWithLink(str(e), "")
@debug
@app.function_name(name="noticeNotifierTimer")
@app.schedule(schedule="0 */30 * * * *", arg_name="noticeNotifierTimer", run_on_startup=False,
              use_monitor=False) 
def noticeNotifier(noticeNotifierTimer:func.TimerRequest) -> None:
    logging.info("noticeNotifier called.")
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
            mostRecentNotices = p.getMostRecentNotice()
            for title, url in mostRecentNotices:
                Slack.sendTextWithLink(title, url)
            p.runAll()
            logging.info(f"{p.name} updated. slack message was sent.")

@app.function_name(name="tester")
@app.route(route="test", auth_level=func.AuthLevel.ANONYMOUS)
def tester(req:func.HttpRequest) -> func.HttpResponse:
    Bachelor = Crawling.Sogang(Crawling.BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/bachelor.txt", "학사공지")
    logging.info("test.")
    Bachelor.getSoup()
    tmp = Bachelor.getPostCount()
    Slack.sendTextWithLink(f'Test: {tmp}', "https://test.com")
    return func.HttpResponse(str(tmp))
