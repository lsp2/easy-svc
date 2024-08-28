from tinydb import Query
from .. import db  # 引入单例数据库实例

Record = Query()

TABLE_NAME = 'record'

def update_record(data, table_name=TABLE_NAME):

    _id = data.get("userId")
    if db.table(table_name).contains(Record.userId == _id):
        try:
            db.table(table_name).update(data, Record.userId == _id)
            return True
        except:
          return False
    else:
        try:
            db.table(table_name).insert(data)
            return True
        except:
          return False

def get_record(user_id, table_name=TABLE_NAME):
    try:
        record = db.table(table_name).get(Record.userId == user_id)
        return record
    except:
        raise


def delete_record(user_id, table_name=TABLE_NAME):
    if db.table(table_name).contains(Record.userId==user_id):
        try:    
            db.table(table_name).remove(Record.userId==user_id)
            return True
        except:
            raise
    return False