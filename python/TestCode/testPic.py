
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import preprocess_input
import os
# path = '../trainData/'
# path = '../testData/acne/'
# path = '../testData/eczema/'
# path = '../testData/healthy/'
from tensorflow.python.keras.saving import load_model
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# path = '../TestData/psoriasis/'
# path = '../TestData/acne/'
# path = '../TestData/eczema/'
# path = '../TestData/healthy/'
# fileList = os.listdir(path)

matrix=['../TestData/acne/','../TestData/eczema/','../TestData/healthy/','../TestData/psoriasis/']
# model = load_model('./logs/regularizers.l10.001/model_weight2.h5')
# model = load_model('./logs/regularizers.l20.001/model_weight2.h5')
# model = load_model('./logs/droput0.1/model_weight2.h5')
# model = load_model('./logs/adadelta-lr0.01/model_weight2.h5')
# model = load_model('./logs/Adagrad-lr0.01/model_weight3.h5')
# model = load_model('./logs/adma-lr0.01/model_weight.h5')
# model = load_model('./logs/SGD-lr0.01/model_weight3.h5')
model = load_model('./logs/RMSprop0.01/model_weight.h5')

def get_pic():
    acne = 0
    eczema = 0
    healthy = 0
    psoriasis = 0
    for path in matrix:
        for root, dirs, files in os.walk(path):
                print(root)
                print(dirs)
                print(files)
                for filePath in files:
                    image = load_img(root + filePath, target_size=(224, 224))

                    image = img_to_array(image)


                    image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])


                    image = preprocess_input(image)

                    predict_result = model.predict(image)
                    if predict_result[0][0]>0.5:
                        acne = acne + 1
                    if predict_result[0][1] > 0.5:
                        eczema = eczema + 1
                    if predict_result[0][2] > 0.5:
                        healthy = healthy + 1
                    if predict_result[0][3] > 0.5:
                        psoriasis = psoriasis + 1
                    # print("predict_result:", predict_result)
        print(path,acne,eczema,healthy,psoriasis)
        acne = 0
        eczema = 0
        healthy = 0
        psoriasis = 0
get_pic()

