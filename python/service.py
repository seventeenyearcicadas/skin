# author:think
# datetime:2020/8/5 14:12
# software: PyCharm

"""
文件说明：

"""
# coding:utf-8
# 2019/10/22 16:01
# huihui
# ref:
import os
import time


from flask import Flask, request, jsonify

from keras.preprocessing import image
import numpy as np
from keras.models import load_model
from tensorflow_core.python.keras.applications.vgg16 import preprocess_input




app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_frame():
    start_time = time.time()
    upload_file = request.files['file']
    old_file_name = upload_file.filename
    if upload_file:
        # 接收图片，保存图片
        file_path = os.path.join('./', old_file_name)
        upload_file.save(file_path)
        print("success")
        print('file saved to %s' % file_path)
        # 图片打开及格式转换
        img_path = "./test.jpg"
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # 加载模型
        model = load_model('./model/model_weight.h5')
        # 预测图片
        preds = model.predict(x)
        print(preds[0][0])
        # 图片种类
        labels = ['acne', 'eczema',  'healthy',  'psoriasis']
        # 返回结果
        dict = {}
        # 将预测的结果封装为字典
        for index, label in enumerate(labels):
            dict[label] = preds[0][index]
        print(dict)
        duration = time.time() - start_time
        print('duration:[%.0fms]' % (duration * 1000))
        # 格式化返回
        return jsonify(str(dict))
    else:
        return 'failed'
@app.route('/test', methods=['POST'])
def get_test():
    return 'hello world tang'

if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=5003, debug=True)