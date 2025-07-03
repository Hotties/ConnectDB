class Item:
    def __init__(self, measure_Year, achl_Kind_Code, achl_Kind_Nm, sample_Cnt, sample_Rm):
        self.measure_Year = int(measure_Year)
        self.achl_Kind_Code = int(achl_Kind_Code)
        self.achl_Kind_Nm = achl_Kind_Nm
        self.sample_Cnt = int(sample_Cnt)
        self.sample_Rm = sample_Rm


class cmpr_Item:
    def __init__(self, cmpr_Item_Code, cmpr_Item_Nm, measure_Year, achl_Kind_Code):
        self.cmpr_Item_Code = int(cmpr_Item_Code)
        self.cmpr_Item_Nm = cmpr_Item_Nm
        self.measure_Year = int(measure_Year)
        self.achl_Kind_Code = int(achl_Kind_Code)


class cmpr_Dtl:
    def __init__(self, cmpr_Dtl_Code, cmpr_Dtl_Nm, cmpr_Dtl_Engl_Nm,
                 sfe, prsiundo, in_Value, mouthresdng,
                 ctmouthresdng, f_Value, p_Value,
                 cmpr_Item_Code, measure_Year, achl_Kind_Code):
        
        self.cmpr_Dtl_Code = int(cmpr_Dtl_Code)
        self.cmpr_Dtl_Nm = cmpr_Dtl_Nm
        self.cmpr_Dtl_Engl_Nm = cmpr_Dtl_Engl_Nm
        self.sfe = sfe
        self.prsiundo = prsiundo
        self.in_Value = in_Value
        self.mouthresdng = float(mouthresdng) if mouthresdng else None
        self.ctmouthresdng = float(ctmouthresdng) if ctmouthresdng else None
        self.f_Value = float(f_Value) if f_Value else None
        self.p_Value = float(p_Value) if p_Value else None
        self.cmpr_Item_Code = int(cmpr_Item_Code)
        self.measure_Year = int(measure_Year)
        self.achl_Kind_Code = int(achl_Kind_Code)
