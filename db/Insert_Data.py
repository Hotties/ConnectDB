import pymysql
from parser.make_class import Item, cmpr_Item, cmpr_Dtl
from error import InsertError
from typing import List

def Insert_Item(cur: pymysql.cursors.Cursor, _Item: Item, conn: pymysql.Connection):
    try:
        query = """
            INSERT IGNORE INTO ITEM 
            (measure_Year, achl_Kind_Code, achl_Kind_Nm, sample_Cnt, sample_Rm)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            _Item.measure_Year,
            _Item.achl_Kind_Code,
            _Item.achl_Kind_Nm,
            _Item.sample_Cnt,
            _Item.sample_Rm
        ))
        conn.commit()
        return cur.rowcount
    except pymysql.MySQLError as e:
        raise InsertError(f"[Insert_Item] DB 삽입 실패: {e}")

def Insert_cmpr_Item(cur: pymysql.cursors.Cursor, _Item: Item, _cmpr_Item: cmpr_Item, conn: pymysql.Connection):
    try:
        query = """
            INSERT IGNORE INTO CMPR_ITEM_LIST
            (cmpr_Item_Code, cmpr_Item_Nm, measure_Year, achl_Kind_Code)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (
            _cmpr_Item.cmpr_Item_Code,
            _cmpr_Item.cmpr_Item_Nm,
            _Item.measure_Year,
            _Item.achl_Kind_Code
        ))
        conn.commit()
        return cur.rowcount
    except pymysql.MySQLError as e:
        raise InsertError(f"[Insert_cmpr_Item] DB 삽입 실패: {e}")

def Insert_cmpr_Dtl(cur: pymysql.cursors.Cursor, _cmprItem: cmpr_Item, _cmprDtl: cmpr_Dtl, conn: pymysql.Connection):
    try:
        query = """
            INSERT IGNORE INTO CMPR_DTL_LIST
            (cmpr_Dtl_Code, cmpr_Dtl_Nm, cmpr_Dtl_Engl_Nm, sfe, prsiundo, in_Value,
             mouthresdng, ctmouthresdng, f_Value, p_Value, 
             cmpr_Item_Code, measure_Year, achl_Kind_Code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            _cmprDtl.cmpr_Dtl_Code,
            _cmprDtl.cmpr_Dtl_Nm,
            _cmprDtl.cmpr_Dtl_Engl_Nm,
            _cmprDtl.sfe,
            _cmprDtl.prsiundo,
            _cmprDtl.in_Value,
            _cmprDtl.mouthresdng,
            _cmprDtl.ctmouthresdng,
            _cmprDtl.f_Value,
            _cmprDtl.p_Value,
            _cmprItem.cmpr_Item_Code,
            _cmprItem.measure_Year,
            _cmprItem.achl_Kind_Code
        ))
        conn.commit()
        return cur.rowcount
    except pymysql.MySQLError as e:
        raise InsertError(f"[Insert_cmpr_Dtl] DB 삽입 실패: {e}")
