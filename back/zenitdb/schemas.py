from typing_extensions import Annotated
from pydantic import BaseModel,BeforeValidator
from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator
from userdef import user_validators
from enum import Enum
import jdatetime


# 'd|w|m|y.0|1|-1'
def parse_ZDate(v):
    if(v == None):
        return None

    if isinstance(v, datetime):
        return v        

    d = v.lower().split('.')

    flag = d[0]
    try:
        nums = int(d[1])
    except:
        nums = 0
        
    base = jdatetime.datetime.today()
    base = jdatetime.datetime(year=base.year, month=base.month, day=base.day)
    
    result = None

    if(flag == 'n'):
        result = jdatetime.datetime.now()
    elif(flag == 'd'):
        result = base + timedelta(days=nums)
    elif(flag == 'w'):
        result =  base + timedelta(days=((nums * 7) - base.weekday()))
    elif(flag == 'm'):
        ym = divmod(base.month - 1 + nums, 12)
        result = jdatetime.datetime(year = base.year + ym[0], month = ym[1] + 1, day = 1)
    elif(flag == 'y'):
        result = jdatetime.datetime(year = base.year + nums, month = 1, day = 1)
    else:
        return v
        
    return result.togregorian()

ZDate = Annotated[datetime, BeforeValidator(parse_ZDate)]

class History(BaseModel):
    history_id: int
    history_editor: int
    history_thing_type: str
    history_thing_Id: int
    history_date: datetime
    history_data: str


#region user


### User ###
class User(BaseModel):
    id: int = 0
    user_name: str | None = None # 
    user_mobile: str | None = None # 
    user_tel: str | None = None # 
    user_country: str | None = None # 
    user_city: str | None = None # 
    user_lang: str | None = None # 
    user_group_id: int = 0 # 
    user_smshour: int | None = None # 
    user_access: str | None = None # 
    user_ack: bool | None = None # 
    user_active: bool | None = None # 
    user_bdate: ZDate | None = None # 
    user_money: int | None = None # 
    user_iswomen: bool | None = None # 
    user_smslevel: str | None = None # 
    user_smsfinishdate: ZDate | None = None # 
    user_telegram_session: str | None = None # 

class User_patch(BaseModel):

    user_name: str | None = None
    user_mobile: str | None = None
    user_tel: str | None = None
    user_country: str | None = None
    user_city: str | None = None
    user_lang: str | None = None
    user_group_id: int | None = None
    user_smshour: int | None = None
    user_access: str | None = None
    user_ack: bool | None = None
    user_active: bool | None = None
    user_bdate: ZDate | None = None
    user_money: int | None = None
    user_iswomen: bool | None = None
    user_smslevel: str | None = None
    user_smsfinishdate: ZDate | None = None
    user_telegram_session: str | None = None

#endregion user

#region group


### Group ###
class Group(BaseModel):
    id: int = 0
    group_name: str | None = None # 
    group_poshtiban_id: int = 0 # 
    group_start_date: ZDate | None = None # 
    group_start_page: int | None = None # 
    group_assign_day: ZDate | None = None # 
    group_uc: int | None = None # 
    group_type: int | None = None # 0>normal,1>private,2>freerun

class Group_post(BaseModel):

    group_name: str = None
    group_poshtiban_id: int
    group_start_date: ZDate = None
    group_start_page: int = None
    group_assign_day: ZDate = None
    group_uc: int = None
    group_type: int = None

class Group_patch(BaseModel):

    group_name: str | None = None
    group_poshtiban_id: int | None = None
    group_start_date: ZDate | None = None
    group_start_page: int | None = None
    group_assign_day: ZDate | None = None
    group_uc: int | None = None
    group_type: int | None = None

#endregion group

#region assign


### Assign ###
class Assign(BaseModel):
    id: int = 0
    assign_user_id: int = 0 # 
    assign_moment: ZDate | None = None # 
    assign_pagenumber: int | None = None # 
    assign_status: int | None = None # 
    assign_done_moment: ZDate | None = None # 
    assign_follow_result: str | None = None # 

class Assign_post(BaseModel):

    assign_user_id: int
    assign_moment: ZDate = None
    assign_pagenumber: int = None
    assign_status: int = None
    assign_done_moment: ZDate = None
    assign_follow_result: str = None

#endregion assign

#region payment


### Payment ###
class Payment(BaseModel):
    id: int = 0
    py_user_id: int = 0 # 
    py_amount: int | None = None # 
    py_desc: str | None = None # 
    py_state: int | None = None # 
    py_date: ZDate | None = None # 
    py_RefId: str | None = None # 
    py_xpaypingrequestid: str | None = None # 

#endregion payment

#region sms


### Sms ###
class Sms(BaseModel):
    id: int = 0
    user_id: int = 0 # 
    sms_messageId: str | None = None # 
    sms_moment: str | None = None # 
    sms_receptor: str | None = None # 
    sms_message: str | None = None # 
    sms_status: bool | None = None # 
    sms_cost: int | None = None # 

#endregion sms


