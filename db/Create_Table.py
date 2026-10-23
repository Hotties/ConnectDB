from enum import UNIQUE

import pymysql.cursors

def create_Item(cur: pymysql.cursors.Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ITEM (
            measure_Year INT,
            achl_Kind_Code INT,
            achl_Kind_Nm CHAR(50),
            sample_Cnt INT,
            sample_Rm CHAR(100),
            PRIMARY KEY (measure_Year, achl_Kind_Code)
        )
    """)

def create_cmpr_Item_List(cur: pymysql.cursors.Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS CMPR_ITEM_LIST (
            cmpr_Item_Code INT,
            cmpr_Item_Nm CHAR(50),
            measure_Year INT,
            achl_Kind_Code INT,
            FOREIGN KEY (measure_Year, achl_Kind_Code)
                REFERENCES ITEM(measure_Year, achl_Kind_Code),
            PRIMARY KEY (cmpr_Item_Code, measure_Year, achl_Kind_Code)
        )
    """)

## 해당 외래키는 CMPR_ITEM_LIST 테이블의 (cmpr_Item_Code, measure_Year, achl_Kind_Code) 컬럼을 참조합니다.
##기존에는 (cmpr_Item_Code,measure_Year)을 외래키로 설정했지만, 유일성 보장이 되지않기 때문에 부모의 유일성을 보장하는 컬럼까지 포함하여 외래키를 설정했습니다.
def create_Dtl_List(cur: pymysql.cursors.Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS CMPR_DTL_LIST (
            cmpr_Dtl_Code INT,
            cmpr_Dtl_Nm CHAR(50),
            cmpr_Dtl_Engl_Nm CHAR(50),
            sfe CHAR(50),
            prsiundo CHAR(50),
            in_Value CHAR(50),
            mouthresdng FLOAT,
            ctmouthresdng FLOAT,
            f_Value FLOAT,
            p_Value FLOAT,
            cmpr_Item_Code INT,
            measure_Year INT,
                
            achl_Kind_Code INT,
            FOREIGN KEY (cmpr_Item_Code, measure_Year, achl_Kind_Code)
                REFERENCES CMPR_ITEM_LIST(cmpr_Item_Code, measure_Year, achl_Kind_Code),
            PRIMARY KEY (cmpr_Dtl_Code, cmpr_Item_Code, measure_Year, achl_Kind_Code)
        )
    """)
