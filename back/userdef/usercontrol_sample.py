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
    # fields['load_n_user_cetr_project'] = False
    # fields['query_json_user_cetr_project'] = '[]'
    # fields['load_n_user_edit_project'] = False
    # fields['query_json_user_edit_project'] = '[]'
    # fields['load_n_user_aprv_project'] = False
    # fields['query_json_user_aprv_project'] = '[]'
    # fields['load_n_user_project_users'] = False
    # fields['query_json_user_project_users'] = '[]'
    # fields['load_n_user_cetr_dttype'] = False
    # fields['query_json_user_cetr_dttype'] = '[]'
    # fields['load_n_user_edit_dttype'] = False
    # fields['query_json_user_edit_dttype'] = '[]'
    # fields['load_n_user_aprv_dttype'] = False
    # fields['query_json_user_aprv_dttype'] = '[]'
    # fields['load_n_user_cetr_dtitem'] = False
    # fields['query_json_user_cetr_dtitem'] = '[]'
    # fields['load_n_user_edit_dtitem'] = False
    # fields['query_json_user_edit_dtitem'] = '[]'
    # fields['load_n_user_aprv_dtitem'] = False
    # fields['query_json_user_aprv_dtitem'] = '[]'
    # fields['load_n_user_cetr_topic'] = False
    # fields['query_json_user_cetr_topic'] = '[]'
    # fields['load_n_user_edit_topic'] = False
    # fields['query_json_user_edit_topic'] = '[]'
    # fields['load_n_user_aprv_topic'] = False
    # fields['query_json_user_aprv_topic'] = '[]'
    # fields['load_n_user_cetr_federate'] = False
    # fields['query_json_user_cetr_federate'] = '[]'
    # fields['load_n_user_edit_federate'] = False
    # fields['query_json_user_edit_federate'] = '[]'
    # fields['load_n_user_aprv_federate'] = False
    # fields['query_json_user_aprv_federate'] = '[]'
    # fields['load_n_user_cetr_federatetopic'] = False
    # fields['query_json_user_cetr_federatetopic'] = '[]'
    # fields['load_n_user_edit_federatetopic'] = False
    # fields['query_json_user_edit_federatetopic'] = '[]'
    # fields['load_n_user_aprv_federatetopic'] = False
    # fields['query_json_user_aprv_federatetopic'] = '[]'
    # fields['load_n_user_wiki'] = False
    # fields['query_json_user_wiki'] = '[]'


    # do magic with params or check user rights

    result = crud.read_user(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_user_byId -------------------------------------------------------------
def read_user_byId(db: Session, user, id:int
):

    # do magic with params or check user rights

    result = crud.read_user_byId(db, user, id
    )

    # do magic with the result of operation

    return result;


## patch_user -------------------------------------------------------------
def patch_user(db: Session,user,id: int, fields):

    # fields
    # fields['user_name'] = None
    # fields['user_mobile'] = None
    # fields['user_tel'] = None
    # fields['user_address'] = None
    # fields['user_comment'] = None

    # do magic with params or check user rights

    result = crud.patch_user(db, user, id, fields)

    # do magic with the result of operation

    return result


#endregion user


#region project

## read_project -------------------------------------------------------------
def read_project(
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
    # fields['load_1_user_cetr'] = False
    # fields['query_json_user_cetr'] = '[]'
    # fields['load_1_user_edit'] = False
    # fields['query_json_user_edit'] = '[]'
    # fields['load_1_user_aprv'] = False
    # fields['query_json_user_aprv'] = '[]'
    # fields['load_n_project_project_users'] = False
    # fields['query_json_project_project_users'] = '[]'
    # fields['load_n_proj_dttype'] = False
    # fields['query_json_proj_dttype'] = '[]'
    # fields['load_n_proj_topic'] = False
    # fields['query_json_proj_topic'] = '[]'
    # fields['load_n_proj_federate'] = False
    # fields['query_json_proj_federate'] = '[]'
    # fields['load_n_proj_diagram'] = False
    # fields['query_json_proj_diagram'] = '[]'


    # do magic with params or check user rights

    result = crud.read_project(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_project_byId -------------------------------------------------------------
def read_project_byId(db: Session, user, id:int
    ,load_user_user_cetr: bool = True
    ,load_user_user_edit: bool = True
    ,load_user_user_aprv: bool = True
):

    # do magic with params or check user rights

    result = crud.read_project_byId(db, user, id
        ,load_user_user_cetr=load_user_user_cetr
        ,load_user_user_edit=load_user_user_edit
        ,load_user_user_aprv=load_user_user_aprv
    )

    # do magic with the result of operation

    return result;


## insert_project -------------------------------------------------------------
def insert_project (
    db: Session
    ,user
    ,the_Project: schemas.Project
):
    
    # the_Project.user_cetr_id = user.id # would you like?
    # the_Project.user_edit_id = user.id # would you like?
    # the_Project.user_aprv_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_project(db, user, the_Project)

    # do magic with the result of operation

    return result


## patch_project -------------------------------------------------------------
def patch_project(db: Session,user,id: int, fields):

    # fields
    # fields['ids'] = None
    # fields['user_cetr_id'] = None
    # fields['user_cetr_id'] = user.id # would you like?
    # fields['cetr_time'] = None
    # fields['user_edit_id'] = None
    # fields['user_edit_id'] = user.id # would you like?
    # fields['edit_time'] = None
    # fields['user_aprv_id'] = None
    # fields['user_aprv_id'] = user.id # would you like?
    # fields['aprv_time'] = None
    # fields['proj_name'] = None
    # fields['desc1'] = None
    # fields['desc2'] = None

    # do magic with params or check user rights

    result = crud.patch_project(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_project -------------------------------------------------------------
def delete_project(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_project(db, user, id)

    # do magic with the result of operation

    return result


#endregion project


#region project_users

## read_project_users -------------------------------------------------------------
def read_project_users(
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
    # fields['load_1_project'] = False
    # fields['query_json_project'] = '[]'
    # fields['load_1_user'] = False
    # fields['query_json_user'] = '[]'


    # do magic with params or check user rights

    result = crud.read_project_users(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_project_users_byId -------------------------------------------------------------
def read_project_users_byId(db: Session, user, id:int
    ,load_project_project: bool = True
    ,load_user_user: bool = True
):

    # do magic with params or check user rights

    result = crud.read_project_users_byId(db, user, id
        ,load_project_project=load_project_project
        ,load_user_user=load_user_user
    )

    # do magic with the result of operation

    return result;


## insert_project_users -------------------------------------------------------------
def insert_project_users (
    db: Session
    ,user
    ,the_Project_Users: schemas.Project_Users
):
    
    # the_Project_Users.user_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_project_users(db, user, the_Project_Users)

    # do magic with the result of operation

    return result


## delete_project_users -------------------------------------------------------------
def delete_project_users(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_project_users(db, user, id)

    # do magic with the result of operation

    return result


#endregion project_users


#region dttype

## read_dttype_byId -------------------------------------------------------------
def read_dttype_byId(db: Session, user, id:int
    ,load_user_user_cetr: bool = True
    ,load_user_user_edit: bool = True
    ,load_user_user_aprv: bool = True
    ,load_project_proj: bool = True
):

    # do magic with params or check user rights

    result = crud.read_dttype_byId(db, user, id
        ,load_user_user_cetr=load_user_user_cetr
        ,load_user_user_edit=load_user_user_edit
        ,load_user_user_aprv=load_user_user_aprv
        ,load_project_proj=load_project_proj
    )

    # do magic with the result of operation

    return result;


## insert_dttype -------------------------------------------------------------
def insert_dttype (
    db: Session
    ,user
    ,the_Dttype: schemas.Dttype
):
    
    # the_Dttype.user_cetr_id = user.id # would you like?
    # the_Dttype.user_edit_id = user.id # would you like?
    # the_Dttype.user_aprv_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_dttype(db, user, the_Dttype)

    # do magic with the result of operation

    return result


## patch_dttype -------------------------------------------------------------
def patch_dttype(db: Session,user,id: int, fields):

    # fields
    # fields['ids'] = None
    # fields['user_cetr_id'] = None
    # fields['user_cetr_id'] = user.id # would you like?
    # fields['cetr_time'] = None
    # fields['user_edit_id'] = None
    # fields['user_edit_id'] = user.id # would you like?
    # fields['edit_time'] = None
    # fields['user_aprv_id'] = None
    # fields['user_aprv_id'] = user.id # would you like?
    # fields['aprv_time'] = None
    # fields['proj_id'] = None
    # fields['dt_kind'] = None
    # fields['name'] = None
    # fields['desc1'] = None
    # fields['desc2'] = None
    # fields['modified'] = None
    # fields['ok_name'] = None
    # fields['ok_desc1'] = None
    # fields['ok_desc2'] = None

    # do magic with params or check user rights

    result = crud.patch_dttype(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_dttype -------------------------------------------------------------
def delete_dttype(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_dttype(db, user, id)

    # do magic with the result of operation

    return result


#endregion dttype


#region dtitem

## read_dtitem -------------------------------------------------------------
def read_dtitem(
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
    # fields['load_1_user_cetr'] = False
    # fields['query_json_user_cetr'] = '[]'
    # fields['load_1_user_edit'] = False
    # fields['query_json_user_edit'] = '[]'
    # fields['load_1_user_aprv'] = False
    # fields['query_json_user_aprv'] = '[]'
    # fields['load_1_di_master'] = False
    # fields['query_json_di_master'] = '[]'
    # fields['load_1_di_type'] = False
    # fields['query_json_di_type'] = '[]'
    # fields['load_1_ok_di_type'] = False
    # fields['query_json_ok_di_type'] = '[]'


    # do magic with params or check user rights

    result = crud.read_dtitem(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_dtitem_byId -------------------------------------------------------------
def read_dtitem_byId(db: Session, user, id:int
    ,load_user_user_cetr: bool = True
    ,load_user_user_edit: bool = True
    ,load_user_user_aprv: bool = True
    ,load_dttype_di_master: bool = True
    ,load_dttype_di_type: bool = True
    ,load_dttype_ok_di_type: bool = True
):

    # do magic with params or check user rights

    result = crud.read_dtitem_byId(db, user, id
        ,load_user_user_cetr=load_user_user_cetr
        ,load_user_user_edit=load_user_user_edit
        ,load_user_user_aprv=load_user_user_aprv
        ,load_dttype_di_master=load_dttype_di_master
        ,load_dttype_di_type=load_dttype_di_type
        ,load_dttype_ok_di_type=load_dttype_ok_di_type
    )

    # do magic with the result of operation

    return result;


## insert_dtitem -------------------------------------------------------------
def insert_dtitem (
    db: Session
    ,user
    ,the_Dtitem: schemas.Dtitem
):
    
    # the_Dtitem.user_cetr_id = user.id # would you like?
    # the_Dtitem.user_edit_id = user.id # would you like?
    # the_Dtitem.user_aprv_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_dtitem(db, user, the_Dtitem)

    # do magic with the result of operation

    return result


## patch_dtitem -------------------------------------------------------------
def patch_dtitem(db: Session,user,id: int, fields):

    # fields
    # fields['ids'] = None
    # fields['user_cetr_id'] = None
    # fields['user_cetr_id'] = user.id # would you like?
    # fields['cetr_time'] = None
    # fields['user_edit_id'] = None
    # fields['user_edit_id'] = user.id # would you like?
    # fields['edit_time'] = None
    # fields['user_aprv_id'] = None
    # fields['user_aprv_id'] = user.id # would you like?
    # fields['aprv_time'] = None
    # fields['di_master_id'] = None
    # fields['di_kind'] = None
    # fields['name'] = None
    # fields['di_type_id'] = None
    # fields['di_value'] = None
    # fields['desc1'] = None
    # fields['desc2'] = None
    # fields['modified'] = None
    # fields['ok_name'] = None
    # fields['ok_di_type_id'] = None
    # fields['ok_di_value'] = None
    # fields['ok_desc1'] = None
    # fields['ok_desc2'] = None

    # do magic with params or check user rights

    result = crud.patch_dtitem(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_dtitem -------------------------------------------------------------
def delete_dtitem(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_dtitem(db, user, id)

    # do magic with the result of operation

    return result


#endregion dtitem


#region topic

## read_topic -------------------------------------------------------------
def read_topic(
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
    # fields['load_1_user_cetr'] = False
    # fields['query_json_user_cetr'] = '[]'
    # fields['load_1_user_edit'] = False
    # fields['query_json_user_edit'] = '[]'
    # fields['load_1_user_aprv'] = False
    # fields['query_json_user_aprv'] = '[]'
    # fields['load_1_proj'] = False
    # fields['query_json_proj'] = '[]'
    # fields['load_1_start_dttype'] = False
    # fields['query_json_start_dttype'] = '[]'
    # fields['load_1_end_dttype'] = False
    # fields['query_json_end_dttype'] = '[]'
    # fields['load_1_ok_start_dttype'] = False
    # fields['query_json_ok_start_dttype'] = '[]'
    # fields['load_1_ok_end_dttype'] = False
    # fields['query_json_ok_end_dttype'] = '[]'
    # fields['load_n_topic_federatetopic'] = False
    # fields['query_json_topic_federatetopic'] = '[]'


    # do magic with params or check user rights

    result = crud.read_topic(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_topic_byId -------------------------------------------------------------
def read_topic_byId(db: Session, user, id:int
    ,load_user_user_cetr: bool = True
    ,load_user_user_edit: bool = True
    ,load_user_user_aprv: bool = True
    ,load_project_proj: bool = True
    ,load_dttype_start_dttype: bool = True
    ,load_dttype_end_dttype: bool = True
    ,load_dttype_ok_start_dttype: bool = True
    ,load_dttype_ok_end_dttype: bool = True
):

    # do magic with params or check user rights

    result = crud.read_topic_byId(db, user, id
        ,load_user_user_cetr=load_user_user_cetr
        ,load_user_user_edit=load_user_user_edit
        ,load_user_user_aprv=load_user_user_aprv
        ,load_project_proj=load_project_proj
        ,load_dttype_start_dttype=load_dttype_start_dttype
        ,load_dttype_end_dttype=load_dttype_end_dttype
        ,load_dttype_ok_start_dttype=load_dttype_ok_start_dttype
        ,load_dttype_ok_end_dttype=load_dttype_ok_end_dttype
    )

    # do magic with the result of operation

    return result;


## insert_topic -------------------------------------------------------------
def insert_topic (
    db: Session
    ,user
    ,the_Topic: schemas.Topic
):
    
    # the_Topic.user_cetr_id = user.id # would you like?
    # the_Topic.user_edit_id = user.id # would you like?
    # the_Topic.user_aprv_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_topic(db, user, the_Topic)

    # do magic with the result of operation

    return result


## patch_topic -------------------------------------------------------------
def patch_topic(db: Session,user,id: int, fields):

    # fields
    # fields['ids'] = None
    # fields['user_cetr_id'] = None
    # fields['user_cetr_id'] = user.id # would you like?
    # fields['cetr_time'] = None
    # fields['user_edit_id'] = None
    # fields['user_edit_id'] = user.id # would you like?
    # fields['edit_time'] = None
    # fields['user_aprv_id'] = None
    # fields['user_aprv_id'] = user.id # would you like?
    # fields['aprv_time'] = None
    # fields['proj_id'] = None
    # fields['start_dttype_id'] = None
    # fields['end_dttype_id'] = None
    # fields['name'] = None
    # fields['desc1'] = None
    # fields['desc2'] = None
    # fields['modified'] = None
    # fields['graph'] = None
    # fields['ok_start_dttype_id'] = None
    # fields['ok_end_dttype_id'] = None
    # fields['ok_name'] = None
    # fields['ok_desc1'] = None
    # fields['ok_desc2'] = None
    # fields['ok_graph'] = None

    # do magic with params or check user rights

    result = crud.patch_topic(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_topic -------------------------------------------------------------
def delete_topic(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_topic(db, user, id)

    # do magic with the result of operation

    return result


#endregion topic


#region federate

## read_federate -------------------------------------------------------------
def read_federate(
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
    # fields['load_1_user_cetr'] = False
    # fields['query_json_user_cetr'] = '[]'
    # fields['load_1_user_edit'] = False
    # fields['query_json_user_edit'] = '[]'
    # fields['load_1_user_aprv'] = False
    # fields['query_json_user_aprv'] = '[]'
    # fields['load_1_proj'] = False
    # fields['query_json_proj'] = '[]'
    # fields['load_n_federate_federatetopic'] = False
    # fields['query_json_federate_federatetopic'] = '[]'


    # do magic with params or check user rights

    result = crud.read_federate(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_federate_byId -------------------------------------------------------------
def read_federate_byId(db: Session, user, id:int
    ,load_user_user_cetr: bool = True
    ,load_user_user_edit: bool = True
    ,load_user_user_aprv: bool = True
    ,load_project_proj: bool = True
):

    # do magic with params or check user rights

    result = crud.read_federate_byId(db, user, id
        ,load_user_user_cetr=load_user_user_cetr
        ,load_user_user_edit=load_user_user_edit
        ,load_user_user_aprv=load_user_user_aprv
        ,load_project_proj=load_project_proj
    )

    # do magic with the result of operation

    return result;


## insert_federate -------------------------------------------------------------
def insert_federate (
    db: Session
    ,user
    ,the_Federate: schemas.Federate
):
    
    # the_Federate.user_cetr_id = user.id # would you like?
    # the_Federate.user_edit_id = user.id # would you like?
    # the_Federate.user_aprv_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_federate(db, user, the_Federate)

    # do magic with the result of operation

    return result


## patch_federate -------------------------------------------------------------
def patch_federate(db: Session,user,id: int, fields):

    # fields
    # fields['ids'] = None
    # fields['user_cetr_id'] = None
    # fields['user_cetr_id'] = user.id # would you like?
    # fields['cetr_time'] = None
    # fields['user_edit_id'] = None
    # fields['user_edit_id'] = user.id # would you like?
    # fields['edit_time'] = None
    # fields['user_aprv_id'] = None
    # fields['user_aprv_id'] = user.id # would you like?
    # fields['aprv_time'] = None
    # fields['proj_id'] = None
    # fields['name'] = None
    # fields['desc1'] = None
    # fields['desc2'] = None
    # fields['modified'] = None
    # fields['ok_name'] = None
    # fields['ok_desc1'] = None
    # fields['ok_desc2'] = None
    # fields['login'] = None
    # fields['passw'] = None
    # fields['token'] = None
    # fields['ip'] = None
    # fields['mac'] = None
    # fields['host'] = None
    # fields['port'] = None
    # fields['connectionType'] = None
    # fields['liveness'] = None

    # do magic with params or check user rights

    result = crud.patch_federate(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_federate -------------------------------------------------------------
def delete_federate(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_federate(db, user, id)

    # do magic with the result of operation

    return result


#endregion federate


#region federatetopic

## read_federatetopic -------------------------------------------------------------
def read_federatetopic(
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
    # fields['load_1_user_cetr'] = False
    # fields['query_json_user_cetr'] = '[]'
    # fields['load_1_user_edit'] = False
    # fields['query_json_user_edit'] = '[]'
    # fields['load_1_user_aprv'] = False
    # fields['query_json_user_aprv'] = '[]'
    # fields['load_1_federate'] = False
    # fields['query_json_federate'] = '[]'
    # fields['load_1_topic'] = False
    # fields['query_json_topic'] = '[]'


    # do magic with params or check user rights

    result = crud.read_federatetopic(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_federatetopic_byId -------------------------------------------------------------
def read_federatetopic_byId(db: Session, user, id:int
    ,load_user_user_cetr: bool = True
    ,load_user_user_edit: bool = True
    ,load_user_user_aprv: bool = True
    ,load_federate_federate: bool = True
    ,load_topic_topic: bool = True
):

    # do magic with params or check user rights

    result = crud.read_federatetopic_byId(db, user, id
        ,load_user_user_cetr=load_user_user_cetr
        ,load_user_user_edit=load_user_user_edit
        ,load_user_user_aprv=load_user_user_aprv
        ,load_federate_federate=load_federate_federate
        ,load_topic_topic=load_topic_topic
    )

    # do magic with the result of operation

    return result;


## insert_federatetopic -------------------------------------------------------------
def insert_federatetopic (
    db: Session
    ,user
    ,the_Federatetopic: schemas.Federatetopic
):
    
    # the_Federatetopic.user_cetr_id = user.id # would you like?
    # the_Federatetopic.user_edit_id = user.id # would you like?
    # the_Federatetopic.user_aprv_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_federatetopic(db, user, the_Federatetopic)

    # do magic with the result of operation

    return result


## patch_federatetopic -------------------------------------------------------------
def patch_federatetopic(db: Session,user,id: int, fields):

    # fields
    # fields['ids'] = None
    # fields['user_cetr_id'] = None
    # fields['user_cetr_id'] = user.id # would you like?
    # fields['cetr_time'] = None
    # fields['user_edit_id'] = None
    # fields['user_edit_id'] = user.id # would you like?
    # fields['edit_time'] = None
    # fields['user_aprv_id'] = None
    # fields['user_aprv_id'] = user.id # would you like?
    # fields['aprv_time'] = None
    # fields['federate_id'] = None
    # fields['topic_id'] = None
    # fields['dir'] = None
    # fields['desc1'] = None
    # fields['desc2'] = None

    # do magic with params or check user rights

    result = crud.patch_federatetopic(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_federatetopic -------------------------------------------------------------
def delete_federatetopic(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_federatetopic(db, user, id)

    # do magic with the result of operation

    return result


#endregion federatetopic


#region diagram

## read_diagram -------------------------------------------------------------
def read_diagram(
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
    # fields['load_1_proj'] = False
    # fields['query_json_proj'] = '[]'


    # do magic with params or check user rights

    result = crud.read_diagram(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_diagram_byId -------------------------------------------------------------
def read_diagram_byId(db: Session, user, id:int
    ,load_project_proj: bool = True
):

    # do magic with params or check user rights

    result = crud.read_diagram_byId(db, user, id
        ,load_project_proj=load_project_proj
    )

    # do magic with the result of operation

    return result;


## insert_diagram -------------------------------------------------------------
def insert_diagram (
    db: Session
    ,user
    ,the_Diagram: schemas.Diagram
):
    

    # do magic with params or check user rights

    result = crud.insert_diagram(db, user, the_Diagram)

    # do magic with the result of operation

    return result


## patch_diagram -------------------------------------------------------------
def patch_diagram(db: Session,user,id: int, fields):

    # fields
    # fields['name'] = None
    # fields['proj_id'] = None
    # fields['Content'] = None

    # do magic with params or check user rights

    result = crud.patch_diagram(db, user, id, fields)

    # do magic with the result of operation

    return result


## delete_diagram -------------------------------------------------------------
def delete_diagram(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_diagram(db, user, id)

    # do magic with the result of operation

    return result


#endregion diagram


#region wiki

## read_wiki -------------------------------------------------------------
def read_wiki(
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
    # fields['load_n_wiki_wiki_tags'] = False
    # fields['query_json_wiki_wiki_tags'] = '[]'


    # do magic with params or check user rights

    result = crud.read_wiki(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_wiki_byId -------------------------------------------------------------
def read_wiki_byId(db: Session, user, id:int
    ,load_user_user: bool = True
):

    # do magic with params or check user rights

    result = crud.read_wiki_byId(db, user, id
        ,load_user_user=load_user_user
    )

    # do magic with the result of operation

    return result;


## insert_wiki -------------------------------------------------------------
def insert_wiki (
    db: Session
    ,user
    ,the_Wiki: schemas.Wiki
):
    
    # the_Wiki.user_id = user.id # would you like?

    # do magic with params or check user rights

    result = crud.insert_wiki(db, user, the_Wiki)

    # do magic with the result of operation

    return result


## patch_wiki -------------------------------------------------------------
def patch_wiki(db: Session,user,id: int, fields):

    # fields
    # fields['moment'] = None
    # fields['user_id'] = None
    # fields['user_id'] = user.id # would you like?
    # fields['content'] = None

    # do magic with params or check user rights

    result = crud.patch_wiki(db, user, id, fields)

    # do magic with the result of operation

    return result


#endregion wiki


#region wiki_tags

## read_wiki_tags -------------------------------------------------------------
def read_wiki_tags(
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
    # fields['load_1_wiki'] = False
    # fields['query_json_wiki'] = '[]'


    # do magic with params or check user rights

    result = crud.read_wiki_tags(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    # do magic with the result of operation

    return result


## read_wiki_tags_byId -------------------------------------------------------------
def read_wiki_tags_byId(db: Session, user, id:int
    ,load_wiki_wiki: bool = True
):

    # do magic with params or check user rights

    result = crud.read_wiki_tags_byId(db, user, id
        ,load_wiki_wiki=load_wiki_wiki
    )

    # do magic with the result of operation

    return result;


## insert_wiki_tags -------------------------------------------------------------
def insert_wiki_tags (
    db: Session
    ,user
    ,the_Wiki_Tags: schemas.Wiki_Tags
):
    

    # do magic with params or check user rights

    result = crud.insert_wiki_tags(db, user, the_Wiki_Tags)

    # do magic with the result of operation

    return result


## delete_wiki_tags -------------------------------------------------------------
def delete_wiki_tags(db: Session,user,id: int):

    # do magic with params or check user rights

    result = crud.delete_wiki_tags(db, user, id)

    # do magic with the result of operation

    return result


#endregion wiki_tags


