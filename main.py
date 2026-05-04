

import pymysql.cursors
import api.Connect_Api as connect_api
import parser.Parsing_Data as parsing_Data
from db.Connect_Db import db_Connect
import db.Create_Table as Create_Table
import db.Insert_Data as Insert_Data
from api.File_Writer import FileWriter

def main():

    ## db 연결
    conn = db_Connect()
 
    cur = conn.cursor()

    ## 관련 테이블 생성    
    Create_Table.create_Item(cur)
    Create_Table.create_cmpr_Item_List(cur)
    Create_Table.create_Dtl_List(cur)

    ##결과 입력 함수 생성
    writer = FileWriter()

    for code in range(435001,435002):

        print(f"{code}번 코드 처리중 ...")

        ## api 연결
        try:    
            connect_api.apiConnect(2015,code,writer)
        except Exception as e:
            print(f"{code}코드 api 연결 실패: {e}")
            continue

        ## 데이터 파싱 
        Item,cmpr_Item_List,Dtl_List = parsing_Data.parsing(writer)

        # for i in Dtl_List:  
        #     print(f"Item: {i.__dict__}")
        
        ## 데이터 삽입
        Item_rowCount = Insert_Data.Insert_Item(cur,Item,conn)
            
        print(Item_rowCount)

        cmpr_Item_rowCount,cmpr_Dtl_rowCount=0,0

        #cmpr_Item_rowCount = Insert_Data.cmpr_Item(cur,Item,cmpr_Item_List,conn)

        for cmpr_Item in cmpr_Item_List:
            cmpr_Item_rowCount += Insert_Data.Insert_cmpr_Item(cur,Item,cmpr_Item,conn)
        print(f"cmpr_Item_rowCount: {cmpr_Item_rowCount}")

        #cmpr_Dtl_rowCount = Insert_Data.Insert_cmpr_Dtl(cur,Item,Dtl_List,conn)
        for cmpr_Dtl in Dtl_List:
            cmpr_Dtl_rowCount += Insert_Data.Insert_cmpr_Dtl(cur,cmpr_Dtl,conn)
        print(f"cmpr_Dtl_rowCount: {cmpr_Dtl_rowCount}")

    conn.close()

if __name__ == "__main__":
    main()
