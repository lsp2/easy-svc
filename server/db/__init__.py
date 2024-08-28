from tinydb import TinyDB
import os
import threading
from .config import DB_DIR, DB_FILENAME, TABLE_NAME  # 引入配置文件

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_db(*args, **kwargs)
        return cls._instance

    def _init_db(self, *args, **kwargs):
        # 确保数据库目录存在
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)

        # 数据库文件路径
        db_path = os.path.join(DB_DIR, DB_FILENAME)

        # 初始化 TinyDB 实例
        self._db = TinyDB(db_path)

        # 加载配置中的表名并创建表
        self._initialize_tables()

    def _initialize_tables(self):
        for name in TABLE_NAME:
            if name not in self._db.tables():
                self._db.table(name)

    def get_db(self):
        return self._db

# 创建数据库单例实例
db = Database().get_db()
