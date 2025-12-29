import json
from parser.make_class import Item,cmpr_Item,cmpr_Dtl
import api.connect_api as connect_api

def parsing(writer):
    
    file_number = writer.file_number
    print(f"{file_number} : 파일넘버")
    
    with open(f'response{file_number-1}.json','r',encoding='utf-8') as f:
        datas = json.load(f)
     
        item = parsing_Item(datas)
        cmpr = parsing_cmpr_Item_List(item,datas)
        print(cmpr[0].cmpr_Item_Code)
        cmpr_Item_Code_list = []
        for i in cmpr:
             cmpr_Item_Code_list.append(i.cmpr_Item_Code)
        cmpr_Dtl = parsing_cmpr_Dtl_List(item, cmpr_Item_Code_list, datas)
        
        return item,cmpr,cmpr_Dtl
        

def parsing_Item(datas):

    try:
        item_List = datas["response"]["body"]["items"]["item"]
            
            # items가 리스트라면 첫 번째 요소를 사용
        if isinstance(item_List, list):
                first_item = item_List[0]  # 리스트에서 첫 번째 항목 가져오기
        else:
                first_item = item_List  # 만약 딕셔너리라면 그대로 사용
        print(first_item["measure_Year"])
            # Item 객체 생성
        item = Item(first_item["measure_Year"],
                    first_item["achl_Kind_Code"],
                    first_item["achl_Kind_Nm"],
                    first_item["sample_Cnt"],
                    first_item["sample_Rm"])
        

        print(item.__dict__)  # 객체 정보를 출력
        
    except KeyError as e:
        print(f"KeyError 발생1: {e}")  # 키 오류가 발생하면 출력
        return 0
    return item

def parsing_cmpr_Item_List(item, datas):

    measure_Year = item.measure_Year
    achl_Kind_Code = item.achl_Kind_Code
    try:
        cmpr_Item_List = datas["response"]["body"]["items"]["item"]["cmpr_Item_List"]["item"]
        if isinstance(cmpr_Item_List, list):
                first_item = cmpr_Item_List[0]  # 리스트에서 첫 번째 항목 가져오기
        else:
                first_item = cmpr_Item_List  # 만약 딕셔너리라면 그대로 사용
            
            # cmpr_list 객체 생성
        cmpr_list:list[cmpr_Item] = list()
        for a in cmpr_Item_List:
            #print(a["cmpr_Item_Code"],a["cmpr_Item_Nm"])
            cmpr_list.append(cmpr_Item(a["cmpr_Item_Code"],a["cmpr_Item_Nm"],measure_Year,achl_Kind_Code))
        
    except KeyError as e:
        print(f"KeyError 발생: {e}")  # 키 오류가 발생하면 출력
        return 0
    return cmpr_list

def parsing_cmpr_Dtl_List(item, cmpr_Item_Code_List, datas):
    measure_Year = item.measure_Year
    achl_Kind_Code = item.achl_Kind_Code

    try:
        cmpr_Dtl_List = datas["response"]["body"]["items"]["item"]["cmpr_Item_List"]["item"]
        
        if isinstance(cmpr_Dtl_List, list):
                first_item = cmpr_Dtl_List[0]  # 리스트에서 첫 번째 항목 가져오기
        else:
                first_item = cmpr_Dtl_List  # 만약 딕셔너리라면 그대로 사용
        dtl_list:list[cmpr_Dtl] = list()
        for i in range(len(cmpr_Item_Code_List)):
            cmpr_Dtl_List2 = cmpr_Dtl_List[i]["cmpr_Dtl_List"]["item"]
            for a in cmpr_Dtl_List2:
                dtl_list.append(cmpr_Dtl(a["cmpr_Dtl_Code"],a["cmpr_Dtl_Nm"],a["cmpr_Dtl_Engl_Nm"],a["sfe"],a["prsiundo"]
                                         ,a["in_Value"],a["mouthresdng"],a["ctmouthresdng"],a["f_Value"],a["p_Value"]
                                         ,i,measure_Year,achl_Kind_Code))
    except KeyError as e:
        print(f"KeyError 발생: {e}")  # 키 오류가 발생하면 출력
        return 0
    return dtl_list