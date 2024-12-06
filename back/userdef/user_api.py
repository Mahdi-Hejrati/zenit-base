from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, text
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from zenitdb.database import get_db
# from datetime import datetime,timedelta
from zenitdb.app import app
from zenitdb import crud, schemas, models
from userdef.user_login import get_current_user
from userdef.usercontrol import ControlProjectAccess, raiseError

# from conf.conf import Test_Mode


## Approve_Dttype  --------------------------------------------------------------
@app.post("/dttype/approve/{id}", tags=["Dttype"])
def Approve_Dttype(
    id: int
    ,user: Annotated[dict, Depends(get_current_user)]
    ,db: Session = Depends(get_db)
):
    dttype = db.get(models.Dttype, id)
    if dttype == None:
        raiseError(404, 'NOT_FOUND', msg='DataType Not found')

    if not ControlProjectAccess(db, dttype.proj_id, user.id, 'master'):
        raiseError(403, 'NO_ACCESS', msg='Access Denied, connect with Project master')
        
    stmt = (
        select(models.Dttype)
        .where(models.Dttype.ok_name == dttype.name)
        .where(models.Dttype.proj_id == dttype.proj_id)
        .where(models.Dttype.id != dttype.id)
    )

    repeted = db.scalars(stmt).all()

    if len(repeted) > 0:
        raiseError(422, 'NAME_REPEAT', msg='Name [{dtitem.name}] used with other DataTypes'
                   , items=[{'id':i.id, 'name':i.name,'ok_name':i.ok_name} for i in repeted])

    stmt = (
        select(models.Dtitem)
        .where(models.Dtitem.di_master_id == dttype.id)
    )

    items = db.scalars(stmt).all()

    not_approved_items = [{'id':i.id, 'name':i.name,'ok_name':i.ok_name} for i in items if i.modified]
    if len(not_approved_items) > 0:
        raiseError(422, 'ITEM_NOT_APPROVE', msg='please Approve Items First', items=not_approved_items)


    diff_items_kind = [{'id':i.id, 'name':i.name,'ok_name':i.ok_name} for i in items if i.di_kind != dttype.dt_kind]
    if len(diff_items_kind) > 0:
        raiseError(422, 'ITEM_TYPE_MISMATCH', msg='Items must have kind of DataType', items=diff_items_kind)

    dttype.aprv_time = schemas.parse_ZDate('n')
    dttype.user_aprv_id = user.id
    dttype.modified = 0
    dttype.ok_name = dttype.name
    dttype.ok_desc1 = dttype.desc1
    dttype.ok_desc2 = dttype.desc2

    db.commit()
    return crud.read_dttype_byId(db, user, id)

## Approve_Dtitem  --------------------------------------------------------------
@app.post("/dtitem/approve/{id}", tags=["Dtitem"])
def Approve_Dtitem(
    id: int
    ,user: Annotated[dict, Depends(get_current_user)]
    ,db: Session = Depends(get_db)
):
    dtitem = db.get(models.Dtitem, id)
    if dtitem == None:
        raiseError(404, 'NOT_FOUND', msg='Data Item Not Found')

        
    dttype = db.get(models.Dttype, dtitem.di_master_id)
    if dttype == None:
        raiseError(404, 'NOT_FOUND', msg='DataType Not Found')

    if not ControlProjectAccess(db, dttype.proj_id, user.id, 'master'):
        raiseError(403, 'NO_ACCESS', msg='Access Denied, connect with Project master')
        
    stmt = (
        select(models.Dtitem)
        .where(models.Dtitem.ok_name == dtitem.name)
        .where(models.Dtitem.di_master_id == dtitem.di_master_id)
        .where(models.Dtitem.id != dtitem.id)
    )

    repeted = db.scalars(stmt).all()

    if len(repeted) > 0:
        raiseError(422, 'NAME_REPEAT', msg=f'Name [{dtitem.name}] is repeated', items=[{'id':i.id, 'name':i.name,'ok_name':i.ok_name} for i in repeted])

    if dtitem.di_kind == 'struct' and (not dtitem.di_type_id in [-1, -2, -3, -4, -5, -6, -7, -8, -9]):
        dtitem_type = db.get(models.Dttype, dtitem.di_type_id)
        if dtitem_type == None:
            raiseError(404, 'ITEM_TYPE_NOT_FOUND', msg='Type of this Item not found'
                       , type_id=dtitem.di_type_id)

    dtitem.user_aprv_id = user.id
    dtitem.aprv_time = schemas.parse_ZDate('n')
    dtitem.ok_name = dtitem.name
    dtitem.ok_desc1 = dtitem.desc1
    dtitem.ok_desc2 = dtitem.desc2

    dtitem.ok_di_type_id = dtitem.di_type_id
    dtitem.ok_di_value = dtitem.di_value

    dtitem.modified = 0

    db.commit()
    
    return crud.read_dtitem_byId(db, user, id)

## Approve_Topic
@app.post("/topic/approve/{id}", tags=["Topic"])
def Approve_Topic(
    id: int
    ,user: Annotated[dict, Depends(get_current_user)]
    ,db: Session = Depends(get_db)
):
    topic = db.get(models.Topic, id)
    if topic == None:
        raiseError(404, 'NOT_FOUND', msg='Topic not found')

    if not ControlProjectAccess(db, topic.proj_id, user.id):
        raiseError(403, 'NO_ACCESS', msg='Access Denied, connect with Project master')

    start_type = db.get(models.Dttype, topic.start_dttype_id)
    if start_type == None:
        raiseError(404, 'NOT_FOUND', msg='Start DataType Not Found')

    end_type = db.get(models.Dttype, topic.end_dttype_id)
    if end_type == None:
        raiseError(404, 'NOT_FOUND', msg='End DataType Not Found')

    stmt = (
        select(models.Topic)
        .where(models.Topic.ok_name == topic.name)
        .where(models.Topic.proj_id == topic.proj_id)
        .where(models.Topic.id != topic.id)
    )

    repeted = db.scalars(stmt).all()

    if len(repeted) > 0:
        raiseError(422, 'NAME_REPEAT', msg=f'Name [{topic.name}] used with other Topics'
                   , items=[{'id':i.id, 'name':i.name,'ok_name':i.ok_name} for i in repeted])

    topic.aprv_time = schemas.parse_ZDate('n')
    topic.user_aprv_id = user.id
    topic.modified = 0
    topic.ok_name = topic.name
    topic.ok_desc1 = topic.desc1
    topic.ok_desc2 = topic.desc2
    topic.ok_start_dttype_id = topic.start_dttype_id
    topic.ok_end_dttype_id = topic.end_dttype_id
    topic.ok_graph = topic.graph 

    db.commit()

    return crud.read_topic_byId(db, user, id)

## Approve_Federate  --------------------------------------------------------------
@app.post("/federate/approve/{id}", tags=["Federate"])
def Approve_Federate(
    id: int
    ,user: Annotated[dict, Depends(get_current_user)]
    ,db: Session = Depends(get_db)
):
    federate = db.get(models.Federate, id)
    if federate == None:
        raiseError(404, 'NOT_FOUND', msg='Federate Not found')
        
    if not ControlProjectAccess(db, federate.proj_id, user.id, 'master'):
        raiseError(403, 'NO_ACCESS', msg='Access Denied, connect with Project master')
        
    stmt = (
        select(models.Federate)
        .where(models.Federate.ok_name == federate.name)
        .where(models.Federate.proj_id == federate.proj_id)
        .where(models.Federate.id != federate.id)
    )

    repeted = db.scalars(stmt).all()

    if len(repeted) > 0:
        raiseError(422, '', msg=f"Name [{federate.name}] is used with other federate"
                   , items=[{'id':i.id, 'name':i.name,'ok_name':i.ok_name} for i in repeted])

    federate.modified = 0
    federate.user_aprv_id = user.id
    federate.aprv_time = schemas.parse_ZDate('n')
    federate.ok_name = federate.name
    federate.ok_desc1 = federate.desc1
    federate.ok_desc2 = federate.desc2

    db.commit()
    
    return crud.read_federate_byId(db, user, id)


