# author:Xiaohan MA
# datetime:2020/8/5 14:12
# software: PyCharm


# coding:utf-8

import os
import time


from flask import Flask, request, jsonify

from keras.preprocessing import image
import numpy as np
from keras.models import load_model
from tensorflow_core.python.keras.applications.vgg16 import preprocess_input




app = Flask(__name__)

# Define the interface
@app.route('/', methods=['POST'])
def get_frame():
    start_time = time.time()
    upload_file = request.files['file']
    old_file_name = upload_file.filename
    if upload_file:
        # Receive pictures, save pictures
        file_path = os.path.join('./', old_file_name)
        upload_file.save(file_path)
        print("success")
        print('file saved to %s' % file_path)
        # Picture opening and format conversion
        img_path = "./test.jpg"
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Load model
        model = load_model('./model/model_weight.h5')
        # Predict picture
        preds = model.predict(x)
        print(preds[0][0])
        # Lable of images 
        labels = ['acne', 'eczema',  'healthy',  'psoriasis']
        # Return result
        dict = {}
        # Encapsulate the predicted result as a dictionary
        for index, label in enumerate(labels):
            dict[label] = preds[0][index]
        print(dict)
        duration = time.time() - start_time
        print('duration:[%.0fms]' % (duration * 1000))
        # Format the result returned
        return jsonify(str(dict))
    else:
        return 'failed'


if __name__ == "__main__":
    # Set the host to 0.0.0.0, then external users can also access this service
    app.run(host="0.0.0.0", port=5003, debug=True)