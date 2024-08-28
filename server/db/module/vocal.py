from tinydb import Query
from .. import db  # 引入单例数据库实例

Vocal = Query()

TABLE_NAME = 'vocal'

def get_all_vocals(table_name=TABLE_NAME):
    try:
        return db.table(table_name).all()
    except:
        raise  

def get_spk_name(spk_id, table_name=TABLE_NAME):
    try:
        name = db.table(table_name).get(Vocal.spkId == spk_id)
        return name
    except:
        raise