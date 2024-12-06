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
    ,load_n_user_project_users: bool = False
    ,params_user_project_users: str = '{}'
    ,query_json_user_project_users: str = '[]'
    ,load_n_user_wiki: bool = False
    ,params_user_wiki: str = '{}'
    ,query_json_user_wiki: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_n_user_project_users**: load many project_users items that have relation with User
    - **params_user_project_users**: parameters of this load See route project_users/read - assign it with JSON.stringify(...)
    - **query_json_user_project_users**: json array filter that many items of project_users should pass
    - **load_n_user_wiki**: load many wiki items that have relation with User
    - **params_user_wiki**: parameters of this load See route wiki/read - assign it with JSON.stringify(...)
    - **query_json_user_wiki**: json array filter that many items of wiki should pass
    """
    result = None

    fields = {
        'load_n_user_project_users':load_n_user_project_users,
        'params_user_project_users':json.loads(params_user_project_users),
        'query_json_user_project_users':query_json_user_project_users,
        'load_n_user_wiki':load_n_user_wiki,
        'params_user_wiki':json.loads(params_user_wiki),
        'query_json_user_wiki':query_json_user_wiki,
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
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_user_byId' in usercontrol_defs):
        read_user_byId = getattr(usercontrol, 'read_user_byId')

        result = read_user_byId(db, user, id
        )
    else:
        result = crud.read_user_byId(db, user, id
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
        ,'user_address': the_User.user_address
        ,'user_comment': the_User.user_comment
    }

    if('patch_user' in usercontrol_defs):
        patch_user = getattr(usercontrol, 'patch_user')

        result = patch_user(db, user, id, fields=p)
    else:
        result = crud.patch_user(db, user, id, fields=p)

    db.commit()
    return result



#endregion user


#region project

## Project #####################################################################
## Read_Project  ----------------------------------------------------------------
@app.get("/project/read", tags=["Project"],
summary="read the Project with search & pagination"
)
def Read_Project(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user_cetr: bool = False
    ,query_json_user_cetr: str = '[]'
    ,load_1_user_edit: bool = False
    ,query_json_user_edit: str = '[]'
    ,load_1_user_aprv: bool = False
    ,query_json_user_aprv: str = '[]'
    ,load_n_project_project_users: bool = False
    ,params_project_project_users: str = '{}'
    ,query_json_project_project_users: str = '[]'
    ,load_n_proj_diagram: bool = False
    ,params_proj_diagram: str = '{}'
    ,query_json_proj_diagram: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_user_cetr**: load one item from User
    - **query_json_user_cetr**: json array to filter the User object that 
            user_cetr_id object should pass
    - **load_1_user_edit**: load one item from User
    - **query_json_user_edit**: json array to filter the User object that 
            user_edit_id object should pass
    - **load_1_user_aprv**: load one item from User
    - **query_json_user_aprv**: json array to filter the User object that 
            user_aprv_id object should pass
    - **load_n_project_project_users**: load many project_users items that have relation with Project
    - **params_project_project_users**: parameters of this load See route project_users/read - assign it with JSON.stringify(...)
    - **query_json_project_project_users**: json array filter that many items of project_users should pass
    - **load_n_proj_diagram**: load many diagram items that have relation with Project
    - **params_proj_diagram**: parameters of this load See route diagram/read - assign it with JSON.stringify(...)
    - **query_json_proj_diagram**: json array filter that many items of diagram should pass
    """
    result = None

    fields = {
        'load_1_user_cetr': load_1_user_cetr,
        'query_json_user_cetr': query_json_user_cetr,
        'load_1_user_edit': load_1_user_edit,
        'query_json_user_edit': query_json_user_edit,
        'load_1_user_aprv': load_1_user_aprv,
        'query_json_user_aprv': query_json_user_aprv,
        'load_n_project_project_users':load_n_project_project_users,
        'params_project_project_users':json.loads(params_project_project_users),
        'query_json_project_project_users':query_json_project_project_users,
        'load_n_proj_diagram':load_n_proj_diagram,
        'params_proj_diagram':json.loads(params_proj_diagram),
        'query_json_proj_diagram':query_json_proj_diagram,
    }


    
    if('read_project' in usercontrol_defs):
        read_project = getattr(usercontrol, 'read_project')
        result = read_project(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_project(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Project_byId  ---------------------------------------------------------------
@app.get("/project/{id}", tags=["Project"])
def Read_Project_byId(
    id: int
    ,load_user_user_cetr: bool = False
    ,load_user_user_edit: bool = False
    ,load_user_user_aprv: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_project_byId' in usercontrol_defs):
        read_project_byId = getattr(usercontrol, 'read_project_byId')

        result = read_project_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
        )
    else:
        result = crud.read_project_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
        )

    return result;


## Insert_Project  --------------------------------------------------------------
@app.post("/project", tags=["Project"])
def Insert_Project(
    the_Project: schemas.Project_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Project2 = schemas.Project(
        # Other fields use default values
        proj_name = the_Project.proj_name,
        desc1 = the_Project.desc1,
        desc2 = the_Project.desc2,
    )

    if('insert_project' in usercontrol_defs):
        insert_project = getattr(usercontrol, 'insert_project')
        result = insert_project(db, user, the_Project2)
    else:
        result = crud.insert_project(db, user, the_Project2)

    db.commit()
    return result


## Patch_Project --------------------------------------------------------------------
@app.patch("/project/{id}", tags=["Project"])
def Patch_Project(
    id: int
    ,the_Project: schemas.Project_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'proj_name': the_Project.proj_name
        ,'desc1': the_Project.desc1
        ,'desc2': the_Project.desc2
    }

    if('patch_project' in usercontrol_defs):
        patch_project = getattr(usercontrol, 'patch_project')

        result = patch_project(db, user, id, fields=p)
    else:
        result = crud.patch_project(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Project  ------------------------------------------------------------------
@app.delete("/project/{id}", tags=["Project"])
def Delete_Project(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_project' in usercontrol_defs):
        delete_project = getattr(usercontrol, 'delete_project')

        result = delete_project(db, user, id)
    else:
        result = crud.delete_project(db, user, id)

    db.commit()
    return result


## history_Project  -----------------------------------------------------------------------
@app.get("/project/history/{id}", tags=["Project"])
def history_Project(id: int
    ,page: int = 1
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    return crud.read_history_project(db, user, id, page)

#endregion project


#region project_users

## Project_Users #####################################################################
## Read_Project_Users  ----------------------------------------------------------------
@app.get("/project_users/read", tags=["Project_Users"],
summary="read the Project_Users with search & pagination"
)
def Read_Project_Users(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_project: bool = False
    ,query_json_project: str = '[]'
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
    - **load_1_project**: load one item from Project
    - **query_json_project**: json array to filter the Project object that 
            project_id object should pass
    - **load_1_user**: load one item from User
    - **query_json_user**: json array to filter the User object that 
            user_id object should pass
    """
    result = None

    fields = {
        'load_1_project': load_1_project,
        'query_json_project': query_json_project,
        'load_1_user': load_1_user,
        'query_json_user': query_json_user,
    }


    
    if('read_project_users' in usercontrol_defs):
        read_project_users = getattr(usercontrol, 'read_project_users')
        result = read_project_users(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_project_users(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Project_Users_byId  ---------------------------------------------------------------
@app.get("/project_users/{id}", tags=["Project_Users"])
def Read_Project_Users_byId(
    id: int
    ,load_project_project: bool = False
    ,load_user_user: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_project_users_byId' in usercontrol_defs):
        read_project_users_byId = getattr(usercontrol, 'read_project_users_byId')

        result = read_project_users_byId(db, user, id
            ,load_project_project=load_project_project
            ,load_user_user=load_user_user
        )
    else:
        result = crud.read_project_users_byId(db, user, id
            ,load_project_project=load_project_project
            ,load_user_user=load_user_user
        )

    return result;


## Insert_Project_Users  --------------------------------------------------------------
@app.post("/project_users", tags=["Project_Users"])
def Insert_Project_Users(
    the_Project_Users: schemas.Project_Users_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Project_Users2 = schemas.Project_Users(
        # Other fields use default values
        project_id = the_Project_Users.project_id,
        user_id = the_Project_Users.user_id,
        access = the_Project_Users.access,
    )

    if('insert_project_users' in usercontrol_defs):
        insert_project_users = getattr(usercontrol, 'insert_project_users')
        result = insert_project_users(db, user, the_Project_Users2)
    else:
        result = crud.insert_project_users(db, user, the_Project_Users2)

    db.commit()
    return result


## Delete_Project_Users  ------------------------------------------------------------------
@app.delete("/project_users/{id}", tags=["Project_Users"])
def Delete_Project_Users(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_project_users' in usercontrol_defs):
        delete_project_users = getattr(usercontrol, 'delete_project_users')

        result = delete_project_users(db, user, id)
    else:
        result = crud.delete_project_users(db, user, id)

    db.commit()
    return result



#endregion project_users


#region dttype

## Dttype #####################################################################
## Read_Dttype_byId  ---------------------------------------------------------------
@app.get("/dttype/{id}", tags=["Dttype"])
def Read_Dttype_byId(
    id: int
    ,load_user_user_cetr: bool = False
    ,load_user_user_edit: bool = False
    ,load_user_user_aprv: bool = False
    ,load_project_proj: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_dttype_byId' in usercontrol_defs):
        read_dttype_byId = getattr(usercontrol, 'read_dttype_byId')

        result = read_dttype_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_project_proj=load_project_proj
        )
    else:
        result = crud.read_dttype_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_project_proj=load_project_proj
        )

    return result;


## Insert_Dttype  --------------------------------------------------------------
@app.post("/dttype", tags=["Dttype"])
def Insert_Dttype(
    the_Dttype: schemas.Dttype_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Dttype2 = schemas.Dttype(
        # Other fields use default values
        proj_id = the_Dttype.proj_id,
        dt_kind = the_Dttype.dt_kind,
        name = the_Dttype.name,
        desc1 = the_Dttype.desc1,
        desc2 = the_Dttype.desc2,
    )

    if('insert_dttype' in usercontrol_defs):
        insert_dttype = getattr(usercontrol, 'insert_dttype')
        result = insert_dttype(db, user, the_Dttype2)
    else:
        result = crud.insert_dttype(db, user, the_Dttype2)

    db.commit()
    return result


## Patch_Dttype --------------------------------------------------------------------
@app.patch("/dttype/{id}", tags=["Dttype"])
def Patch_Dttype(
    id: int
    ,the_Dttype: schemas.Dttype_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'name': the_Dttype.name
        ,'desc1': the_Dttype.desc1
        ,'desc2': the_Dttype.desc2
    }

    if('patch_dttype' in usercontrol_defs):
        patch_dttype = getattr(usercontrol, 'patch_dttype')

        result = patch_dttype(db, user, id, fields=p)
    else:
        result = crud.patch_dttype(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Dttype  ------------------------------------------------------------------
@app.delete("/dttype/{id}", tags=["Dttype"])
def Delete_Dttype(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_dttype' in usercontrol_defs):
        delete_dttype = getattr(usercontrol, 'delete_dttype')

        result = delete_dttype(db, user, id)
    else:
        result = crud.delete_dttype(db, user, id)

    db.commit()
    return result


## history_Dttype  -----------------------------------------------------------------------
@app.get("/dttype/history/{id}", tags=["Dttype"])
def history_Dttype(id: int
    ,page: int = 1
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    return crud.read_history_dttype(db, user, id, page)

#endregion dttype


#region dtitem

## Dtitem #####################################################################
## Read_Dtitem  ----------------------------------------------------------------
@app.get("/dtitem/read", tags=["Dtitem"],
summary="read the Dtitem with search & pagination"
)
def Read_Dtitem(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user_cetr: bool = False
    ,query_json_user_cetr: str = '[]'
    ,load_1_user_edit: bool = False
    ,query_json_user_edit: str = '[]'
    ,load_1_user_aprv: bool = False
    ,query_json_user_aprv: str = '[]'
    ,load_1_di_master: bool = False
    ,query_json_di_master: str = '[]'
    ,load_1_di_type: bool = False
    ,query_json_di_type: str = '[]'
    ,load_1_ok_di_type: bool = False
    ,query_json_ok_di_type: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_user_cetr**: load one item from User
    - **query_json_user_cetr**: json array to filter the User object that 
            user_cetr_id object should pass
    - **load_1_user_edit**: load one item from User
    - **query_json_user_edit**: json array to filter the User object that 
            user_edit_id object should pass
    - **load_1_user_aprv**: load one item from User
    - **query_json_user_aprv**: json array to filter the User object that 
            user_aprv_id object should pass
    - **load_1_di_master**: load one item from Dttype
    - **query_json_di_master**: json array to filter the Dttype object that 
            di_master_id object should pass
    - **load_1_di_type**: load one item from Dttype
    - **query_json_di_type**: json array to filter the Dttype object that 
            di_type_id object should pass
    - **load_1_ok_di_type**: load one item from Dttype
    - **query_json_ok_di_type**: json array to filter the Dttype object that 
            ok_di_type_id object should pass
    """
    result = None

    fields = {
        'load_1_user_cetr': load_1_user_cetr,
        'query_json_user_cetr': query_json_user_cetr,
        'load_1_user_edit': load_1_user_edit,
        'query_json_user_edit': query_json_user_edit,
        'load_1_user_aprv': load_1_user_aprv,
        'query_json_user_aprv': query_json_user_aprv,
        'load_1_di_master': load_1_di_master,
        'query_json_di_master': query_json_di_master,
        'load_1_di_type': load_1_di_type,
        'query_json_di_type': query_json_di_type,
        'load_1_ok_di_type': load_1_ok_di_type,
        'query_json_ok_di_type': query_json_ok_di_type,
    }


    
    if('read_dtitem' in usercontrol_defs):
        read_dtitem = getattr(usercontrol, 'read_dtitem')
        result = read_dtitem(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_dtitem(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Dtitem_byId  ---------------------------------------------------------------
@app.get("/dtitem/{id}", tags=["Dtitem"])
def Read_Dtitem_byId(
    id: int
    ,load_user_user_cetr: bool = False
    ,load_user_user_edit: bool = False
    ,load_user_user_aprv: bool = False
    ,load_dttype_di_master: bool = False
    ,load_dttype_di_type: bool = False
    ,load_dttype_ok_di_type: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_dtitem_byId' in usercontrol_defs):
        read_dtitem_byId = getattr(usercontrol, 'read_dtitem_byId')

        result = read_dtitem_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_dttype_di_master=load_dttype_di_master
            ,load_dttype_di_type=load_dttype_di_type
            ,load_dttype_ok_di_type=load_dttype_ok_di_type
        )
    else:
        result = crud.read_dtitem_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_dttype_di_master=load_dttype_di_master
            ,load_dttype_di_type=load_dttype_di_type
            ,load_dttype_ok_di_type=load_dttype_ok_di_type
        )

    return result;


## Insert_Dtitem  --------------------------------------------------------------
@app.post("/dtitem", tags=["Dtitem"])
def Insert_Dtitem(
    the_Dtitem: schemas.Dtitem_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Dtitem2 = schemas.Dtitem(
        # Other fields use default values
        di_master_id = the_Dtitem.di_master_id,
        di_kind = the_Dtitem.di_kind,
        name = the_Dtitem.name,
        di_type_id = the_Dtitem.di_type_id,
        di_value = the_Dtitem.di_value,
        desc1 = the_Dtitem.desc1,
        desc2 = the_Dtitem.desc2,
    )

    if('insert_dtitem' in usercontrol_defs):
        insert_dtitem = getattr(usercontrol, 'insert_dtitem')
        result = insert_dtitem(db, user, the_Dtitem2)
    else:
        result = crud.insert_dtitem(db, user, the_Dtitem2)

    db.commit()
    return result


## Patch_Dtitem --------------------------------------------------------------------
@app.patch("/dtitem/{id}", tags=["Dtitem"])
def Patch_Dtitem(
    id: int
    ,the_Dtitem: schemas.Dtitem_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'name': the_Dtitem.name
        ,'di_type_id': the_Dtitem.di_type_id
        ,'di_value': the_Dtitem.di_value
        ,'desc1': the_Dtitem.desc1
        ,'desc2': the_Dtitem.desc2
    }

    if('patch_dtitem' in usercontrol_defs):
        patch_dtitem = getattr(usercontrol, 'patch_dtitem')

        result = patch_dtitem(db, user, id, fields=p)
    else:
        result = crud.patch_dtitem(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Dtitem  ------------------------------------------------------------------
@app.delete("/dtitem/{id}", tags=["Dtitem"])
def Delete_Dtitem(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_dtitem' in usercontrol_defs):
        delete_dtitem = getattr(usercontrol, 'delete_dtitem')

        result = delete_dtitem(db, user, id)
    else:
        result = crud.delete_dtitem(db, user, id)

    db.commit()
    return result


## history_Dtitem  -----------------------------------------------------------------------
@app.get("/dtitem/history/{id}", tags=["Dtitem"])
def history_Dtitem(id: int
    ,page: int = 1
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    return crud.read_history_dtitem(db, user, id, page)

#endregion dtitem


#region topic

## Topic #####################################################################
## Read_Topic  ----------------------------------------------------------------
@app.get("/topic/read", tags=["Topic"],
summary="read the Topic with search & pagination"
)
def Read_Topic(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user_cetr: bool = False
    ,query_json_user_cetr: str = '[]'
    ,load_1_user_edit: bool = False
    ,query_json_user_edit: str = '[]'
    ,load_1_user_aprv: bool = False
    ,query_json_user_aprv: str = '[]'
    ,load_1_proj: bool = False
    ,query_json_proj: str = '[]'
    ,load_1_start_dttype: bool = False
    ,query_json_start_dttype: str = '[]'
    ,load_1_end_dttype: bool = False
    ,query_json_end_dttype: str = '[]'
    ,load_1_ok_start_dttype: bool = False
    ,query_json_ok_start_dttype: str = '[]'
    ,load_1_ok_end_dttype: bool = False
    ,query_json_ok_end_dttype: str = '[]'
    ,load_n_topic_federatetopic: bool = False
    ,params_topic_federatetopic: str = '{}'
    ,query_json_topic_federatetopic: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_user_cetr**: load one item from User
    - **query_json_user_cetr**: json array to filter the User object that 
            user_cetr_id object should pass
    - **load_1_user_edit**: load one item from User
    - **query_json_user_edit**: json array to filter the User object that 
            user_edit_id object should pass
    - **load_1_user_aprv**: load one item from User
    - **query_json_user_aprv**: json array to filter the User object that 
            user_aprv_id object should pass
    - **load_1_proj**: load one item from Project
    - **query_json_proj**: json array to filter the Project object that 
            proj_id object should pass
    - **load_1_start_dttype**: load one item from Dttype
    - **query_json_start_dttype**: json array to filter the Dttype object that 
            start_dttype_id object should pass
    - **load_1_end_dttype**: load one item from Dttype
    - **query_json_end_dttype**: json array to filter the Dttype object that 
            end_dttype_id object should pass
    - **load_1_ok_start_dttype**: load one item from Dttype
    - **query_json_ok_start_dttype**: json array to filter the Dttype object that 
            ok_start_dttype_id object should pass
    - **load_1_ok_end_dttype**: load one item from Dttype
    - **query_json_ok_end_dttype**: json array to filter the Dttype object that 
            ok_end_dttype_id object should pass
    - **load_n_topic_federatetopic**: load many federatetopic items that have relation with Topic
    - **params_topic_federatetopic**: parameters of this load See route federatetopic/read - assign it with JSON.stringify(...)
    - **query_json_topic_federatetopic**: json array filter that many items of federatetopic should pass
    """
    result = None

    fields = {
        'load_1_user_cetr': load_1_user_cetr,
        'query_json_user_cetr': query_json_user_cetr,
        'load_1_user_edit': load_1_user_edit,
        'query_json_user_edit': query_json_user_edit,
        'load_1_user_aprv': load_1_user_aprv,
        'query_json_user_aprv': query_json_user_aprv,
        'load_1_proj': load_1_proj,
        'query_json_proj': query_json_proj,
        'load_1_start_dttype': load_1_start_dttype,
        'query_json_start_dttype': query_json_start_dttype,
        'load_1_end_dttype': load_1_end_dttype,
        'query_json_end_dttype': query_json_end_dttype,
        'load_1_ok_start_dttype': load_1_ok_start_dttype,
        'query_json_ok_start_dttype': query_json_ok_start_dttype,
        'load_1_ok_end_dttype': load_1_ok_end_dttype,
        'query_json_ok_end_dttype': query_json_ok_end_dttype,
        'load_n_topic_federatetopic':load_n_topic_federatetopic,
        'params_topic_federatetopic':json.loads(params_topic_federatetopic),
        'query_json_topic_federatetopic':query_json_topic_federatetopic,
    }


    
    if('read_topic' in usercontrol_defs):
        read_topic = getattr(usercontrol, 'read_topic')
        result = read_topic(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_topic(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Topic_byId  ---------------------------------------------------------------
@app.get("/topic/{id}", tags=["Topic"])
def Read_Topic_byId(
    id: int
    ,load_user_user_cetr: bool = False
    ,load_user_user_edit: bool = False
    ,load_user_user_aprv: bool = False
    ,load_project_proj: bool = False
    ,load_dttype_start_dttype: bool = False
    ,load_dttype_end_dttype: bool = False
    ,load_dttype_ok_start_dttype: bool = False
    ,load_dttype_ok_end_dttype: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_topic_byId' in usercontrol_defs):
        read_topic_byId = getattr(usercontrol, 'read_topic_byId')

        result = read_topic_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_project_proj=load_project_proj
            ,load_dttype_start_dttype=load_dttype_start_dttype
            ,load_dttype_end_dttype=load_dttype_end_dttype
            ,load_dttype_ok_start_dttype=load_dttype_ok_start_dttype
            ,load_dttype_ok_end_dttype=load_dttype_ok_end_dttype
        )
    else:
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

    return result;


## Insert_Topic  --------------------------------------------------------------
@app.post("/topic", tags=["Topic"])
def Insert_Topic(
    the_Topic: schemas.Topic_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Topic2 = schemas.Topic(
        # Other fields use default values
        proj_id = the_Topic.proj_id,
        start_dttype_id = the_Topic.start_dttype_id,
        end_dttype_id = the_Topic.end_dttype_id,
        name = the_Topic.name,
        desc1 = the_Topic.desc1,
        desc2 = the_Topic.desc2,
    )

    if('insert_topic' in usercontrol_defs):
        insert_topic = getattr(usercontrol, 'insert_topic')
        result = insert_topic(db, user, the_Topic2)
    else:
        result = crud.insert_topic(db, user, the_Topic2)

    db.commit()
    return result


## Patch_Topic --------------------------------------------------------------------
@app.patch("/topic/{id}", tags=["Topic"])
def Patch_Topic(
    id: int
    ,the_Topic: schemas.Topic_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'start_dttype_id': the_Topic.start_dttype_id
        ,'end_dttype_id': the_Topic.end_dttype_id
        ,'name': the_Topic.name
        ,'desc1': the_Topic.desc1
        ,'desc2': the_Topic.desc2
        ,'graph': the_Topic.graph
    }

    if('patch_topic' in usercontrol_defs):
        patch_topic = getattr(usercontrol, 'patch_topic')

        result = patch_topic(db, user, id, fields=p)
    else:
        result = crud.patch_topic(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Topic  ------------------------------------------------------------------
@app.delete("/topic/{id}", tags=["Topic"])
def Delete_Topic(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_topic' in usercontrol_defs):
        delete_topic = getattr(usercontrol, 'delete_topic')

        result = delete_topic(db, user, id)
    else:
        result = crud.delete_topic(db, user, id)

    db.commit()
    return result


## history_Topic  -----------------------------------------------------------------------
@app.get("/topic/history/{id}", tags=["Topic"])
def history_Topic(id: int
    ,page: int = 1
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    return crud.read_history_topic(db, user, id, page)

#endregion topic


#region federate

## Federate #####################################################################
## Read_Federate  ----------------------------------------------------------------
@app.get("/federate/read", tags=["Federate"],
summary="read the Federate with search & pagination"
)
def Read_Federate(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user_cetr: bool = False
    ,query_json_user_cetr: str = '[]'
    ,load_1_user_edit: bool = False
    ,query_json_user_edit: str = '[]'
    ,load_1_user_aprv: bool = False
    ,query_json_user_aprv: str = '[]'
    ,load_1_proj: bool = False
    ,query_json_proj: str = '[]'
    ,load_n_federate_federatetopic: bool = False
    ,params_federate_federatetopic: str = '{}'
    ,query_json_federate_federatetopic: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_user_cetr**: load one item from User
    - **query_json_user_cetr**: json array to filter the User object that 
            user_cetr_id object should pass
    - **load_1_user_edit**: load one item from User
    - **query_json_user_edit**: json array to filter the User object that 
            user_edit_id object should pass
    - **load_1_user_aprv**: load one item from User
    - **query_json_user_aprv**: json array to filter the User object that 
            user_aprv_id object should pass
    - **load_1_proj**: load one item from Project
    - **query_json_proj**: json array to filter the Project object that 
            proj_id object should pass
    - **load_n_federate_federatetopic**: load many federatetopic items that have relation with Federate
    - **params_federate_federatetopic**: parameters of this load See route federatetopic/read - assign it with JSON.stringify(...)
    - **query_json_federate_federatetopic**: json array filter that many items of federatetopic should pass
    """
    result = None

    fields = {
        'load_1_user_cetr': load_1_user_cetr,
        'query_json_user_cetr': query_json_user_cetr,
        'load_1_user_edit': load_1_user_edit,
        'query_json_user_edit': query_json_user_edit,
        'load_1_user_aprv': load_1_user_aprv,
        'query_json_user_aprv': query_json_user_aprv,
        'load_1_proj': load_1_proj,
        'query_json_proj': query_json_proj,
        'load_n_federate_federatetopic':load_n_federate_federatetopic,
        'params_federate_federatetopic':json.loads(params_federate_federatetopic),
        'query_json_federate_federatetopic':query_json_federate_federatetopic,
    }


    
    if('read_federate' in usercontrol_defs):
        read_federate = getattr(usercontrol, 'read_federate')
        result = read_federate(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_federate(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Federate_byId  ---------------------------------------------------------------
@app.get("/federate/{id}", tags=["Federate"])
def Read_Federate_byId(
    id: int
    ,load_user_user_cetr: bool = False
    ,load_user_user_edit: bool = False
    ,load_user_user_aprv: bool = False
    ,load_project_proj: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_federate_byId' in usercontrol_defs):
        read_federate_byId = getattr(usercontrol, 'read_federate_byId')

        result = read_federate_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_project_proj=load_project_proj
        )
    else:
        result = crud.read_federate_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_project_proj=load_project_proj
        )

    return result;


## Insert_Federate  --------------------------------------------------------------
@app.post("/federate", tags=["Federate"])
def Insert_Federate(
    the_Federate: schemas.Federate_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Federate2 = schemas.Federate(
        # Other fields use default values
        proj_id = the_Federate.proj_id,
        name = the_Federate.name,
        desc1 = the_Federate.desc1,
        desc2 = the_Federate.desc2,
        login = the_Federate.login,
        passw = the_Federate.passw,
        token = the_Federate.token,
        ip = the_Federate.ip,
        mac = the_Federate.mac,
        host = the_Federate.host,
        port = the_Federate.port,
        connectionType = the_Federate.connectionType,
        liveness = the_Federate.liveness,
    )

    if('insert_federate' in usercontrol_defs):
        insert_federate = getattr(usercontrol, 'insert_federate')
        result = insert_federate(db, user, the_Federate2)
    else:
        result = crud.insert_federate(db, user, the_Federate2)

    db.commit()
    return result


## Patch_Federate --------------------------------------------------------------------
@app.patch("/federate/{id}", tags=["Federate"])
def Patch_Federate(
    id: int
    ,the_Federate: schemas.Federate_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'name': the_Federate.name
        ,'desc1': the_Federate.desc1
        ,'desc2': the_Federate.desc2
        ,'login': the_Federate.login
        ,'passw': the_Federate.passw
        ,'token': the_Federate.token
        ,'ip': the_Federate.ip
        ,'mac': the_Federate.mac
        ,'host': the_Federate.host
        ,'port': the_Federate.port
        ,'connectionType': the_Federate.connectionType
        ,'liveness': the_Federate.liveness
    }

    if('patch_federate' in usercontrol_defs):
        patch_federate = getattr(usercontrol, 'patch_federate')

        result = patch_federate(db, user, id, fields=p)
    else:
        result = crud.patch_federate(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Federate  ------------------------------------------------------------------
@app.delete("/federate/{id}", tags=["Federate"])
def Delete_Federate(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_federate' in usercontrol_defs):
        delete_federate = getattr(usercontrol, 'delete_federate')

        result = delete_federate(db, user, id)
    else:
        result = crud.delete_federate(db, user, id)

    db.commit()
    return result


## history_Federate  -----------------------------------------------------------------------
@app.get("/federate/history/{id}", tags=["Federate"])
def history_Federate(id: int
    ,page: int = 1
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    return crud.read_history_federate(db, user, id, page)

#endregion federate


#region federatetopic

## Federatetopic #####################################################################
## Read_Federatetopic  ----------------------------------------------------------------
@app.get("/federatetopic/read", tags=["Federatetopic"],
summary="read the Federatetopic with search & pagination"
)
def Read_Federatetopic(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_federate: bool = False
    ,query_json_federate: str = '[]'
    ,load_1_topic: bool = False
    ,query_json_topic: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_federate**: load one item from Federate
    - **query_json_federate**: json array to filter the Federate object that 
            federate_id object should pass
    - **load_1_topic**: load one item from Topic
    - **query_json_topic**: json array to filter the Topic object that 
            topic_id object should pass
    """
    result = None

    fields = {
        'load_1_federate': load_1_federate,
        'query_json_federate': query_json_federate,
        'load_1_topic': load_1_topic,
        'query_json_topic': query_json_topic,
    }


    
    if('read_federatetopic' in usercontrol_defs):
        read_federatetopic = getattr(usercontrol, 'read_federatetopic')
        result = read_federatetopic(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_federatetopic(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Federatetopic_byId  ---------------------------------------------------------------
@app.get("/federatetopic/{id}", tags=["Federatetopic"])
def Read_Federatetopic_byId(
    id: int
    ,load_user_user_cetr: bool = False
    ,load_user_user_edit: bool = False
    ,load_user_user_aprv: bool = False
    ,load_federate_federate: bool = False
    ,load_topic_topic: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_federatetopic_byId' in usercontrol_defs):
        read_federatetopic_byId = getattr(usercontrol, 'read_federatetopic_byId')

        result = read_federatetopic_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_federate_federate=load_federate_federate
            ,load_topic_topic=load_topic_topic
        )
    else:
        result = crud.read_federatetopic_byId(db, user, id
            ,load_user_user_cetr=load_user_user_cetr
            ,load_user_user_edit=load_user_user_edit
            ,load_user_user_aprv=load_user_user_aprv
            ,load_federate_federate=load_federate_federate
            ,load_topic_topic=load_topic_topic
        )

    return result;


## Insert_Federatetopic  --------------------------------------------------------------
@app.post("/federatetopic", tags=["Federatetopic"])
def Insert_Federatetopic(
    the_Federatetopic: schemas.Federatetopic_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Federatetopic2 = schemas.Federatetopic(
        # Other fields use default values
        federate_id = the_Federatetopic.federate_id,
        topic_id = the_Federatetopic.topic_id,
        dir = the_Federatetopic.dir,
        desc1 = the_Federatetopic.desc1,
        desc2 = the_Federatetopic.desc2,
    )

    if('insert_federatetopic' in usercontrol_defs):
        insert_federatetopic = getattr(usercontrol, 'insert_federatetopic')
        result = insert_federatetopic(db, user, the_Federatetopic2)
    else:
        result = crud.insert_federatetopic(db, user, the_Federatetopic2)

    db.commit()
    return result


## Patch_Federatetopic --------------------------------------------------------------------
@app.patch("/federatetopic/{id}", tags=["Federatetopic"])
def Patch_Federatetopic(
    id: int
    ,the_Federatetopic: schemas.Federatetopic_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'federate_id': the_Federatetopic.federate_id
        ,'topic_id': the_Federatetopic.topic_id
        ,'dir': the_Federatetopic.dir
        ,'desc1': the_Federatetopic.desc1
        ,'desc2': the_Federatetopic.desc2
    }

    if('patch_federatetopic' in usercontrol_defs):
        patch_federatetopic = getattr(usercontrol, 'patch_federatetopic')

        result = patch_federatetopic(db, user, id, fields=p)
    else:
        result = crud.patch_federatetopic(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Federatetopic  ------------------------------------------------------------------
@app.delete("/federatetopic/{id}", tags=["Federatetopic"])
def Delete_Federatetopic(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_federatetopic' in usercontrol_defs):
        delete_federatetopic = getattr(usercontrol, 'delete_federatetopic')

        result = delete_federatetopic(db, user, id)
    else:
        result = crud.delete_federatetopic(db, user, id)

    db.commit()
    return result



#endregion federatetopic


#region diagram

## Diagram #####################################################################
## Read_Diagram  ----------------------------------------------------------------
@app.get("/diagram/read", tags=["Diagram"],
summary="read the Diagram with search & pagination"
)
def Read_Diagram(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_proj: bool = False
    ,query_json_proj: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_proj**: load one item from Project
    - **query_json_proj**: json array to filter the Project object that 
            proj_id object should pass
    """
    result = None

    fields = {
        'load_1_proj': load_1_proj,
        'query_json_proj': query_json_proj,
    }


    
    if('read_diagram' in usercontrol_defs):
        read_diagram = getattr(usercontrol, 'read_diagram')
        result = read_diagram(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_diagram(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Diagram_byId  ---------------------------------------------------------------
@app.get("/diagram/{id}", tags=["Diagram"])
def Read_Diagram_byId(
    id: int
    ,load_project_proj: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_diagram_byId' in usercontrol_defs):
        read_diagram_byId = getattr(usercontrol, 'read_diagram_byId')

        result = read_diagram_byId(db, user, id
            ,load_project_proj=load_project_proj
        )
    else:
        result = crud.read_diagram_byId(db, user, id
            ,load_project_proj=load_project_proj
        )

    return result;


## Insert_Diagram  --------------------------------------------------------------
@app.post("/diagram", tags=["Diagram"])
def Insert_Diagram(
    the_Diagram: schemas.Diagram_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Diagram2 = schemas.Diagram(
        # Other fields use default values
        name = the_Diagram.name,
        proj_id = the_Diagram.proj_id,
        Content = the_Diagram.Content,
    )

    if('insert_diagram' in usercontrol_defs):
        insert_diagram = getattr(usercontrol, 'insert_diagram')
        result = insert_diagram(db, user, the_Diagram2)
    else:
        result = crud.insert_diagram(db, user, the_Diagram2)

    db.commit()
    return result


## Patch_Diagram --------------------------------------------------------------------
@app.patch("/diagram/{id}", tags=["Diagram"])
def Patch_Diagram(
    id: int
    ,the_Diagram: schemas.Diagram_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'name': the_Diagram.name
        ,'Content': the_Diagram.Content
    }

    if('patch_diagram' in usercontrol_defs):
        patch_diagram = getattr(usercontrol, 'patch_diagram')

        result = patch_diagram(db, user, id, fields=p)
    else:
        result = crud.patch_diagram(db, user, id, fields=p)

    db.commit()
    return result


## Delete_Diagram  ------------------------------------------------------------------
@app.delete("/diagram/{id}", tags=["Diagram"])
def Delete_Diagram(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_diagram' in usercontrol_defs):
        delete_diagram = getattr(usercontrol, 'delete_diagram')

        result = delete_diagram(db, user, id)
    else:
        result = crud.delete_diagram(db, user, id)

    db.commit()
    return result



#endregion diagram


#region wiki

## Wiki #####################################################################
## Read_Wiki  ----------------------------------------------------------------
@app.get("/wiki/read", tags=["Wiki"],
summary="read the Wiki with search & pagination"
)
def Read_Wiki(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_user: bool = False
    ,query_json_user: str = '[]'
    ,load_n_wiki_wiki_tags: bool = False
    ,params_wiki_wiki_tags: str = '{}'
    ,query_json_wiki_wiki_tags: str = '[]'
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
    - **load_n_wiki_wiki_tags**: load many wiki_tags items that have relation with Wiki
    - **params_wiki_wiki_tags**: parameters of this load See route wiki_tags/read - assign it with JSON.stringify(...)
    - **query_json_wiki_wiki_tags**: json array filter that many items of wiki_tags should pass
    """
    result = None

    fields = {
        'load_1_user': load_1_user,
        'query_json_user': query_json_user,
        'load_n_wiki_wiki_tags':load_n_wiki_wiki_tags,
        'params_wiki_wiki_tags':json.loads(params_wiki_wiki_tags),
        'query_json_wiki_wiki_tags':query_json_wiki_wiki_tags,
    }


    
    if('read_wiki' in usercontrol_defs):
        read_wiki = getattr(usercontrol, 'read_wiki')
        result = read_wiki(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_wiki(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Wiki_byId  ---------------------------------------------------------------
@app.get("/wiki/{id}", tags=["Wiki"])
def Read_Wiki_byId(
    id: int
    ,load_user_user: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_wiki_byId' in usercontrol_defs):
        read_wiki_byId = getattr(usercontrol, 'read_wiki_byId')

        result = read_wiki_byId(db, user, id
            ,load_user_user=load_user_user
        )
    else:
        result = crud.read_wiki_byId(db, user, id
            ,load_user_user=load_user_user
        )

    return result;


## Insert_Wiki  --------------------------------------------------------------
@app.post("/wiki", tags=["Wiki"])
def Insert_Wiki(
    the_Wiki: schemas.Wiki_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Wiki2 = schemas.Wiki(
        # Other fields use default values
        moment = the_Wiki.moment,
        content = the_Wiki.content,
    )

    if('insert_wiki' in usercontrol_defs):
        insert_wiki = getattr(usercontrol, 'insert_wiki')
        result = insert_wiki(db, user, the_Wiki2)
    else:
        result = crud.insert_wiki(db, user, the_Wiki2)

    db.commit()
    return result


## Patch_Wiki --------------------------------------------------------------------
@app.patch("/wiki/{id}", tags=["Wiki"])
def Patch_Wiki(
    id: int
    ,the_Wiki: schemas.Wiki_patch
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    p = {
        'id': id
        ,'content': the_Wiki.content
    }

    if('patch_wiki' in usercontrol_defs):
        patch_wiki = getattr(usercontrol, 'patch_wiki')

        result = patch_wiki(db, user, id, fields=p)
    else:
        result = crud.patch_wiki(db, user, id, fields=p)

    db.commit()
    return result



#endregion wiki


#region wiki_tags

## Wiki_Tags #####################################################################
## Read_Wiki_Tags  ----------------------------------------------------------------
@app.get("/wiki_tags/read", tags=["Wiki_Tags"],
summary="read the Wiki_Tags with search & pagination"
)
def Read_Wiki_Tags(
    page: int = 1
    ,pageSize: int = 10
    ,filter: str = ''
    ,query_json: str | None=None
    ,order_by: str | None = '[["id"]]'
    ,all_rows: bool = False
    ,load_1_wiki: bool = False
    ,query_json_wiki: str = '[]'
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):

    """
    - **query_json**: a json list of objects 
        like [{ "field":"id", "op":"eq", "value": 2 }] 
        op is one of eq,le,lt,ge,gt,cn: contains, in
        assign it with JSON.stringify(...)
    - **filter**: as plain string means all fields contains that string    
    - **load_1_wiki**: load one item from Wiki
    - **query_json_wiki**: json array to filter the Wiki object that 
            wiki_id object should pass
    """
    result = None

    fields = {
        'load_1_wiki': load_1_wiki,
        'query_json_wiki': query_json_wiki,
    }


    
    if('read_wiki_tags' in usercontrol_defs):
        read_wiki_tags = getattr(usercontrol, 'read_wiki_tags')
        result = read_wiki_tags(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)
    else:
        result = crud.read_wiki_tags(db, user, page, pageSize, filter, query_json, order_by, all_rows, fields)

    return result


## Read_Wiki_Tags_byId  ---------------------------------------------------------------
@app.get("/wiki_tags/{id}", tags=["Wiki_Tags"])
def Read_Wiki_Tags_byId(
    id: int
    ,load_wiki_wiki: bool = False
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('read_wiki_tags_byId' in usercontrol_defs):
        read_wiki_tags_byId = getattr(usercontrol, 'read_wiki_tags_byId')

        result = read_wiki_tags_byId(db, user, id
            ,load_wiki_wiki=load_wiki_wiki
        )
    else:
        result = crud.read_wiki_tags_byId(db, user, id
            ,load_wiki_wiki=load_wiki_wiki
        )

    return result;


## Insert_Wiki_Tags  --------------------------------------------------------------
@app.post("/wiki_tags", tags=["Wiki_Tags"])
def Insert_Wiki_Tags(
    the_Wiki_Tags: schemas.Wiki_Tags_post
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    the_Wiki_Tags2 = schemas.Wiki_Tags(
        # Other fields use default values
        wiki_id = the_Wiki_Tags.wiki_id,
        thing = the_Wiki_Tags.thing,
        thing_id = the_Wiki_Tags.thing_id,
    )

    if('insert_wiki_tags' in usercontrol_defs):
        insert_wiki_tags = getattr(usercontrol, 'insert_wiki_tags')
        result = insert_wiki_tags(db, user, the_Wiki_Tags2)
    else:
        result = crud.insert_wiki_tags(db, user, the_Wiki_Tags2)

    db.commit()
    return result


## Delete_Wiki_Tags  ------------------------------------------------------------------
@app.delete("/wiki_tags/{id}", tags=["Wiki_Tags"])
def Delete_Wiki_Tags(
    id: int
    ,user: dict = Depends(get_current_user)
    ,db: Session = Depends(get_db)
):
    result = None

    if('delete_wiki_tags' in usercontrol_defs):
        delete_wiki_tags = getattr(usercontrol, 'delete_wiki_tags')

        result = delete_wiki_tags(db, user, id)
    else:
        result = crud.delete_wiki_tags(db, user, id)

    db.commit()
    return result



#endregion wiki_tags


