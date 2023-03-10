# -*- coding: utf-8 -*-
"""Final Working hours_py.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18anHh5qev271jZ4fIGaLZtkYXrBl6pTA
"""

# -*- coding: utf-8 -*-
"""Work Preference  Predictions-1D RNN__Time_Series.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k8jM573egLzoTbOg6x9eGtqRwejnuRoZ
"""

# Commented out IPython magic to ensure Python compatibility.
#@title
# %matplotlib inline
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, GRU, Embedding
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from tensorflow.keras.backend import square, mean

import pandas as pd

df = pd.read_excel('/content/try_woking_hours.xlsx')

print(df.head())


"""The data observed once per candidate in six months.  Total candidates are x, say 100 to start with.
If we want to predict the for next six months ahead of time, the data is shifted by 30*6 observation points. After that new entries are made for same candidates. 
However, the data is not continous, all values per candidate is not there. The look ahead can be experimented and learned in with time. k_look_ahead to be changed as per requirements of modelling.
"""

shift_data = 15

target_names = ['NoHours']
df_targets = df[target_names] 


df_targets = df[target_names].shift(-shift_data)

feature_names = [ 'GMT','D', 'M','Y', 'LAT',  'LONG' ,	'Weight',	'Income',	'Age',	'Gender',	'WorkingHours',	'TypeOfWork',	'Health',	'NumChildren'	,'Married',	'Relatationship',	'Nuclear family',	'DietVegNonVeg']
df_feature  = df[feature_names] 


x_data = df_feature.values[0:-shift_data]
y_data = df_targets.values[:-shift_data]


x_train, x_test, y_train, y_test=train_test_split(x_data, y_data, test_size=0.15)
 

validation_data = (np.expand_dims(x_test, axis=0),
                   np.expand_dims(y_test, axis=0))

num_x = x_data.shape[1]
print(num_x)

num_y = y_data.shape[1]
print(num_y)

 
num_train =  x_train.shape[0] 
print(num_train)
num_test =  x_test.shape[0]
print(num_test)

 

def batch_generator(batch_size, sequence_length):
 
    while True:
        x_type = (batch_size, sequence_length, num_x)
        x_batch = np.zeros(shape=x_type, dtype=np.float16)
        y_type = (batch_size, sequence_length, num_y)
        y_batch = np.zeros(shape=y_type, dtype=np.float16)

        for i in range(batch_size):
            i = np.random.randint(num_train - sequence_length)
            x_batch[i] = x_train[i:i+sequence_length]
            y_batch[i] = y_train[i:i+sequence_length]        
        yield (x_batch, y_batch)

batch_size = 50
sequence_length = 30 * 1
sequence_length

generator = batch_generator(batch_size=batch_size,
                            sequence_length=sequence_length)

x_batch, y_batch = next(generator)

print(x_batch.shape)
print(y_batch.shape)

 

validation_data = (np.expand_dims(x_test, axis=0),
                   np.expand_dims(y_test, axis=0))

model2 = Sequential()
model2.add(GRU(units=512,
              return_sequences=True,
              input_shape=(None, num_x)))

model2.add(Dense(num_y, activation='sigmoid'))


optimizer = RMSprop(lr=1e-3)
model2.compile(loss='mse', optimizer=optimizer)

model2.summary()
 
 
model2.fit(x=generator,
           epochs=100,
           steps_per_epoch=50,
          validation_data=validation_data)



result = model2.evaluate(x=np.expand_dims(x_test, axis=0),
                        y=np.expand_dims(y_test, axis=0))

print("loss is", result)
 
x  = x_test
y  = y_test

end = 0 + 50
x  = x[0:end]
y  = y[0:end]
x = np.expand_dims(x, axis=0)
y_pred = model2.predict(x=x)
cls_pred = np.argmax(y_pred, axis=1)

print(y_pred)