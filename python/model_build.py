# author:Xiaohan Ma
# datetime:2020/7/23 9:28


import keras
from keras import applications, regularizers
from keras.callbacks import TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model


from keras.layers import Flatten,Dense,Dropout


# Define global variables
img_width, img_height = 224, 224
batch_size = 32
epochs = 1
train_data_dir = '../TrainData'
validation_data_dir = '../TestData'

#Data augmentation 
datagen = ImageDataGenerator(horizontal_flip=True,vertical_flip=True, featurewise_center=True, samplewise_center=True, featurewise_std_normalization=True, samplewise_std_normalization=True)


#Generate the training set
train_generator = datagen.flow_from_directory(
    '../TrainData',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=batch_size)

#Generate the Validation set
validation_generator = datagen.flow_from_directory(
    '../TestData',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True)
	
# load the original VGG16 model provided by Keras, weights are trained on the ImageNet dataset. Remove the top fully connected layer
base_model = applications.VGG16(weights="imagenet",include_top=False,input_shape=(img_width,img_height,3))

# Freeze the weights in each layer
for layer in base_model.layers:
    layer.trainable = False
	
# Create New Sequential model
top_model = Sequential()

# Add the Flatten layer
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))

# Add the Dense layer with units, activation function and regurization method setting 
top_model.add(Dense(2048, activation='relu', kernel_regularizer=regularizers.l2(0.001)))

# Add the Dropout layer with possibility of 0.5 
top_model.add(Dropout(0.5))

# Add the Dense layer and set parameters to suit our problem
top_model.add(Dense(4, activation='softmax'))

# Splice model
inputs = base_model.input
outputs = top_model(base_model.output)
model = Model(inputs, outputs)

#Print model
model.summary()

print('[INFO] compiling model')

#Compile model with choosing loss function and optimizer and metrics 
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(learning_rate=0.01, beta_1=0.9, beta_2=0.999),
              metrics=['accuracy'])
			  
print('[INFO] training model')

# Display network graph with TensorBoard
tbCallBack = TensorBoard(log_dir="./logs",update_freq='batch', histogram_freq=0,write_graph=True, write_images=True)

#Model training
model.fit_generator(generator=train_generator, steps_per_epoch=1000 / batch_size, epochs=5,
                    validation_data=validation_generator, validation_steps=250 / batch_size, callbacks=[tbCallBack])
					
# Save model
model.save('./model/model_weight.h5')



