from tinydb import Query
from .. import db  # 引入单例数据库实例

Audio = Query()

TABLE_NAME = 'audio'

def update_audio(data, table_name=TABLE_NAME):
    _id = data.get("userId")
    if db.table(table_name).contains(Audio.userId==_id):
        try:
            db.table(table_name).update(data, Audio.UserId==_id)
            return True
        except:
          return False
    else:
        try:
            db.table(table_name).insert(data)
            return True
        except:
          return False
        
def get_audio(user_id, table_name=TABLE_NAME):
    try:
        audio = db.table(table_name).get(Audio.userId==user_id)
        return audio
    except:
        raise

        
def delete_audio(user_id, table_name=TABLE_NAME):
    if db.table(table_name).contains(Audio.userId==user_id):
        try:    
            db.table(table_name).remove(Audio.userId==user_id)
            return True
        except:
            raise
    return False
