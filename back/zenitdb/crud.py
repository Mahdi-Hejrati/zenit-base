from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session, aliased
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from . import models,schemas
import json

def parse_json(json_str, dflt=[]):
    try:
        return json.loads(json_str)
    except:
        return dflt



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

    load_1_user_group = fields.get('load_1_user_group', False)
    query_json_user_group = fields.get('query_json_user_group', '[]')
    load_n_group_poshtiban_group = fields.get('load_n_group_poshtiban_group', False)
    params_group_poshtiban_group = fields.get('params_group_poshtiban_group', {})
    query_json_group_poshtiban_group = fields.get('query_json_group_poshtiban_group', '[]')
    load_n_assign_user_assign = fields.get('load_n_assign_user_assign', False)
    params_assign_user_assign = fields.get('params_assign_user_assign', {})
    query_json_assign_user_assign = fields.get('query_json_assign_user_assign', '[]')
    load_n_py_user_payment = fields.get('load_n_py_user_payment', False)
    params_py_user_payment = fields.get('params_py_user_payment', {})
    query_json_py_user_payment = fields.get('query_json_py_user_payment', '[]')
    load_n_user_sms = fields.get('load_n_user_sms', False)
    params_user_sms = fields.get('params_user_sms', {})
    query_json_user_sms = fields.get('query_json_user_sms', '[]')
    

#    debug_str = []
    stmt = select(models.User)

    query_json = parse_json(query_json)
    if(query_json):
        for f in query_json:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(models.User, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(models.User, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(models.User, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(models.User, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(models.User, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(models.User, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(models.User, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(models.User, f['field']).in_(f['value']))

    if(filter):
        stmt = stmt.where(
            or_(
                models.User.user_name.contains(filter),  
                models.User.user_mobile.contains(filter),  
                models.User.user_tel.contains(filter),  
                models.User.user_country.contains(filter),  
                models.User.user_city.contains(filter),  
                models.User.user_lang.contains(filter),  
                models.User.user_smshour.contains(filter),  
                models.User.user_access.contains(filter),  
                models.User.user_ack.contains(filter),  
                models.User.user_active.contains(filter),  
                models.User.user_bdate.contains(filter),  
                models.User.user_money.contains(filter),  
                models.User.user_iswomen.contains(filter),  
                models.User.user_smslevel.contains(filter),  
                models.User.user_smsfinishdate.contains(filter),  
                models.User.user_telegram_session.contains(filter)  
            )
        )


    _user_group = aliased(models.Group, name="_user_group")
    query_json_user_group = parse_json(query_json_user_group)

    if(query_json_user_group):
        stmt = stmt.join(_user_group, models.User.user_group_id == _user_group.id)

        for f in query_json_user_group:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_user_group, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_user_group, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_user_group, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_user_group, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_user_group, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_user_group, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_user_group, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_user_group, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_user_group NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_user_group NOT FOUND" )



    # load related_to back fields
    _group_poshtiban_group = aliased(models.Group, name="_group_poshtiban_group")
    query_json_group_poshtiban_group = parse_json(query_json_group_poshtiban_group)

    if(query_json_group_poshtiban_group):
        stmt = stmt.join(_group_poshtiban_group, models.User.id == _group_poshtiban_group.group_poshtiban_id)

        for f in query_json_group_poshtiban_group:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_group_poshtiban_group, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_group_poshtiban_group, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_group_poshtiban_group NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_group_poshtiban_group NOT FOUND" )

    _assign_user_assign = aliased(models.Assign, name="_assign_user_assign")
    query_json_assign_user_assign = parse_json(query_json_assign_user_assign)

    if(query_json_assign_user_assign):
        stmt = stmt.join(_assign_user_assign, models.User.id == _assign_user_assign.assign_user_id)

        for f in query_json_assign_user_assign:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_assign_user_assign, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_assign_user_assign, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_assign_user_assign NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_assign_user_assign NOT FOUND" )

    _py_user_payment = aliased(models.Payment, name="_py_user_payment")
    query_json_py_user_payment = parse_json(query_json_py_user_payment)

    if(query_json_py_user_payment):
        stmt = stmt.join(_py_user_payment, models.User.id == _py_user_payment.py_user_id)

        for f in query_json_py_user_payment:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_py_user_payment, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_py_user_payment, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_py_user_payment NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_py_user_payment NOT FOUND" )

    _user_sms = aliased(models.Sms, name="_user_sms")
    query_json_user_sms = parse_json(query_json_user_sms)

    if(query_json_user_sms):
        stmt = stmt.join(_user_sms, models.User.id == _user_sms.user_id)

        for f in query_json_user_sms:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_user_sms, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_user_sms, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_user_sms, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_user_sms, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_user_sms, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_user_sms, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_user_sms, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_user_sms, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_user_sms NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_user_sms NOT FOUND" )


    total = db.scalars(stmt.with_only_columns(func.count(models.User.id))).first()
    
    if(not all_rows):
        stmt = stmt.limit(pageSize)
        stmt = stmt.offset((page - 1) * pageSize)

    if(order_by):
        order_by = parse_json(order_by)
        for o in order_by:
            if(hasattr(models.User, o[0])):
                if(len(o) == 2 and o[1] == 'desc'):
                    stmt = stmt.order_by(getattr(models.User, o[0]).desc())
                else:
                    stmt = stmt.order_by(getattr(models.User, o[0]).asc())

    rows = db.scalars(stmt).all()

    for i in rows:
        if(load_1_user_group):
            i.user_group = read_group_byId(db, user, i.user_group_id)
        pass

    for i in rows:
        if(load_n_group_poshtiban_group):
            tl = query_json_group_poshtiban_group[:]
            tl.append({
                "field": "group_poshtiban_id", "op":"eq", "value":i.id
            })
            
            tmp = read_group(db, user, query_json = json.dumps(jsonable_encoder(tl)), all_rows = True, 
                                  fields=params_group_poshtiban_group)
            i.group_poshtiban_group_items = tmp["rows"]
#            for ds in tmp['debug_str']:
#                debug_str.append("group_poshtiban_group." + ds)

        if(load_n_assign_user_assign):
            tl = query_json_assign_user_assign[:]
            tl.append({
                "field": "assign_user_id", "op":"eq", "value":i.id
            })
            
            tmp = read_assign(db, user, query_json = json.dumps(jsonable_encoder(tl)), all_rows = True, 
                                  fields=params_assign_user_assign)
            i.assign_user_assign_items = tmp["rows"]
#            for ds in tmp['debug_str']:
#                debug_str.append("assign_user_assign." + ds)

        if(load_n_py_user_payment):
            tl = query_json_py_user_payment[:]
            tl.append({
                "field": "py_user_id", "op":"eq", "value":i.id
            })
            
            tmp = read_payment(db, user, query_json = json.dumps(jsonable_encoder(tl)), all_rows = True, 
                                  fields=params_py_user_payment)
            i.py_user_payment_items = tmp["rows"]
#            for ds in tmp['debug_str']:
#                debug_str.append("py_user_payment." + ds)

        if(load_n_user_sms):
            tl = query_json_user_sms[:]
            tl.append({
                "field": "user_id", "op":"eq", "value":i.id
            })
            
            tmp = read_sms(db, user, query_json = json.dumps(jsonable_encoder(tl)), all_rows = True, 
                                  fields=params_user_sms)
            i.user_sms_items = tmp["rows"]
#            for ds in tmp['debug_str']:
#                debug_str.append("user_sms." + ds)

        pass

    for i in range(len(rows)):
        rows[i].row_number = (pageSize * (page-1)) + i + 1
        pass

    return {
        "rows": rows, 
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "all_rows": all_rows,
        "order_by": order_by,
        "query_json": query_json,
        #"stmt": str(stmt).replace("\"", "`"),
        #"debug_str": debug_str
    }


## read_user_byId -------------------------------------------------------------
def read_user_byId(db: Session, user, id:int
    ,load_group_user_group: bool = False
):
    result = db.get(models.User, id)
    if(load_group_user_group and result):
        result.user_group = read_group_byId(db, user, result.user_group_id)

    return result

## insert_user -------------------------------------------------------------
def insert_user (
    db: Session
    ,user
    ,the_User: schemas.User
):

    db_thing = models.User(
                user_name=the_User.user_name, 
                user_mobile=the_User.user_mobile, 
                user_tel=the_User.user_tel, 
                user_country=the_User.user_country, 
                user_city=the_User.user_city, 
                user_lang=the_User.user_lang, 
                user_group_id=the_User.user_group_id, 
                user_smshour=the_User.user_smshour, 
                user_access=the_User.user_access, 
                user_ack=the_User.user_ack, 
                user_active=the_User.user_active, 
                user_bdate=the_User.user_bdate, 
                user_money=the_User.user_money, 
                user_iswomen=the_User.user_iswomen, 
                user_smslevel=the_User.user_smslevel, 
                user_smsfinishdate=the_User.user_smsfinishdate, 
                user_telegram_session=the_User.user_telegram_session 
            )
    db.add(db_thing)    
    db.flush()
    db.refresh(db_thing)

    result = {
        "the_User": jsonable_encoder(db_thing)
    }

    return result


## patch_user -------------------------------------------------------------
def patch_user(db: Session,user,id: int, fields):

    user_name = fields.get('user_name', None)
    user_mobile = fields.get('user_mobile', None)
    user_tel = fields.get('user_tel', None)
    user_country = fields.get('user_country', None)
    user_city = fields.get('user_city', None)
    user_lang = fields.get('user_lang', None)
    user_group_id = fields.get('user_group_id', None)
    user_smshour = fields.get('user_smshour', None)
    user_access = fields.get('user_access', None)
    user_ack = fields.get('user_ack', None)
    user_active = fields.get('user_active', None)
    user_bdate = fields.get('user_bdate', None)
    user_bdate = schemas.parse_ZDate(user_bdate)
    user_money = fields.get('user_money', None)
    user_iswomen = fields.get('user_iswomen', None)
    user_smslevel = fields.get('user_smslevel', None)
    user_smsfinishdate = fields.get('user_smsfinishdate', None)
    user_smsfinishdate = schemas.parse_ZDate(user_smsfinishdate)
    user_telegram_session = fields.get('user_telegram_session', None)


    db_thing = db.get(models.User, id)


    if(user_name is not None):
        db_thing.user_name = user_name
    if(user_mobile is not None):
        db_thing.user_mobile = user_mobile
    if(user_tel is not None):
        db_thing.user_tel = user_tel
    if(user_country is not None):
        db_thing.user_country = user_country
    if(user_city is not None):
        db_thing.user_city = user_city
    if(user_lang is not None):
        db_thing.user_lang = user_lang
    if(user_group_id is not None):
        db_thing.user_group_id = user_group_id
    if(user_smshour is not None):
        db_thing.user_smshour = user_smshour
    if(user_access is not None):
        db_thing.user_access = user_access
    if(user_ack is not None):
        db_thing.user_ack = user_ack
    if(user_active is not None):
        db_thing.user_active = user_active
    if(user_bdate is not None):
        db_thing.user_bdate = user_bdate
    if(user_money is not None):
        db_thing.user_money = user_money
    if(user_iswomen is not None):
        db_thing.user_iswomen = user_iswomen
    if(user_smslevel is not None):
        db_thing.user_smslevel = user_smslevel
    if(user_smsfinishdate is not None):
        db_thing.user_smsfinishdate = user_smsfinishdate
    if(user_telegram_session is not None):
        db_thing.user_telegram_session = user_telegram_session

    result = {
        "the_User": jsonable_encoder(db_thing)
    }

    return result

## delete_user -------------------------------------------------------------
def delete_user(db: Session, user, id: int):

    result = { }
    thing = db.get(models.User, id)
    if(thing):

        db.delete(thing)
        result["thing"] = jsonable_encoder(thing)
        result["state"] = "deleted"

        return result

        # end if

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

    load_1_group_poshtiban = fields.get('load_1_group_poshtiban', False)
    query_json_group_poshtiban = fields.get('query_json_group_poshtiban', '[]')
    load_n_user_group_user = fields.get('load_n_user_group_user', False)
    params_user_group_user = fields.get('params_user_group_user', {})
    query_json_user_group_user = fields.get('query_json_user_group_user', '[]')
    

#    debug_str = []
    stmt = select(models.Group)

    query_json = parse_json(query_json)
    if(query_json):
        for f in query_json:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(models.Group, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(models.Group, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(models.Group, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(models.Group, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(models.Group, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(models.Group, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(models.Group, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(models.Group, f['field']).in_(f['value']))

    if(filter):
        stmt = stmt.where(
            or_(
                models.Group.group_name.contains(filter),  
                models.Group.group_start_date.contains(filter),  
                models.Group.group_start_page.contains(filter),  
                models.Group.group_assign_day.contains(filter),  
                models.Group.group_uc.contains(filter),  
                models.Group.group_type.contains(filter)  
            )
        )


    _group_poshtiban = aliased(models.User, name="_group_poshtiban")
    query_json_group_poshtiban = parse_json(query_json_group_poshtiban)

    if(query_json_group_poshtiban):
        stmt = stmt.join(_group_poshtiban, models.Group.group_poshtiban_id == _group_poshtiban.id)

        for f in query_json_group_poshtiban:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_group_poshtiban, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_group_poshtiban, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_group_poshtiban NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_group_poshtiban NOT FOUND" )



    # load related_to back fields
    _user_group_user = aliased(models.User, name="_user_group_user")
    query_json_user_group_user = parse_json(query_json_user_group_user)

    if(query_json_user_group_user):
        stmt = stmt.join(_user_group_user, models.Group.id == _user_group_user.user_group_id)

        for f in query_json_user_group_user:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_user_group_user, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_user_group_user, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_user_group_user NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_user_group_user NOT FOUND" )


    total = db.scalars(stmt.with_only_columns(func.count(models.Group.id))).first()
    
    if(not all_rows):
        stmt = stmt.limit(pageSize)
        stmt = stmt.offset((page - 1) * pageSize)

    if(order_by):
        order_by = parse_json(order_by)
        for o in order_by:
            if(hasattr(models.Group, o[0])):
                if(len(o) == 2 and o[1] == 'desc'):
                    stmt = stmt.order_by(getattr(models.Group, o[0]).desc())
                else:
                    stmt = stmt.order_by(getattr(models.Group, o[0]).asc())

    rows = db.scalars(stmt).all()

    for i in rows:
        if(load_1_group_poshtiban):
            i.group_poshtiban = read_user_byId(db, user, i.group_poshtiban_id)
        pass

    for i in rows:
        if(load_n_user_group_user):
            tl = query_json_user_group_user[:]
            tl.append({
                "field": "user_group_id", "op":"eq", "value":i.id
            })
            
            tmp = read_user(db, user, query_json = json.dumps(jsonable_encoder(tl)), all_rows = True, 
                                  fields=params_user_group_user)
            i.user_group_user_items = tmp["rows"]
#            for ds in tmp['debug_str']:
#                debug_str.append("user_group_user." + ds)

        pass

    for i in range(len(rows)):
        rows[i].row_number = (pageSize * (page-1)) + i + 1
        pass

    return {
        "rows": rows, 
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "all_rows": all_rows,
        "order_by": order_by,
        "query_json": query_json,
        #"stmt": str(stmt).replace("\"", "`"),
        #"debug_str": debug_str
    }


## read_group_byId -------------------------------------------------------------
def read_group_byId(db: Session, user, id:int
    ,load_user_group_poshtiban: bool = False
):
    result = db.get(models.Group, id)
    if(load_user_group_poshtiban and result):
        result.group_poshtiban = read_user_byId(db, user, result.group_poshtiban_id)

    return result

## insert_group -------------------------------------------------------------
def insert_group (
    db: Session
    ,user
    ,the_Group: schemas.Group
):

    db_thing = models.Group(
                group_name=the_Group.group_name, 
                group_poshtiban_id=the_Group.group_poshtiban_id, 
                group_start_date=the_Group.group_start_date, 
                group_start_page=the_Group.group_start_page, 
                group_assign_day=the_Group.group_assign_day, 
                group_uc=the_Group.group_uc, 
                group_type=the_Group.group_type 
            )
    db.add(db_thing)    
    db.flush()
    db.refresh(db_thing)

    result = {
        "the_Group": jsonable_encoder(db_thing)
    }

    return result


## patch_group -------------------------------------------------------------
def patch_group(db: Session,user,id: int, fields):

    group_name = fields.get('group_name', None)
    group_poshtiban_id = fields.get('group_poshtiban_id', None)
    group_start_date = fields.get('group_start_date', None)
    group_start_date = schemas.parse_ZDate(group_start_date)
    group_start_page = fields.get('group_start_page', None)
    group_assign_day = fields.get('group_assign_day', None)
    group_assign_day = schemas.parse_ZDate(group_assign_day)
    group_uc = fields.get('group_uc', None)
    group_type = fields.get('group_type', None)


    db_thing = db.get(models.Group, id)


    if(group_name is not None):
        db_thing.group_name = group_name
    if(group_poshtiban_id is not None):
        db_thing.group_poshtiban_id = group_poshtiban_id
    if(group_start_date is not None):
        db_thing.group_start_date = group_start_date
    if(group_start_page is not None):
        db_thing.group_start_page = group_start_page
    if(group_assign_day is not None):
        db_thing.group_assign_day = group_assign_day
    if(group_uc is not None):
        db_thing.group_uc = group_uc
    if(group_type is not None):
        db_thing.group_type = group_type

    result = {
        "the_Group": jsonable_encoder(db_thing)
    }

    return result

## delete_group -------------------------------------------------------------
def delete_group(db: Session, user, id: int):

    result = { }
    thing = db.get(models.Group, id)
    if(thing):

        db.delete(thing)
        result["thing"] = jsonable_encoder(thing)
        result["state"] = "deleted"

        return result

        # end if

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

    load_1_assign_user = fields.get('load_1_assign_user', False)
    query_json_assign_user = fields.get('query_json_assign_user', '[]')
    

#    debug_str = []
    stmt = select(models.Assign)

    query_json = parse_json(query_json)
    if(query_json):
        for f in query_json:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(models.Assign, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(models.Assign, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(models.Assign, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(models.Assign, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(models.Assign, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(models.Assign, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(models.Assign, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(models.Assign, f['field']).in_(f['value']))

    if(filter):
        stmt = stmt.where(
            or_(
                models.Assign.assign_moment.contains(filter),  
                models.Assign.assign_pagenumber.contains(filter),  
                models.Assign.assign_status.contains(filter),  
                models.Assign.assign_done_moment.contains(filter),  
                models.Assign.assign_follow_result.contains(filter)  
            )
        )


    _assign_user = aliased(models.User, name="_assign_user")
    query_json_assign_user = parse_json(query_json_assign_user)

    if(query_json_assign_user):
        stmt = stmt.join(_assign_user, models.Assign.assign_user_id == _assign_user.id)

        for f in query_json_assign_user:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_assign_user, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_assign_user, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_assign_user, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_assign_user, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_assign_user, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_assign_user, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_assign_user, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_assign_user, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_assign_user NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_assign_user NOT FOUND" )



    # load related_to back fields

    total = db.scalars(stmt.with_only_columns(func.count(models.Assign.id))).first()
    
    if(not all_rows):
        stmt = stmt.limit(pageSize)
        stmt = stmt.offset((page - 1) * pageSize)

    if(order_by):
        order_by = parse_json(order_by)
        for o in order_by:
            if(hasattr(models.Assign, o[0])):
                if(len(o) == 2 and o[1] == 'desc'):
                    stmt = stmt.order_by(getattr(models.Assign, o[0]).desc())
                else:
                    stmt = stmt.order_by(getattr(models.Assign, o[0]).asc())

    rows = db.scalars(stmt).all()

    for i in rows:
        if(load_1_assign_user):
            i.assign_user = read_user_byId(db, user, i.assign_user_id)
        pass

    for i in rows:
        pass

    for i in range(len(rows)):
        rows[i].row_number = (pageSize * (page-1)) + i + 1
        pass

    return {
        "rows": rows, 
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "all_rows": all_rows,
        "order_by": order_by,
        "query_json": query_json,
        #"stmt": str(stmt).replace("\"", "`"),
        #"debug_str": debug_str
    }


## read_assign_byId -------------------------------------------------------------
def read_assign_byId(db: Session, user, id:int
    ,load_user_assign_user: bool = False
):
    result = db.get(models.Assign, id)
    if(load_user_assign_user and result):
        result.assign_user = read_user_byId(db, user, result.assign_user_id)

    return result

## insert_assign -------------------------------------------------------------
def insert_assign (
    db: Session
    ,user
    ,the_Assign: schemas.Assign
):

    db_thing = models.Assign(
                assign_user_id=the_Assign.assign_user_id, 
                assign_moment=the_Assign.assign_moment, 
                assign_pagenumber=the_Assign.assign_pagenumber, 
                assign_status=the_Assign.assign_status, 
                assign_done_moment=the_Assign.assign_done_moment, 
                assign_follow_result=the_Assign.assign_follow_result 
            )
    db.add(db_thing)    
    db.flush()
    db.refresh(db_thing)

    result = {
        "the_Assign": jsonable_encoder(db_thing)
    }

    return result


## patch_assign -------------------------------------------------------------
def patch_assign(db: Session,user,id: int, fields):

    assign_user_id = fields.get('assign_user_id', None)
    assign_moment = fields.get('assign_moment', None)
    assign_moment = schemas.parse_ZDate(assign_moment)
    assign_pagenumber = fields.get('assign_pagenumber', None)
    assign_status = fields.get('assign_status', None)
    assign_done_moment = fields.get('assign_done_moment', None)
    assign_done_moment = schemas.parse_ZDate(assign_done_moment)
    assign_follow_result = fields.get('assign_follow_result', None)


    db_thing = db.get(models.Assign, id)


    if(assign_user_id is not None):
        db_thing.assign_user_id = assign_user_id
    if(assign_moment is not None):
        db_thing.assign_moment = assign_moment
    if(assign_pagenumber is not None):
        db_thing.assign_pagenumber = assign_pagenumber
    if(assign_status is not None):
        db_thing.assign_status = assign_status
    if(assign_done_moment is not None):
        db_thing.assign_done_moment = assign_done_moment
    if(assign_follow_result is not None):
        db_thing.assign_follow_result = assign_follow_result

    result = {
        "the_Assign": jsonable_encoder(db_thing)
    }

    return result

## delete_assign -------------------------------------------------------------
def delete_assign(db: Session, user, id: int):

    result = { }
    thing = db.get(models.Assign, id)
    if(thing):

        db.delete(thing)
        result["thing"] = jsonable_encoder(thing)
        result["state"] = "deleted"

        return result

        # end if

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

    load_1_py_user = fields.get('load_1_py_user', False)
    query_json_py_user = fields.get('query_json_py_user', '[]')
    

#    debug_str = []
    stmt = select(models.Payment)

    query_json = parse_json(query_json)
    if(query_json):
        for f in query_json:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(models.Payment, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(models.Payment, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(models.Payment, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(models.Payment, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(models.Payment, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(models.Payment, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(models.Payment, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(models.Payment, f['field']).in_(f['value']))

    if(filter):
        stmt = stmt.where(
            or_(
                models.Payment.py_amount.contains(filter),  
                models.Payment.py_desc.contains(filter),  
                models.Payment.py_state.contains(filter),  
                models.Payment.py_date.contains(filter),  
                models.Payment.py_RefId.contains(filter),  
                models.Payment.py_xpaypingrequestid.contains(filter)  
            )
        )


    _py_user = aliased(models.User, name="_py_user")
    query_json_py_user = parse_json(query_json_py_user)

    if(query_json_py_user):
        stmt = stmt.join(_py_user, models.Payment.py_user_id == _py_user.id)

        for f in query_json_py_user:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_py_user, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_py_user, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_py_user, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_py_user, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_py_user, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_py_user, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_py_user, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_py_user, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_py_user NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_py_user NOT FOUND" )



    # load related_to back fields

    total = db.scalars(stmt.with_only_columns(func.count(models.Payment.id))).first()
    
    if(not all_rows):
        stmt = stmt.limit(pageSize)
        stmt = stmt.offset((page - 1) * pageSize)

    if(order_by):
        order_by = parse_json(order_by)
        for o in order_by:
            if(hasattr(models.Payment, o[0])):
                if(len(o) == 2 and o[1] == 'desc'):
                    stmt = stmt.order_by(getattr(models.Payment, o[0]).desc())
                else:
                    stmt = stmt.order_by(getattr(models.Payment, o[0]).asc())

    rows = db.scalars(stmt).all()

    for i in rows:
        if(load_1_py_user):
            i.py_user = read_user_byId(db, user, i.py_user_id)
        pass

    for i in rows:
        pass

    for i in range(len(rows)):
        rows[i].row_number = (pageSize * (page-1)) + i + 1
        pass

    return {
        "rows": rows, 
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "all_rows": all_rows,
        "order_by": order_by,
        "query_json": query_json,
        #"stmt": str(stmt).replace("\"", "`"),
        #"debug_str": debug_str
    }


## read_payment_byId -------------------------------------------------------------
def read_payment_byId(db: Session, user, id:int
    ,load_user_py_user: bool = False
):
    result = db.get(models.Payment, id)
    if(load_user_py_user and result):
        result.py_user = read_user_byId(db, user, result.py_user_id)

    return result

## insert_payment -------------------------------------------------------------
def insert_payment (
    db: Session
    ,user
    ,the_Payment: schemas.Payment
):

    db_thing = models.Payment(
                py_user_id=the_Payment.py_user_id, 
                py_amount=the_Payment.py_amount, 
                py_desc=the_Payment.py_desc, 
                py_state=the_Payment.py_state, 
                py_date=the_Payment.py_date, 
                py_RefId=the_Payment.py_RefId, 
                py_xpaypingrequestid=the_Payment.py_xpaypingrequestid 
            )
    db.add(db_thing)    
    db.flush()
    db.refresh(db_thing)

    result = {
        "the_Payment": jsonable_encoder(db_thing)
    }

    return result


## patch_payment -------------------------------------------------------------
def patch_payment(db: Session,user,id: int, fields):

    py_user_id = fields.get('py_user_id', None)
    py_amount = fields.get('py_amount', None)
    py_desc = fields.get('py_desc', None)
    py_state = fields.get('py_state', None)
    py_date = fields.get('py_date', None)
    py_date = schemas.parse_ZDate(py_date)
    py_RefId = fields.get('py_RefId', None)
    py_xpaypingrequestid = fields.get('py_xpaypingrequestid', None)


    db_thing = db.get(models.Payment, id)


    if(py_user_id is not None):
        db_thing.py_user_id = py_user_id
    if(py_amount is not None):
        db_thing.py_amount = py_amount
    if(py_desc is not None):
        db_thing.py_desc = py_desc
    if(py_state is not None):
        db_thing.py_state = py_state
    if(py_date is not None):
        db_thing.py_date = py_date
    if(py_RefId is not None):
        db_thing.py_RefId = py_RefId
    if(py_xpaypingrequestid is not None):
        db_thing.py_xpaypingrequestid = py_xpaypingrequestid

    result = {
        "the_Payment": jsonable_encoder(db_thing)
    }

    return result

## delete_payment -------------------------------------------------------------
def delete_payment(db: Session, user, id: int):

    result = { }
    thing = db.get(models.Payment, id)
    if(thing):

        db.delete(thing)
        result["thing"] = jsonable_encoder(thing)
        result["state"] = "deleted"

        return result

        # end if

    return result


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

    load_1_user = fields.get('load_1_user', False)
    query_json_user = fields.get('query_json_user', '[]')
    

#    debug_str = []
    stmt = select(models.Sms)

    query_json = parse_json(query_json)
    if(query_json):
        for f in query_json:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(models.Sms, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(models.Sms, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(models.Sms, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(models.Sms, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(models.Sms, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(models.Sms, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(models.Sms, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(models.Sms, f['field']).in_(f['value']))

    if(filter):
        stmt = stmt.where(
            or_(
                models.Sms.sms_messageId.contains(filter),  
                models.Sms.sms_moment.contains(filter),  
                models.Sms.sms_receptor.contains(filter),  
                models.Sms.sms_message.contains(filter),  
                models.Sms.sms_status.contains(filter),  
                models.Sms.sms_cost.contains(filter)  
            )
        )


    _user = aliased(models.User, name="_user")
    query_json_user = parse_json(query_json_user)

    if(query_json_user):
        stmt = stmt.join(_user, models.Sms.user_id == _user.id)

        for f in query_json_user:
            if(('ops' in f) and ('zdate' in f['ops'])):
                f['value'] = schemas.parse_ZDate(f['value'])
            if(hasattr(_user, f['field'])):
                if(f['op'] == 'eq'):
                    stmt = stmt.where(getattr(_user, f['field']) == f['value'])
                elif(f['op'] == 'le'):
                    stmt = stmt.where(getattr(_user, f['field']) <= f['value'])
                elif(f['op'] == 'lt'):
                    stmt = stmt.where(getattr(_user, f['field']) < f['value'])
                elif(f['op'] == 'ge'):
                    stmt = stmt.where(getattr(_user, f['field']) > f['value'])
                elif(f['op'] == 'gt'):
                    stmt = stmt.where(getattr(_user, f['field']) >= f['value'])
                elif(f['op'] == 'cn'):
                    stmt = stmt.where(getattr(_user, f['field']).contains(f['value']))
                elif(f['op'] == 'in'):
                    stmt = stmt.where(getattr(_user, f['field']).in_(f['value']))
#                else:
#                    debug_str.append("OP " + f['op'] + " in query_json_user NOT FOUND" )
#            else:
#                debug_str.append("field " + f['field'] + " in query_json_user NOT FOUND" )



    # load related_to back fields

    total = db.scalars(stmt.with_only_columns(func.count(models.Sms.id))).first()
    
    if(not all_rows):
        stmt = stmt.limit(pageSize)
        stmt = stmt.offset((page - 1) * pageSize)

    if(order_by):
        order_by = parse_json(order_by)
        for o in order_by:
            if(hasattr(models.Sms, o[0])):
                if(len(o) == 2 and o[1] == 'desc'):
                    stmt = stmt.order_by(getattr(models.Sms, o[0]).desc())
                else:
                    stmt = stmt.order_by(getattr(models.Sms, o[0]).asc())

    rows = db.scalars(stmt).all()

    for i in rows:
        if(load_1_user):
            i.user = read_user_byId(db, user, i.user_id)
        pass

    for i in rows:
        pass

    for i in range(len(rows)):
        rows[i].row_number = (pageSize * (page-1)) + i + 1
        pass

    return {
        "rows": rows, 
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "all_rows": all_rows,
        "order_by": order_by,
        "query_json": query_json,
        #"stmt": str(stmt).replace("\"", "`"),
        #"debug_str": debug_str
    }


## read_sms_byId -------------------------------------------------------------
def read_sms_byId(db: Session, user, id:int
    ,load_user_user: bool = False
):
    result = db.get(models.Sms, id)
    if(load_user_user and result):
        result.user = read_user_byId(db, user, result.user_id)

    return result

## insert_sms -------------------------------------------------------------
def insert_sms (
    db: Session
    ,user
    ,the_Sms: schemas.Sms
):

    db_thing = models.Sms(
                user_id=the_Sms.user_id, 
                sms_messageId=the_Sms.sms_messageId, 
                sms_moment=the_Sms.sms_moment, 
                sms_receptor=the_Sms.sms_receptor, 
                sms_message=the_Sms.sms_message, 
                sms_status=the_Sms.sms_status, 
                sms_cost=the_Sms.sms_cost 
            )
    db.add(db_thing)    
    db.flush()
    db.refresh(db_thing)

    result = {
        "the_Sms": jsonable_encoder(db_thing)
    }

    return result


## patch_sms -------------------------------------------------------------
def patch_sms(db: Session,user,id: int, fields):

    user_id = fields.get('user_id', None)
    sms_messageId = fields.get('sms_messageId', None)
    sms_moment = fields.get('sms_moment', None)
    sms_receptor = fields.get('sms_receptor', None)
    sms_message = fields.get('sms_message', None)
    sms_status = fields.get('sms_status', None)
    sms_cost = fields.get('sms_cost', None)


    db_thing = db.get(models.Sms, id)


    if(user_id is not None):
        db_thing.user_id = user_id
    if(sms_messageId is not None):
        db_thing.sms_messageId = sms_messageId
    if(sms_moment is not None):
        db_thing.sms_moment = sms_moment
    if(sms_receptor is not None):
        db_thing.sms_receptor = sms_receptor
    if(sms_message is not None):
        db_thing.sms_message = sms_message
    if(sms_status is not None):
        db_thing.sms_status = sms_status
    if(sms_cost is not None):
        db_thing.sms_cost = sms_cost

    result = {
        "the_Sms": jsonable_encoder(db_thing)
    }

    return result

## delete_sms -------------------------------------------------------------
def delete_sms(db: Session, user, id: int):

    result = { }
    thing = db.get(models.Sms, id)
    if(thing):

        db.delete(thing)
        result["thing"] = jsonable_encoder(thing)
        result["state"] = "deleted"

        return result

        # end if

    return result


#endregion sms


