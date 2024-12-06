from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Body
from zenitdb.app import app
from userdef.user_login import get_current_user
import zenitdb.schemas as schemas
import zenitdb.crud as crud
from sqlalchemy.orm import Session
from sqlalchemy import text
from zenitdb.database import get_db
from userdef import usercontrol
from datetime import datetime, timedelta
from zenitdb.schemas import ZDate
import json

usercontrol_defs = dir(usercontrol)

@app.get('/options/{option_name}', tags=["Options"])
def Read_Options(option_name: str
                ,user: dict = Depends(get_current_user)
                ,db: Session = Depends(get_db)):
    zdb = db.scalars(text("SELECT `zs_vl` FROM `zenitSetting` " +  
                          "WHERE `zs_id` = :opn AND " +
                          " (user_id = :u OR user_id = 0) ORDER BY user_id desc ;"), 
                          { 'opn': option_name, 'u': user.id }).first()
    return zdb

@app.post('/options/{option_name}', tags=["Options"])
def Save_Options(option_name: str
                ,value: Annotated[str, Body(embed=False)]
                ,forallusers: bool = False
                ,user: dict = Depends(get_current_user)
                ,db: Session = Depends(get_db)):
    
    db.execute(text("DELETE FROM `zenitSetting` WHERE `zs_id` = :opn AND user_id = :u;"), 
            { 'opn': option_name, 'u': 0 if forallusers else user.id })
    db.execute(text("INSERT INTO `zenitSetting` (`zs_id`, `zs_vl`, `user_id`) " + 
                    "VALUES (:opn, :opv, :u);"), { 'opn': option_name, 'opv': value, 'u': 0 if forallusers else user.id })
    db.commit()
    return


#region user

## User #####################################################################
## Read_User  ----------------------------------------------------------------
@app.get("/user/read", tags=["User"],
summary="read the User with search & pagination"
)
def Read_User(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user_group: bool = False
    ,query_json_user_group: str = '[]'
    ,load_n_group_poshtiban_group: bool = False
    ,params_group_poshtiban_group: str = '{}'
    ,query_json_group_poshtiban_group: str = '[]'
    ,load_n_assign_user_assign: bool = False
    ,params_assign_user_assign: str = '{}'
    ,query_json_assign_user_assign: str = '[]'
    ,load_n_py_user_payment: bool = False
    ,params_py_user_payment: str = '{}'
    ,query_json_py_user_payment: str = '[]'
    ,load_n_user_sms: bool = False
    ,params_user_sms: str = '{}'
    ,query_json_user_sms: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_user_group**: load one item from Group
    - **query_json_user_group**: json array to filter the Group object that 
            user_group_id object should pass
    - **load_n_group_poshtiban_group**: load many group items that have relation with User
    - **params_group_poshtiban_group**: parameters of this load See route group/read - assign it with JSON.stringify(...)
    - **query_json_group_poshtiban_group**: json array filter that many items of group should pass
    - **load_n_assign_user_assign**: load many assign items that have relation with User
    - **params_assign_user_assign**: parameters of this load See route assign/read - assign it with JSON.stringify(...)
    - **query_json_assign_user_assign**: json array filter that many items of assign should pass
    - **load_n_py_user_payment**: load many payment items that have relation with User
    - **params_py_user_payment**: parameters of this load See route payment/read - assign it with JSON.stringify(...)
    - **query_json_py_user_payment**: json array filter that many items of payment should pass
    - **load_n_user_sms**: load many sms items that have relation with User
    - **params_user_sms**: parameters of this load See route sms/read - assign it with JSON.stringify(...)
    - **query_json_user_sms**: json array filter that many items of sms should pass
    """
    result = None

    fields = {
        'load_1_user_group': load_1_user_group,
        'query_json_user_group': query_json_user_group,
        'load_n_group_poshtiban_group':load_n_group_poshtiban_group,
        'params_group_poshtiban_group':json.loads(params_group_poshtiban_group),
        'query_json_group_poshtiban_group':query_json_group_poshtiban_group,
        'load_n_assign_user_assign':load_n_assign_user_assign,
        'params_assign_user_assign':json.loads(params_assign_user_assign),
        'query_json_assign_user_assign':query_json_assign_user_assign,
        'load_n_py_user_payment':load_n_py_user_payment,
        'params_py_user_payment':json.loads(params_py_user_payment),
        'query_json_py_user_payment':query_json_py_user_payment,
        'load_n_user_sms':load_n_user_sms,
        'params_user_sms':json.loads(params_user_sms),
        'query_json_user_sms':query_json_user_sms,
    }


    
    if('read_user' in usercontrol_defs):
        read_user = getattr(usercontrol, 'read_user')
        result = read_user(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_user(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_User_byId  ---------------------------------------------------------------
@app.get("/user/{id}", tags=["User"])
def Read_User_byId(
    id: int
    ,load_group_user_group: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_user_byId' in usercontrol_defs):
        read_user_byId = getattr(usercontrol, 'read_user_byId')

        result = read_user_byId(db, user, id
            ,load_group_user_group=load_group_user_group
        )
    else:
        result = crud.read_user_byId(db, user, id
            ,load_group_user_group=load_group_user_group
        )

    return result;


## Patch_User --------------------------------------------------------------------
@app.patch("/user/{id}", tags=["User"])
def Patch_User(
    id: int
    ,the_User: schemas.User_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'user_name': the_User.user_name
        ,'user_mobile': the_User.user_mobile
        ,'user_tel': the_User.user_tel
        ,'user_country': the_User.user_country
        ,'user_city': the_User.user_city
        ,'user_lang': the_User.user_lang
        ,'user_group_id': the_User.user_group_id
        ,'user_smshour': the_User.user_smshour
        ,'user_access': the_User.user_access
        ,'user_ack': the_User.user_ack
        ,'user_active': the_User.user_active
        ,'user_bdate': the_User.user_bdate
        ,'user_money': the_User.user_money
        ,'user_iswomen': the_User.user_iswomen
        ,'user_smslevel': the_User.user_smslevel
        ,'user_smsfinishdate': the_User.user_smsfinishdate
        ,'user_telegram_session': the_User.user_telegram_session
    }

    if('patch_user' in usercontrol_defs):
        patch_user = getattr(usercontrol, 'patch_user')

        result = patch_user(db, user, id, fields=p)
    else:
        result = crud.patch_user(db, user, id, fields=p)

    db.commit()
    return result


## Delete_User  ------------------------------------------------------------------
@app.delete("/user/{id}", tags=["User"])
def Delete_User(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_user' in usercontrol_defs):
        delete_user = getattr(usercontrol, 'delete_user')

        result = delete_user(db, user, id)
    else:
        result = crud.delete_user(db, user, id)

    db.commit()
    return result



#endregion user


#region group

## Group #####################################################################
## Read_Group  ----------------------------------------------------------------
@app.get("/group/read", tags=["Group"],
summary="read the Group with search & pagination"
)
def Read_Group(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_group_poshtiban: bool = False
    ,query_json_group_poshtiban: str = '[]'
    ,load_n_user_group_user: bool = False
    ,params_user_group_user: str = '{}'
    ,query_json_user_group_user: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_group_poshtiban**: load one item from User
    - **query_json_group_poshtiban**: json array to filter the User object that 
            group_poshtiban_id object should pass
    - **load_n_user_group_user**: load many user items that have relation with Group
    - **params_user_group_user**: parameters of this load See route user/read - assign it with JSON.stringify(...)
    - **query_json_user_group_user**: json array filter that many items of user should pass
    """
    result = None

    fields = {
        'load_1_group_poshtiban': load_1_group_poshtiban,
        'query_json_group_poshtiban': query_json_group_poshtiban,
        'load_n_user_group_user':load_n_user_group_user,
        'params_user_group_user':json.loads(params_user_group_user),
        'query_json_user_group_user':query_json_user_group_user,
    }


    
    if('read_group' in usercontrol_defs):
        read_group = getattr(usercontrol, 'read_group')
        result = read_group(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_group(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Group_byId  ---------------------------------------------------------------
@app.get("/group/{id}", tags=["Group"])
def Read_Group_byId(
    id: int
    ,load_user_group_poshtiban: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_group_byId' in usercontrol_defs):
        read_group_byId = getattr(usercontrol, 'read_group_byId')

        result = read_group_byId(db, user, id
            ,load_user_group_poshtiban=load_user_group_poshtiban
        )
    else:
        result = crud.read_group_byId(db, user, id
            ,load_user_group_poshtiban=load_user_group_poshtiban
        )

    return result;


## Insert_Group  --------------------------------------------------------------
@app.post("/group", tags=["Group"])
def Insert_Group(
    the_Group: schemas.Group_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Group2 = schemas.Group(
        # Other fields use default values
        group_name = the_Group.group_name,
        group_poshtiban_id = the_Group.group_poshtiban_id,
        group_start_date = the_Group.group_start_date,
        group_start_page = the_Group.group_start_page,
        group_assign_day = the_Group.group_assign_day,
        group_uc = the_Group.group_uc,
        group_type = the_Group.group_type,
    )

    if('insert_group' in usercontrol_defs):
        insert_group = getattr(usercontrol, 'insert_group')
        result = insert_group(db, user, the_Group2)
    else:
        result = crud.insert_group(db, user, the_Group2)

    db.commit()
    return result


## Patch_Group --------------------------------------------------------------------
@app.patch("/group/{id}", tags=["Group"])
def Patch_Group(
    id: int
    ,the_Group: schemas.Group_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'group_name': the_Group.group_name
        ,'group_poshtiban_id': the_Group.group_poshtiban_id
        ,'group_start_date': the_Group.group_start_date
        ,'group_start_page': the_Group.group_start_page
        ,'group_assign_day': the_Group.group_assign_day
        ,'group_uc': the_Group.group_uc
        ,'group_type': the_Group.group_type
    }

    if('patch_group' in usercontrol_defs):
        patch_group = getattr(usercontrol, 'patch_group')

        result = patch_group(db, user, id, fields=p)
    else:
        result = crud.patch_group(db, user, id, fields=p)

    db.commit()
    return result



#endregion group


#region assign

## Assign #####################################################################
## Read_Assign  ----------------------------------------------------------------
@app.get("/assign/read", tags=["Assign"],
summary="read the Assign with search & pagination"
)
def Read_Assign(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_assign_user: bool = False
    ,query_json_assign_user: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_assign_user**: load one item from User
    - **query_json_assign_user**: json array to filter the User object that 
            assign_user_id object should pass
    """
    result = None

    fields = {
        'load_1_assign_user': load_1_assign_user,
        'query_json_assign_user': query_json_assign_user,
    }


    
    if('read_assign' in usercontrol_defs):
        read_assign = getattr(usercontrol, 'read_assign')
        result = read_assign(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_assign(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Assign_byId  ---------------------------------------------------------------
@app.get("/assign/{id}", tags=["Assign"])
def Read_Assign_byId(
    id: int
    ,load_user_assign_user: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_assign_byId' in usercontrol_defs):
        read_assign_byId = getattr(usercontrol, 'read_assign_byId')

        result = read_assign_byId(db, user, id
            ,load_user_assign_user=load_user_assign_user
        )
    else:
        result = crud.read_assign_byId(db, user, id
            ,load_user_assign_user=load_user_assign_user
        )

    return result;


## Insert_Assign  --------------------------------------------------------------
@app.post("/assign", tags=["Assign"])
def Insert_Assign(
    the_Assign: schemas.Assign_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Assign2 = schemas.Assign(
        # Other fields use default values
        assign_user_id = the_Assign.assign_user_id,
        assign_moment = the_Assign.assign_moment,
        assign_pagenumber = the_Assign.assign_pagenumber,
        assign_status = the_Assign.assign_status,
        assign_done_moment = the_Assign.assign_done_moment,
        assign_follow_result = the_Assign.assign_follow_result,
    )

    if('insert_assign' in usercontrol_defs):
        insert_assign = getattr(usercontrol, 'insert_assign')
        result = insert_assign(db, user, the_Assign2)
    else:
        result = crud.insert_assign(db, user, the_Assign2)

    db.commit()
    return result



#endregion assign


#region payment

## Payment #####################################################################
## Read_Payment  ----------------------------------------------------------------
@app.get("/payment/read", tags=["Payment"],
summary="read the Payment with search & pagination"
)
def Read_Payment(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_py_user: bool = False
    ,query_json_py_user: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_py_user**: load one item from User
    - **query_json_py_user**: json array to filter the User object that 
            py_user_id object should pass
    """
    result = None

    fields = {
        'load_1_py_user': load_1_py_user,
        'query_json_py_user': query_json_py_user,
    }


    
    if('read_payment' in usercontrol_defs):
        read_payment = getattr(usercontrol, 'read_payment')
        result = read_payment(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_payment(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Payment_byId  ---------------------------------------------------------------
@app.get("/payment/{id}", tags=["Payment"])
def Read_Payment_byId(
    id: int
    ,load_user_py_user: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_payment_byId' in usercontrol_defs):
        read_payment_byId = getattr(usercontrol, 'read_payment_byId')

        result = read_payment_byId(db, user, id
            ,load_user_py_user=load_user_py_user
        )
    else:
        result = crud.read_payment_byId(db, user, id
            ,load_user_py_user=load_user_py_user
        )

    return result;



#endregion payment


#region sms

## Sms #####################################################################
## Read_Sms  ----------------------------------------------------------------
@app.get("/sms/read", tags=["Sms"],
summary="read the Sms with search & pagination"
)
def Read_Sms(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user: bool = False
    ,query_json_user: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_user**: load one item from User
    - **query_json_user**: json array to filter the User object that 
            user_id object should pass
    """
    result = None

    fields = {
        'load_1_user': load_1_user,
        'query_json_user': query_json_user,
    }


    
    if('read_sms' in usercontrol_defs):
        read_sms = getattr(usercontrol, 'read_sms')
        result = read_sms(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_sms(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Sms_byId  ---------------------------------------------------------------
@app.get("/sms/{id}", tags=["Sms"])
def Read_Sms_byId(
    id: int
    ,load_user_user: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_sms_byId' in usercontrol_defs):
        read_sms_byId = getattr(usercontrol, 'read_sms_byId')

        result = read_sms_byId(db, user, id
            ,load_user_user=load_user_user
        )
    else:
        result = crud.read_sms_byId(db, user, id
            ,load_user_user=load_user_user
        )

    return result;



#endregion sms


