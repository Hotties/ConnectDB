import requests
import json
import xmltodict
import api.constant as constant
import error
from api.file_writer import FileWriter

writer = FileWriter()

def check_serviceKey():
    if not hasattr(constant, "serviceKey"):
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
    

def apiConnect(measure_Year,achl_Kind_Code,cmpr_Item_Code, writer):

    check_serviceKey()

    print(f"{measure_Year}년도 api 연결 시도...")
    
    param = {'serviceKey' : constant.serviceKey,'measure_Year' : measure_Year,'achl_Kind_Code':achl_Kind_Code}
    response = requests.get(constant.url,params=param)

    print(f"api response code : {response.status_code}")

    check_api_connect(response_status_code = response.status_code)
    

    data_xml = xmltodict.parse(response.text)
    ##data = json.dumps(data_xml, ensure_ascii=False, indent=4)
    
 
    check_api_reponse(_data = data_xml)

    writer.write(data_xml)


