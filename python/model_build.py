# author:think
# datetime:2020/7/23 9:28
# software: PyCharm

"""
文件说明：

"""
import keras
from keras import applications, regularizers
from keras.callbacks import TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model


from keras.layers import Flatten,Dense,Dropout

img_width, img_height = 224, 224
batch_size = 32
epochs = 1
train_data_dir = '../TrainData'
validation_data_dir = '../TestData'


datagen = ImageDataGenerator(horizontal_flip=True,vertical_flip=True, featurewise_center=True, samplewise_center=True, featurewise_std_normalization=True, samplewise_std_normalization=True)
train_generator = datagen.flow_from_directory(
    '../TrainData',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=batch_size)

# 读验证集图片
validation_generator = datagen.flow_from_directory(
    '../TestData',
    # classes=['acne', 'eczema','healthy','psoriasis'],
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True)
base_model = applications.VGG16(weights="imagenet",include_top=False,input_shape=(img_width,img_height,3))
base_model.summary()

for layer in base_model.layers:
    layer.trainable = False

top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(2048, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
# top_model.add(Dense(2048, activation='relu', kernel_regularizer=regularizers.l1(0.001)))
# , kernel_regularizer=regularizers.l2(0.01)
top_model.add(Dropout(0.5))
top_model.add(Dense(4, activation='softmax'))
inputs = base_model.input
outputs = top_model(base_model.output)
top_model.summary()
model = Model(inputs, outputs)
# sgd=SGD(lr=0.0001,momentum=0.9)
model.summary()
print('[INFO] compiling model')
model.compile(loss=keras.losses.categorical_crossentropy,
              # optimizer=keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True),
              # optimizer=keras.optimizers.Adagrad(lr=0.01, epsilon=1e-6),
              # optimizer=keras.optimizers.adadelta(learning_rate=1.0, rho=0.95, epsilon=1e-6),
              # optimizer=keras.optimizers.RMSprop(lr=0.01, rho=0.9, epsilon=1e-6),
              optimizer=keras.optimizers.Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999),

              metrics=['accuracy'])
print('[INFO] training model')

tbCallBack = TensorBoard(log_dir="./logs",update_freq='batch', histogram_freq=0,write_graph=True, write_images=True)

model.fit_generator(generator=train_generator, steps_per_epoch=1000 / batch_size, epochs=5,
                    validation_data=validation_generator, validation_steps=250 / batch_size, callbacks=[tbCallBack])
model.save('./model/model_weight.h5')



