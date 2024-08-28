from tinydb import Query
from .. import db  # 引入单例数据库实例

User = Query()

TABLE_NAME = 'user'

def add_user(data, table_name=TABLE_NAME):
    try:
        # 检查 userId 是否已经存在 
        _id = data.get('userId')
        if db.table(table_name).contains(User.userId == _id):
            # userId 已经存在，插入失败
            return 0

        # userId 不存在，执行插入
        user_id = db.table(table_name).insert(data)
        return 1
    except:
        raise
    
def get_all_users(table_name=TABLE_NAME):
    try:
        return db.table(table_name).all()
    except:
        raise

def get_user(user_id, table_name=TABLE_NAME):
    try:
        user = db.table(table_name).get(User.userId == user_id)
        return user
    except:
        raise

def valid_user(data, table_name=TABLE_NAME):
    try:
        _id = data.get('userId')
        password = data.get('password')
        if db.table(table_name).contains((User.userId == _id) & (User.password == password)):
            return 1
        else:
            return 0
    except:
        raise

def update_user(user_id, data, table_name=TABLE_NAME):
    if db.table(table_name).contains(User.userId == user_id):
        try:
            db.table(table_name).update(data, UserId=user_id)
            return 1
        except:
            raise
    return 0

def delete_user(user_id, table_name=TABLE_NAME):
    if db.table(table_name).contains(User.userId == user_id):
        try:    
            db.table(table_name).remove(User.userId == user_id)
            return 1
        except:
            raise
    return 0
