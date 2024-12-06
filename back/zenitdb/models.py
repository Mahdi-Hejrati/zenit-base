from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from .database import Base

DATABSE_SIGNATURE = "f1150ced76ff6bbe8b95d7263bb472b7"

class zenitSetting(Base):
    __tablename__ = "zenitSetting"

    zs_id = Column(String(100), primary_key=True)
    user_id = Column(Integer, primary_key=True)
    zs_vl = Column(String(4096), index=False)


class History(Base):
    __tablename__ = "history"

    history_id = Column(Integer, primary_key=True)
    history_editor = Column(Integer)
    history_thing_type = Column(String(100))
    history_thing_Id = Column(Integer)
    history_date = Column(DateTime)
    history_data = Column(JSON)


### User ###
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_login = Column(String(256))
    user_pass = Column(String(256))
    user_name = Column(String(256), index=False) # 
    user_mobile = Column(String(256), index=False) # 
    user_tel = Column(String(256), index=False) # 
    user_country = Column(String(256), index=False) # 
    user_city = Column(String(256), index=False) # 
    user_lang = Column(String(256), index=False) # 
    user_group_id = Column(Integer) # 
    user_smshour = Column(Integer, index=False) # 
    user_access = Column(String(256), index=False) # 
    user_ack = Column(Boolean, index=False) # 
    user_active = Column(Boolean, index=False) # 
    user_bdate = Column(DateTime, index=False) # 
    user_money = Column(Integer, index=False) # 
    user_iswomen = Column(Boolean, index=False) # 
    user_smslevel = Column(String(256), index=False) # 
    user_smsfinishdate = Column(DateTime, index=False) # 
    user_telegram_session = Column(String(256), index=False) # 


### Group ###
class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    group_name = Column(String(256), index=False) # 
    group_poshtiban_id = Column(Integer) # 
    group_start_date = Column(DateTime, index=False) # 
    group_start_page = Column(Integer, index=False) # 
    group_assign_day = Column(DateTime, index=False) # 
    group_uc = Column(Integer, index=False) # 
    group_type = Column(Integer, index=False) # 0>normal,1>private,2>freerun


### Assign ###
class Assign(Base):
    __tablename__ = "assign"

    id = Column(Integer, primary_key=True)
    assign_user_id = Column(Integer) # 
    assign_moment = Column(DateTime, index=False) # 
    assign_pagenumber = Column(Integer, index=False) # 
    assign_status = Column(Integer, index=False) # 
    assign_done_moment = Column(DateTime, index=False) # 
    assign_follow_result = Column(String(4096), index=False) # 


### Payment ###
class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True)
    py_user_id = Column(Integer) # 
    py_amount = Column(Integer, index=False) # 
    py_desc = Column(String(256), index=False) # 
    py_state = Column(Integer, index=False) # 
    py_date = Column(DateTime, index=False) # 
    py_RefId = Column(String(256), index=False) # 
    py_xpaypingrequestid = Column(String(256), index=False) # 


### Sms ###
class Sms(Base):
    __tablename__ = "sms"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer) # 
    sms_messageId = Column(String(256), index=False) # 
    sms_moment = Column(String(256), index=False) # 
    sms_receptor = Column(String(256), index=False) # 
    sms_message = Column(String(256), index=False) # 
    sms_status = Column(Boolean, index=False) # 
    sms_cost = Column(Integer, index=False) # 



