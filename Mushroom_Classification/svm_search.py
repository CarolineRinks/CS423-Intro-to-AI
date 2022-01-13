'''
Author: Caroline Rinks
    This file uses Support Vector Machines to classify the mushrooms dataset found in
    'mushrooms.csv'. A coarse grid search and fine grid search are implemented to select
    the model with the best-performing configuration of hyperparameters, which is evaluated 
    using K-Fold Cross Validation. The mushrooms dataset is managed with the pandas library, 
    and the scikit-learn library is used to implement and evaluate the SVMs.
'''

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.svm import SVC

"""---------------------------------------------------------------------------------------
Pre-Processing
---------------------------------------------------------------------------------------"""
print("\nPre-processing data...")

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

"""---------------------------------------------------------------------------------------
COARSE GRID SEARCH
---------------------------------------------------------------------------------------"""
tuned_parameters = [
    {
        'kernel': ['linear'], 
        'C': [10, 1000]
    },
    {
        'kernel': ['sigmoid'],
        'C': [10, 1000]
    },
    {
        'kernel': ['poly'], 
        'degree': [2, 3, 4],
        'C': [10, 1000]
    },
    {
        'kernel': ['rbf'], 
        'gamma': [1e-3, 1e-4],
        'C': [10, 1000]
    }
]

# Select best-performing hyper-parameter configuration using a Coarse Grid Search
# Evaluates models using K-Fold Cross Validation
print("Conducting Coarse Grid Search...")
clf = GridSearchCV(estimator=SVC(), param_grid=tuned_parameters, verbose=1)
clf.fit(x_train, y_train)

print("\nBest parameters set found on development set:")
print(clf.best_params_)
best = clf
best_predict = best.predict(x_test)
print("Accuracy: %0.3f\t\tPrecision: %0.3f\tRecall: %0.3f" % (accuracy_score(y_test, best_predict),
        precision_score(y_test, best_predict), recall_score(y_test, best_predict)))

print("\nOther explored model configurations:")
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%f (+/-%f) for %r" % (mean, std * 2, params))

'''-----------------------------------------------------------------------------------------------------
FINE GRID SEARCH
-----------------------------------------------------------------------------------------------------'''
fine_tuned_parameters = [
    {
        'kernel': ['linear'], 
        'C': [1, 100, 250, 500, 750, 1000]
    },
    {
        'kernel': ['poly'], 
        'degree': [3, 4],
        'C': [1, 100, 250, 500, 750, 1000]
    }
]

# Select best-performing hyper-parameter configuration using a Fine Grid Search
# Evaluates models using K-Fold Cross Validation
print("\nConducting Fine Grid Search...")
clf = GridSearchCV(estimator=SVC(), param_grid=fine_tuned_parameters, verbose=1)
clf.fit(x_train, y_train)

best = clf
best_predict = best.predict(x_test)
print("\nBest parameters set found on development set:")
print(clf.best_params_)
print("Accuracy: %0.3f\t\tPrecision: %0.3f\tRecall: %0.3f" % (accuracy_score(y_test, best_predict),
        precision_score(y_test, best_predict), recall_score(y_test, best_predict)))

print("\nOther explored model configurations:")
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%f (+/-%f) for %r" % (mean, std * 2, params))
    