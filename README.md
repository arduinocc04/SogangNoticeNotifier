# HelpSogang
## 사용법
[Solve the dreadful certificate issues in Python requests module](https://levelup.gitconnected.com/solve-the-dreadful-certificate-issues-in-python-requests-module-2020d922c72f)에서 하라는 대로 해서 pem 파일을 만들고, `requests.get(verify=PEM_FILE_NAME)`에 넣는다.

혹시라도 위 링크가 날아갈까봐.. pem 파일 만드는 법을 적어두면, 크롬에서 주소창 왼쪽 자물쇠 모양 클릭하면, 또 자물쇠 모양이 뜬다. 인증서 표시(인증서가 유효함으로 써져 있을 것임)를 클릭한 후 뜨는 창에서 세부 정보를 클릭하면 인증서 계층을 볼 수 있다. 이를 모두 der로 다운로드 한 후, `openssl x509 -in DER_FILE_NAME -inform DER -outform PEM >> PEM_OUT_NAME`을 모든 der 파일에 대해 반복하면 된다. PEM_OUT_NAME은 모두 같아야 한다.

firefox dev edition(일반 에디션도 됨) 사용하면 인증서 chain을 한번에 받을 수 있음. 자물쇠 클릭하고 connection secure -> More information 가서 밑으로 내리다보면  Miscellaneous 있는데 거기서 pem (chain) 클릭하면 다운 받을 수 있음. 
