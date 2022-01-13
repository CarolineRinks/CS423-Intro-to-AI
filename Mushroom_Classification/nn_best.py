'''
Author: Caroline Rinks
    This file contains a static implementation of the best-performing Neural
    Network model found in 'nn_search.py'. The model is evaluated using K-Fold
    Cross Validation, its accuracy is printed, and a Precision-Recall
    Plot is created and displayed to the user.
'''
import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import PrecisionRecallDisplay, precision_score, recall_score
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier

# Hide some warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#tf.get_logger().setLevel('INFO')
#tf.compat.v1.disable_eager_execution()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

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

# Encode labels into numerical format
mappings = list()
encoder = LabelEncoder()
for i in range(len(mushroom_df.columns)):
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

def BestModel():
    model = Sequential()
    model.add(Dense(20, input_dim=22, activation='relu', name='layer_1'))
    model.add(Dense(20, activation='relu', name='layer_2'))
    model.add(Dense(2, activation='sigmoid', name='output_layer'))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    return model

estimator = KerasClassifier(build_fn=BestModel, epochs=100, batch_size=64, verbose=0)
estimator.fit(x_train, y_train)
predictions = estimator.predict(x_test)

# Evaluate Model using K-fold Cross Validation.
kfold = KFold(n_splits=3, shuffle=True)
results = cross_val_score(estimator, x_train, y_train, cv=kfold)

# Print Precision, Recall, and Accuracy.
print("\nBest Model: {'activation_one': 'relu', 'activation_two': 'relu', 'neuron_one': 20, 'neuron_two': 20}")
print("Accuracy: %f\t\tPrecision: %f\tRecall: %f" % (results.mean(),
        precision_score(y_test, predictions), recall_score(y_test, predictions)))

# Plot precision-recall curve.
PrecisionRecallDisplay.from_predictions(y_test, predictions)
plt.show()
