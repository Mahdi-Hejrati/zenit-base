""" 

*** Zenit

This file contains template for Hook function in Zenit

you can copy this function def to userdef file and use for adding bussiness rules 
befor or after the apis

WARNING: you must update the function definations if 
         the zenit-config file changed

"""

from sqlalchemy.orm import Session
from datetime import datetime
from zenitdb import models,schemas,crud


#region user

## read_user -------------------------------------------------------------
def read_user(
    db: Session
    ,user
    ,page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,fields = {}
):
    #fields keys
    # fields['load_1_user_group'] = False
    # fields['query_json_user_group'] = '[]'
    # fields['load_n_group_poshtiban_group'] = False
    # fields['query_json_group_poshtiban_group'] = '[]'
    # fields['load_n_assign_user_assign'] = False
    # fields['query_json_assign_user_assign'] = '[]'
    # fields['load_n_py_user_payment'] = False
    # fields['query_json_py_user_payment'] = '[]'
    # fields['load_n_user_sms'] = False
    # fields['query_json_user_sms'] = '[]'


    # do magic with params or check user rights

    result = crud.read_user(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_user_byId -------------------------------------------------------------
def read_user_byId(db: Session, user, id:int
    ,load_group_user_group: bool = True
):

    # do magic with params or check user rights

    result = crud.read_user_byId(db, user, id
        ,load_group_user_group=load_group_user_group
    )

    # do magic with the result of operation

    return result;


## patch_user -------------------------------------------------------------
def patch_user(db: Session,user,id: int, fields):

    # fields
    # fields['user_name'] = None
    # fields['user_mobile'] = None
    # fields['user_tel'] = None
    # fields['user_country'] = None
    # fields['user_city'] = None
    # fields['user_lang'] = None
    # fields['user_group_id'] = None
    # fields['user_smshour'] = None
    # fields['user_access'] = None
    # fields['user_ack'] = None
    # fields['user_active'] = None
    # fields['user_bdate'] = None
    # fields['user_money'] = None
    # fields['user_iswomen'] = None
    # fields['user_smslevel'] = None
    # fields['user_smsfinishdate'] = None
    # fields['user_telegram_session'] = None

    # do magic with params or check user rights

    result = crud.patch_user(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_user -------------------------------------------------------------
def delete_user(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_user(db, user, id)

    # do magic with the result of operation

    return result


#endregion user


#region group

## read_group -------------------------------------------------------------
def read_group(
    db: Session
    ,user
    ,page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,fields = {}
):
    #fields keys
    # fields['load_1_group_poshtiban'] = False
    # fields['query_json_group_poshtiban'] = '[]'
    # fields['load_n_user_group_user'] = False
    # fields['query_json_user_group_user'] = '[]'


    # do magic with params or check user rights

    result = crud.read_group(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_group_byId -------------------------------------------------------------
def read_group_byId(db: Session, user, id:int
    ,load_user_group_poshtiban: bool = True
):

    # do magic with params or check user rights

    result = crud.read_group_byId(db, user, id
        ,load_user_group_poshtiban=load_user_group_poshtiban
    )

    # do magic with the result of operation

    return result;


## insert_group -------------------------------------------------------------
def insert_group (
    db: Session
    ,user
    ,the_Group: schemas.Group
):
    
    # the_Group.group_poshtiban_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_group(db, user, the_Group)

    # do magic with the result of operation

    return result


## patch_group -------------------------------------------------------------
def patch_group(db: Session,user,id: int, fields):

    # fields
    # fields['group_name'] = None
    # fields['group_poshtiban_id'] = None
    # fields['group_poshtiban_id'] = user.id # would you like?
    # fields['group_start_date'] = None
    # fields['group_start_page'] = None
    # fields['group_assign_day'] = None
    # fields['group_uc'] = None
    # fields['group_type'] = None

    # do magic with params or check user rights

    result = crud.patch_group(db, user, id, fields)

    # do magic with the result of operation

    return result


#endregion group


#region assign

## read_assign -------------------------------------------------------------
def read_assign(
    db: Session
    ,user
    ,page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,fields = {}
):
    #fields keys
    # fields['load_1_assign_user'] = False
    # fields['query_json_assign_user'] = '[]'


    # do magic with params or check user rights

    result = crud.read_assign(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_assign_byId -------------------------------------------------------------
def read_assign_byId(db: Session, user, id:int
    ,load_user_assign_user: bool = True
):

    # do magic with params or check user rights

    result = crud.read_assign_byId(db, user, id
        ,load_user_assign_user=load_user_assign_user
    )

    # do magic with the result of operation

    return result;


## insert_assign -------------------------------------------------------------
def insert_assign (
    db: Session
    ,user
    ,the_Assign: schemas.Assign
):
    
    # the_Assign.assign_user_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_assign(db, user, the_Assign)

    # do magic with the result of operation

    return result


#endregion assign


#region payment

## read_payment -------------------------------------------------------------
def read_payment(
    db: Session
    ,user
    ,page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,fields = {}
):
    #fields keys
    # fields['load_1_py_user'] = False
    # fields['query_json_py_user'] = '[]'


    # do magic with params or check user rights

    result = crud.read_payment(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_payment_byId -------------------------------------------------------------
def read_payment_byId(db: Session, user, id:int
    ,load_user_py_user: bool = True
):

    # do magic with params or check user rights

    result = crud.read_payment_byId(db, user, id
        ,load_user_py_user=load_user_py_user
    )

    # do magic with the result of operation

    return result;


#endregion payment


#region sms

## read_sms -------------------------------------------------------------
def read_sms(
    db: Session
    ,user
    ,page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,fields = {}
):
    #fields keys
    # fields['load_1_user'] = False
    # fields['query_json_user'] = '[]'


    # do magic with params or check user rights

    result = crud.read_sms(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_sms_byId -------------------------------------------------------------
def read_sms_byId(db: Session, user, id:int
    ,load_user_user: bool = True
):

    # do magic with params or check user rights

    result = crud.read_sms_byId(db, user, id
        ,load_user_user=load_user_user
    )

    # do magic with the result of operation

    return result;


#endregion sms


