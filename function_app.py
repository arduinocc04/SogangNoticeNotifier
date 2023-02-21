import typing
import logging

import azure.functions as func

import Crawling
import Slack

app = func.FunctionApp()

@app.function_name(name="noticeNotifierTimer")
@app.schedule(schedule="0 */30 * * * *", arg_name="noticeNotifierTimer", run_on_startup=False,
              use_monitor=False) 
def noticeNotifier(noticeNotifierTimer:func.TimerRequest) -> None:
    logging.info("noticeNotifier called.")
    Bachelor = Crawling.Post(Crawling.BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/bachelor.txt", "학사공지")
    Scholar = Crawling.Post(Crawling.SCHOLARSHIP_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/scholarship.txt", "장학공지")
    General = Crawling.Post(Crawling.GENERAL_SUPPORT_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/generalSupport.txt", "일반지원")
    Onestop = Crawling.Post(Crawling.ONESTOP_SOGANG_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/onestopSogang.txt", "onestop")

    posts:typing.List[Crawling.Post] = [Bachelor, Scholar, General, Onestop]

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
    Bachelor = Crawling.Post(Crawling.BACHELOR_NOTICE_LINK, Crawling.PEM_FILE_LOCATION, Crawling.HEADERS, "NoticeUpdateData/bachelor.txt", "학사공지")
    logging.info("test.")
    Bachelor.getSoup()
    tmp = Bachelor.getPostCount()
    Slack.sendTextWithLink(f'Test: {tmp}', "https://test.com")
    return func.HttpResponse(str(tmp))
