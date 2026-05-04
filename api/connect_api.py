import requests
import xmltodict
from api.Constant import _constants as constant
import error
from api.File_Writer import FileWriter

writer = FileWriter()

def check_serviceKey():
    
    if getattr(constant, "serviceKey", None) is None:   
        raise error.ServiceKeyError()   
    
def check_api_connect(response_status_code):
    if response_status_code != 200:
        raise error.ApiConnectError(response_status_code)
    
def check_api_reponse(_data):
    if "OpenAPI_ServiceResponse" in _data:
        code = _data["OpenAPI_ServiceResponse"]["cmmMsgHeader"]["returnReasonCode"]
        raise error.APIResponseError(code, "OpenAPI 라우팅 오류")
    
    code = _data["response"]["header"]["result_Code"]
    print(f"code : {code}")

    msg = _data["response"]["header"]["result_Msg"]
    print(f"code : {code}")

    if code != "200":
        raise error.APIResponseError(code,msg)

def apiConnect(measure_Year,achl_Kind_Code, writer):

    check_serviceKey()
    print(f"{measure_Year}년도 api 연결 시도...")
    param = {'serviceKey' : constant.serviceKey,'measure_Year' : measure_Year,'achl_Kind_Code':achl_Kind_Code}
    response = requests.get(constant.url,params=param)
    
    print(constant.url)

    print(f"api response code : {response.status_code}")

    check_api_connect(response_status_code = response.status_code)
    

    data_xml = xmltodict.parse(response.text)
    writer.write(data_xml)

    check_api_reponse(_data = data_xml)



