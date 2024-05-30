import datetime
current_time = datetime.datetime.now()

print("函数启动时间:", current_time)
from flask import Flask, request, send_file,jsonify
import json
import tempfile
import requests
import os
import uuid
import shutil
import time

from  api import swap_enchnacer_face

REQUEST_ID_HEADER = 'x-fc-request-id'

app = Flask(__name__)


@app.route('/list_files', methods=['GET'])
def list_files():
    directory = request.args.get('path', '/home/oss/models')  

    files = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            files.append(filename)

    return jsonify(files)

@app.route('/predict', methods=['GET'])
def predict():
    t1 = time.time()
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start with RequestId: " + rid)
    source_url = request.args.get('source_url')

    if not source_url:
        return "source_url parameter is required", 400
    unique_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = os.path.join(tmpdirname, unique_id)
        os.makedirs(temp_dir)
        source_path = os.path.join(temp_dir, 'source.jpg')
        print(f'下载文件的临时文件{source_path}')
        template_path = 'zhanying.jpg'
        output_path = os.path.join(temp_dir, 'output.jpg')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)     Version/17.5 Safari/605.1.15'
        }

        response = requests.get(source_url, headers=headers)
        if response.status_code == 200:
            with open(source_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"下载图片{source_url}失失败，返回结果: {response.text}")

        
        swap_enchnacer_face(source_path, template_path, output_path)
        
        print("Data: " + str(request.args))
        print("FC Invoke End RequestId: " + rid)
        t2 = time.time()
        print(f'耗时{t2-t1}')
        return send_file(output_path, mimetype='image/jpeg')

def downloadModels():
    source_directory = '/home/oss'
    destination_directory = os.getcwd()  

    copied_items = []
    for root, dirs, files in os.walk(source_directory):
        for dir_name in dirs:
            source_dir = os.path.join(root, dir_name)
            relative_dir = os.path.relpath(source_dir, source_directory)
            destination_dir = os.path.join(destination_directory, relative_dir)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                copied_items.append(f"Directory: {relative_dir}")
        for file_name in files:
            source_file = os.path.join(root, file_name)
            relative_file = os.path.relpath(source_file, source_directory)
            destination_file = os.path.join(destination_directory, relative_file)
            if not os.path.exists(destination_file):
                shutil.copy2(source_file, destination_file)
                copied_items.append(f"File: {relative_file}")
            else:
                copied_items.append(f"File: {relative_file} (already exists)")

if __name__ == '__main__':
 
    # downloadModels()
    app.run(host='0.0.0.0', port=9000)
