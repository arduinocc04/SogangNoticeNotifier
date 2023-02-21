# HelpSogang
## 사용법
[Solve the dreadful certificate issues in Python requests module](https://levelup.gitconnected.com/solve-the-dreadful-certificate-issues-in-python-requests-module-2020d922c72f)에서 하라는 대로 해서 pem 파일을 만들고, `requests.get(verify=PEM_FILE_NAME)`에 넣는다.

혹시라도 위 링크가 날아갈까봐.. pem 파일 만드는 법을 적어두면, 크롬에서 주소창 왼쪽 자물쇠 모양 클릭하면, 또 자물쇠 모양이 뜬다. 인증서 표시(인증서가 유효함으로 써져 있을 것임)를 클릭한 후 뜨는 창에서 세부 정보를 클릭하면 인증서 계층을 볼 수 있다. 이를 모두 der로 다운로드 한 후, `openssl x509 -in DER_FILE_NAME -inform DER -outform PEM >> PEM_OUT_NAME`을 모든 der 파일에 대해 반복하면 된다. PEM_OUT_NAME은 모두 같아야 한다.

## Azure functions 사용법
vscode에서 debug 한번 누르고 deploy해야 될것..(아마? 안 해도 될지도?) V2가 좋겠지 싶어서 그냥 써봤는데.. 웬만하면 V1쓰자.. V1도 잘 안된다... V2됐다!!!!!!!!: `pip freeze > requirements.txt`해주니까 됨!!
### Timer Trigger
```python
@app.function_name(name="TIMER_NAME")
@app.schedule(schedule="0 */30 * * * *", arg_name="TIMER_NAME", run_on_startup=False,
              use_monitor=False) 
def noticeNotifier(TIMER_NAME:func.TimerRequest) -> None:
    ...
```
형식으로 사용해야함. `TIMER_NAME`은 모두 같아야 하고, return도 None이어야 함.
### HTTP Trigger
```python
@app.function_name(name="A")
@app.route(route="B")
def C(req:func.HttpRequest) -> func.HttpResponse:
    ...
```
아마 `app.function_name`에 들어가는 `name`과 `def`한 함수 이름은 상관 없을 것임(아닐수도??). `req`라는 이름의 매개변수가 꼭 필요하고, `return`도 꼭 `func.HttpResponse`여야 함.