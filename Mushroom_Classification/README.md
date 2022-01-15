Author: Caroline Rinks

Project 3 (Mushroom classification)

------------
Instructions
------------
To run this program, navigate to the directory where main.py is stored and type 
the following command into a terminal:

    python3 svm_search.py|svm_best.py|nn_search.py|nn_best.py

-----------
Description
-----------
This project uses Neural Networks and Support Vector Machines to classify the mushrooms 
dataset found in 'mushrooms.csv'. A coarse grid search and fine grid search are implemented 
to select the best-performing configuration of hyperparameters, which is evaluated using 
K-Fold Cross Validation. The mushrooms dataset is managed with the pandas library. The 
implementation and evaluation of Neural Networks uses the Keras and Tensorflow libraries, 
and the implementation and evaluation of Support Vector Machines uses the Scikit-learn library.

