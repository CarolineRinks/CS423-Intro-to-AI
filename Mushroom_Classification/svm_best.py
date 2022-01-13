'''
Author: Caroline Rinks
This file contains a static implementation of the best-performing SVM model
found in 'svm_search.py'. The model is evaluated using K-Fold Cross Validation,
its accuracy is printed, and a Precision-Recall Plot is created and displayed
to the user.
'''
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, PrecisionRecallDisplay
from sklearn.svm import SVC

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

# Static implementation of best-performing model
model = SVC(kernel='linear', C=100).fit(x_train, y_train_converted)

# Run test data through the trained model.
predictions = model.predict(x_test)

print("\nBest Model: {'C': %s, 'kernel': %s}" % (model.get_params()['C'], model.get_params()['kernel']))
print("Accuracy: %0.3f\t\tPrecision: %0.3f\tRecall: %0.3f" % (accuracy_score(y_test, predictions),
    precision_score(y_test, predictions), recall_score(y_test, predictions)))

# Use sklearn to plot precision-recall curve
PrecisionRecallDisplay.from_estimator(model, x_test, y_test)
plt.show()