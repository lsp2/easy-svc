from flask import Flask, render_template, request, send_from_directory, send_file
from flask_cors import *  # 导入模块
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from db.module import *
from svc import inference_main as Inference
from datetime import timedelta
import json
import time
import os
import logging

server = Flask(__name__)
server.template_folder = 'template'
server.static_folder  = "static"
server.config['JWT_SECRET_KEY'] = 'HS256'
server.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
JWTManager(server)
CORS(server, supports_credentials=True)  # 设置跨域
HOST = "127.0.0.1"

log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

MODELS_DIR = "svc\\trained"

progressDict = {}


@server.route('/upload/start', methods=['POST'], endpoint="startUpload")
@jwt_required()
def start_upload():
    try:
        id = get_jwt_identity()
        file = request.files.get("audio_file")
        if file is None:
            raise
        file_name = file.filename
        url = '/upload/' + id + "-" + file_name

        if update_audio({'userId': id, 'name': file_name, 'url': url}) is True:
            file.save(os.path.dirname(__file__) + url)  # 保存文件
        else:
            raise

        return  {
                'flag': 1,
                'file': {
                    'name': file_name,
                    'url': url
                }
            }
    except:
        return {
            'flag': 0,
        }
   

@server.route('/upload/audio', methods=['DELETE'], endpoint="deleteUploadFile")
@jwt_required()
def delete_upload_file():
    file_name = request.args["name"]
    id = get_jwt_identity()
    try: 
        if delete_audio(id) is True:
            print(os.path.dirname(__file__) + '/output/' + id + "-" + file_name)
            os.remove(os.path.dirname(__file__)+'/upload/' + id + "-" + file_name)
            return {
                'flag': 1
            }
        else:
            raise
    except:
        return {
            'flag': 0
        }
    
@server.route('/upload/audio', methods=['GET'], endpoint="getUploadFile")
@jwt_required()
def get_upload_file():
    try:
        id = get_jwt_identity()
        data = get_audio(id)
        if data is not None:
            return {
                'flag': 1,
                'file': data
            }
        else:
            raise
    except:
        return {
            'flag': 0
        }

@server.route('/process/start', methods=['GET'], endpoint="startProcess")
@jwt_required()
def start_process():
    try:
        user_id = get_jwt_identity()
        file_name = request.args["name"]
        spk_id = request.args["spk"]
        root = os.path.dirname(__file__)
        input_file_path = root + '/upload/' + user_id + "-" + file_name
        output_file_path = root + '/output/' + user_id + "-" + file_name
        progressDict[user_id] = 0
        
        if Inference.main(progressDict, user_id, spk_id, os.path.join(MODELS_DIR, spk_id), [input_file_path], output_file_path):
            progressDict.pop(user_id)
            url = '/output/' + user_id + "-" + file_name
            create_time = int(time.time())
            data = { "userId": user_id, "spk": spk_id, "fileName": file_name, "url": url, "createTime": create_time }
            update_record(data)
            return {
                'flag': 1,
                'file':{
                    'spk': spk_id,
                    'name': file_name,
                    'url': url,
                    'createTime': create_time 
                }
            }
        else:
            raise
    except:
        progressDict.pop(user_id)
        return {
            'flag': 0
        }
    
@server.route('/process/progress', methods=['GET'], endpoint="getProgressValue")
@jwt_required()
def get_progress_file():
    try:
        id = get_jwt_identity()
        return {
            'flag': 1,
            'value': progressDict[id]
        }   

    except:
        return {
            'flag': 0
        }  

@server.route('/process/audio', methods=['GET'], endpoint="getProcessFile")
@jwt_required()
def get_process_file():
    try:
        id = get_jwt_identity()
        data = get_record(id)
        if data is not None:
            return {
                'flag': 1,
                'file': {
                    'spk': data.get("spk"),
                    'name': data.get("fileName"),
                    'url': data.get("url"),
                    'createTime': data.get("createTime")
                }
            }
        else:
            raise
    except:
        return {
            'flag': 0
        }

@server.route('/process/audio', methods=['DELETE'], endpoint="deleteProcessFile")
@jwt_required()
def delete_process_file():
    file_name = request.args["name"]
    id = get_jwt_identity()
    try: 
        if delete_record(id) is True:
            os.remove(os.path.dirname(__file__) + '/output/' + id + "-" + file_name)
            return {
                'flag': 1
            }
        else:
            raise
    except:
        return {
            'flag': 0
        }
    
@server.route('/process/audio/download/<path:file_name>', methods=['GET'], endpoint="downloadProcessFile")
@jwt_required()    
def download_file(file_name):
    id = get_jwt_identity()
    return send_from_directory(os.path.dirname(__file__) + '/output/', id + "-" + file_name , as_attachment=True)
 
@server.route('/user/info', methods=['GET'], endpoint="getUserInfo")
@jwt_required()
def get_user_info():
    try:
        id = get_jwt_identity()
        data = get_user(id)
        return {
            'flag': 1,
            'user': data
        }
    
    except:
        return {
            'flag': 0
        }  

@server.route('/user/login', methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
        if valid_user(data):
            return {
                'flag': 1,
                'token': create_access_token(data.get("userId"))
            }
        else:
            return {
                'flag': -1
            }    
    except:
        return {
            'flag': 0
        }  


@server.route('/user/register', methods=['POST'])
def register():
    try:
        data = json.loads(request.data)
        if add_user(data):
            return {
                'flag': 1,
                'userId': data.get("userId"),
                'password': data.get("password")
            }
        else:
            return {
                'flag': -1
            }    
    except:
        return {
            'flag': 0
        }  
    

@server.route('/vocal/all', methods=['GET'])
def get_all():
    try:
        data = get_all_vocals()
        return {
            'flag': 1,
            'vocals': data
        }    
    except:
        return {
            'flag': 0
        }  

@server.route('/')
def index():
    return render_template('index.html') # 调用模板文件并传递参数。

@server.route('/src/<path:file_url>', methods=['GET'])
def get_file(file_url):
    return send_file(os.path.join(os.path.dirname(__file__), file_url))

if __name__ == '__main__':
    #server.run() # 启动flask内部服务器，主机地址和端口号选取默认值
    server.run(port=8888, host=HOST, debug=True, threaded=True) 
    # debug=True 开启了debug调试模式，只要代码改变，服务器就会重新加载最新代码，适合开发环境。
    # debug=False 代码修改，服务器不会重新加载，适合生成环境。