# -*- coding: utf-8 -*-
"""CIFAR10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X10lrVsJhjZxQvY564t5nb-TPg2KiSGk

## DATA
"""

import tensorflow as tf
# tf.config.experimental_run_functions_eagerly(True)
import tensorflow.keras as keras
import tensorflow.keras.datasets.mnist as input_data
from keras.datasets import cifar10
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tensorflow.keras import layers

from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score

mnist = cifar10.load_data()
(x_train, y_train), (x_test, y_test) = mnist

y_train

"""### shape images"""

x_train[1].shape

"""### show image"""

imgplot = plt.imshow(x_train[33])

print(y_train[33])

"""## Train Test Split
#### train %85 data & test %15 data
"""

X = np.concatenate((x_train, x_test))
y = np.concatenate((y_train , y_test))

X_train, X_test,y_train , y_test = train_test_split(X, y, test_size=15, random_state=42)

# data for predict
y_train_for_peredct = y_train
y_test_for_peredct = y_test
x_train_1_perd, x_validation_perd, y_train_1_perd, y_validation_perd = train_test_split(X, y, test_size=15)

print(X_train.shape)
print(X.shape)
print(y_train)

X_train, X_test = X_train/255.0, X_test/255.0

print(X_test[5][1][1])

y_train = to_categorical(y_train, dtype ="uint8")
y_test = to_categorical(y_test, dtype ="uint8")

y_train[1]

x_train_1, x_validation, y_train_1, y_validation = train_test_split(X_train, y_train, test_size=15)

x_train_1[1].shape

"""## Create model

#### creat model
"""

model = keras.models.Sequential()
model.add(layers.Flatten(input_shape=[32, 32,3]))
model.add(layers.Dense(200, activation='relu'))
model.add(layers.Dense(150, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(75, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.summary()

model.layers

model.layers[4]

count_layer = 2
weight, bias = model.layers[count_layer].get_weights()
print(model.layers[count_layer])
print("weight", weight)
print("bias", bias)
print("len bias", len(bias))
print("len weight", len(weight))

"""#### compile"""

model.compile(loss=keras.losses.categorical_crossentropy, optimizer='sgd', metrics=['accuracy'])

"""#### callback"""

checkpoint_filepath = "model_cifar10_checkpoint_save.h5"

model_checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, save_weights_only=True, save_best_only=True)

model_checkpoint_earlyEstping = keras.callbacks.EarlyStopping(monitor='loss',patience=10)

"""#### fit"""

history = model.fit(x_train_1, y_train_1, batch_size=128, epochs=1000,
                   validation_data=[x_validation, y_validation], callbacks=[model_checkpoint_callback,model_checkpoint_earlyEstping])

y_train_hat_probs = model.predict(x_train_1, verbose=0)
y_train_hat_classes = np.argmax(y_train_hat_probs,axis=1)

y_test_hat_probs = model.predict(X_test, verbose=0)
y_test_hat_classes = np.argmax(y_test_hat_probs,axis=1)

y_validation_hat_probs = model.predict(x_validation, verbose=0)
y_validation_hat_classes = np.argmax(y_validation_hat_probs,axis=1)

"""## evaluate"""

# # reduce to 1d array

# y_train_hat_probs= y_train_hat_probs[:, 0]
# y_test_hat_probs = y_test_hat_probs[:, 0]
# y_validation_hat_probs= y_validation_hat_probs[:, 0]

y_train_for_peredct_=[]
for i in range(len(y_train_for_peredct)):
    y_train_for_peredct_.append(y_train_for_peredct[i][0])
    
y_test_for_peredct_ = []
for i in range(len(y_test_for_peredct)):
    y_test_for_peredct_.append(y_test_for_peredct[i][0])
    
y_validation_perd_ = []
for i in range(len(y_validation_perd)):
    y_validation_perd_.append(y_validation_perd[i][0])

# accuracy: (tp + tn) / (p + n)
# f1: 2 tp / (2 tp + fp + fn)

# accuracy
accuracy_train = accuracy_score(y_train_1_perd, y_train_hat_classes)
accuracy_test = accuracy_score(y_test_for_peredct_, y_test_hat_classes)
accuracy_validation = accuracy_score(y_validation_perd_, y_validation_hat_classes)

print('Accuracy train : %f' % accuracy_train)
print('Accuracy test : %f' % accuracy_test)
print('Accuracy validation : %f' % accuracy_validation)

f1_train = f1_score(y_train_1_perd, y_train_hat_classes, average='micro')
f1_test = f1_score(y_test_for_peredct_, y_test_hat_classes, average='micro')
f1_validation = f1_score(y_validation_perd_, y_validation_hat_classes, average='micro')

print('F1 score train : %f' % f1_train)
print('F1 score test : %f' % f1_test)
print('F1 score validation : %f' % f1_validation)

# ROC AUC
auc_train = roc_auc_score(y_train_1_perd, y_train_hat_probs , multi_class='ovr')
# auc_test = roc_auc_score(y_test_for_peredct_, y_test_hat_probs, multi_class='ovr')
auc_validation = roc_auc_score(y_validation_perd_, y_validation_hat_probs, multi_class='ovr')

print('ROC AUC train : %f' % auc_train)
# print('ROC AUC test : %f' % auc_test)
print('ROC AUC validation : %f' % auc_validation)



"""## create wide and deep model

#### create model
"""

input_ = tf.keras.Input(shape=x_train_1.shape[1:])

hidden_layer_1 = keras.layers.Dense(200, activation="relu")(input_)
hidden_layer_2 = keras.layers.Dense(150, activation="relu")(hidden_layer_1)
hidden_layer_3 = keras.layers.Dense(100, activation="relu")(hidden_layer_2)
hidden_layer_4 = keras.layers.Dense(75, activation="relu")(hidden_layer_3)

concatted_layer = keras.layers.Concatenate()([hidden_layer_4, input_])
output_layer = keras.layers.Dense(10, activation='softmax')(concatted_layer)
model_function_api = keras.Model(inputs=[input_], outputs=[output_layer])

"""#### compile"""

model_function_api.compile(loss=keras.losses.categorical_crossentropy, optimizer='sgd', metrics=['accuracy'])

"""#### callback"""

checkpoint_filepath = " wide_and_deep_model_cifar10_checkpoint_save.h5"

model_checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, save_weights_only=True, save_best_only=True)

model_checkpoint_earlyEstping = keras.callbacks.EarlyStopping(monitor='loss',patience=10)

"""#### fit

"""

history_wind_and_deep = model_function_api.fit(x_train_1, y_train_1, batch_size=128, epochs=1000,
                   validation_data=[x_validation, y_validation], callbacks=[model_checkpoint_callback,model_checkpoint_earlyEstping])







"""## make function model"""

# # model = keras.models.Sequential()
# model.add(layers.Flatten(input_shape=[32, 32,3]))
# model.add(layers.Dense(200, activation='relu'))
# model.add(layers.Dense(150, activation='relu'))
# model.add(layers.Dense(100, activation='relu'))
# model.add(layers.Dense(75, activation='relu'))
# model.add(layers.Dense(10, activation='softmax'))

# model.summary()

def ann_model(number_of_hidden_layers=2,number_of_nerons=[[100, 50]]):
    model = keras.models.Sequentisl()
    model.add(keras.layers.InputLaye(input_shape=[32, 32,3]))
    
    for hidden_layer in range(number_of_hidden_layers):
        model.add(layers.Dense(number_of_nerons[hidden_layer], activation="relu"))
        
    model.add(layers.Dense(10, activation='softmax'))
    
    model.compile(loss=keras.losses.categorical_crossentropy, optimizer='sgd', metrics=['accuracy'])
    
    return model

keras_sk_reg = keras.wrappers.scikit_learn.KerasRegressor(build_fn=ann_model)











