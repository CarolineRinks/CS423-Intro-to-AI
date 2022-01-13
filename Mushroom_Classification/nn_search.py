'''
Author: Caroline Rinks
    This file uses Neural Networks to classify the mushrooms dataset found in
    'mushrooms.csv'. A coarse grid search and fine grid search are implemented to select
    the best-performing configuration of hyperparameters, which is evaluated using K-Fold
    Cross Validation. The mushrooms dataset is managed with the pandas library, and the 
    Keras and Tensorflow libraries are used to implement and evaluate the Neural Nets.
'''
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
import tensorflow as tf

# Hide some warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

'''------------------------------------------------------------------------------------
Pre-Processing
------------------------------------------------------------------------------------'''
print("\nPre-processing data...\n")

# Read data from mushrooms.csv into a Dataframe
mushroom_df = pd.read_csv("mushrooms.csv")

# Remove invalid instances
invalid = []
for row in range(len(mushroom_df)):
    for i in range(len(mushroom_df.iloc[row])):
        if mushroom_df.iloc[row][i] == '?':
            invalid.append(row)
            break
for i in range(len(invalid)):
    mushroom_df.drop(invalid[i], inplace=True)

# Encode labels into numerical format - Create a dictionary that maps numeric labels to text labels
mappings = list()
encoder = LabelEncoder()
for i in range(len(mushroom_df.columns)):
    # grab a column, transform it to fit the encoder, and then return it to the original column
    mushroom_df[mushroom_df.columns[i]] = encoder.fit_transform(mushroom_df[mushroom_df.columns[i]])
    mappings_dict = {
        index: label for index, label in enumerate(encoder.classes_)
    }
    mappings.append(mappings_dict)

# Separate features from targets.
X = mushroom_df.drop("class", axis=1)
Y = mushroom_df['class']

# Split data for training and testing.
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
y_train_converted = y_train.values.ravel()

# Perform standardization on training and testing data.
scaler = MinMaxScaler(feature_range=(0,1))
x_train = pd.DataFrame(scaler.fit_transform(x_train), columns=x_train.columns, index=x_train.index)
x_test = pd.DataFrame(scaler.transform(x_test), columns=x_test.columns, index=x_test.index)

'''--------------------------------------------------------------------------------
COARSE GRID SEARCH
--------------------------------------------------------------------------------'''
print("Conducting Coarse Grid Search...")

def DynamicModel1(neurons=1, activation_func='sigmoid'):
    """ Creates a sequential Keras model that has an input layer, 
        one hidden layer, and an output layer.

        @param neurons: The number of neurons.
        @param activation_func: The activation function to use for the model.
        @return The created neural network model.
    """
    model = Sequential()
    model.add(Dense(neurons, input_dim=22, activation=activation_func, name='layer_1'))
    model.add(Dense(2, activation='sigmoid', name='output_layer'))
     
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    return model

param_grid = [
    {
        'activation_func': ['linear', 'sigmoid', 'relu', 'tanh'],
        'neurons': [1, 10, 20, 30]
    }
]

# Evaluate performance of each hyperparameter configuration.
model = KerasClassifier(build_fn=DynamicModel1, epochs=100, batch_size=64, verbose=0)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, verbose=1, cv=3)
grid_result = grid.fit(x_train, y_train)

print("\nBest parameters set found on development set:")
print(grid_result.best_params_)
best = grid_result
best_predict = best.predict(x_test)
print("Accuracy: %f\t\Precision: %f\tRecall: %f" % (accuracy_score(y_test, best_predict),
        precision_score(y_test, best_predict), recall_score(y_test, best_predict)))

print("\nOther explored model configurations")
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

'''---------------------------------------------------------------
Fine Grid Search
---------------------------------------------------------------'''
print("\nConducting Fine Grid Search...")

def DynamicModel2(neuron_one=1, neuron_two=1, activation_one='sigmoid', activation_two='sigmoid'):
    """ Creates a sequential Keras model that has an input layer, two 
        hidden layers with a dymanic number of units, and an output layer.

        @param neuron_one: The number of neurons for a layer
        @param neuron_two: The number of neurons for a layer
        @param activation_one: The activation function to use for a layer
        @param activation_two: The activation function to use for a layer
        @return: The created neural network model
    """
    model = Sequential()
    model.add(Dense(neuron_one, input_dim=22, activation=activation_one, name='layer_1'))
    model.add(Dense(neuron_two, activation=activation_two, name='layer_2'))
    model.add(Dense(2, activation='sigmoid', name='output_layer'))
     
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    return model

fine_param_grid = [
    {
        'activation_one': ['relu', 'tanh'], 
        'activation_two': ['relu', 'tanh'], 
        'neuron_one': [20, 25, 30],
        'neuron_two': [20, 25, 30]
    }
]

# Evaluate the performance of each hyperparameter configuration.
model = KerasClassifier(build_fn=DynamicModel2, epochs=90, batch_size=64, verbose=0)
grid = GridSearchCV(estimator=model, param_grid=fine_param_grid, n_jobs=-1, verbose=1, cv=3)
grid_result = grid.fit(x_train, y_train)

print("\nBest parameters set found on development set:")
print(grid_result.best_params_)
best = grid_result
best_predict = best.predict(x_test)
print("Accuracy: %f\tPrecision: %f\tRecall: %f" % (accuracy_score(y_test, best_predict),
        precision_score(y_test, best_predict), recall_score(y_test, best_predict)))

print("\nOther explored model configurations")
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (+/-%f) for %r" % (mean, stdev, param))
