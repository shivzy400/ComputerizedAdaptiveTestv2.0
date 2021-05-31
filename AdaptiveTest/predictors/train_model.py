import os
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV , train_test_split
from sklearn.metrics import accuracy_score

#--------initialize data---------------
os.chdir(r'D:\ProjectsFolder\Flask Projects\CAT2.0\AdaptiveTest')
data = pd.read_csv(r'DataSets\marks_predict.csv')
print(data.head(10))

op_col = list(data.columns)[-1]
data_attr = data.drop(columns=[op_col])
data_class = data[op_col]

#-------model creation-----------------
svc_model = SVC()
X_train , X_test , y_train , y_test = train_test_split(data_attr , data_class , test_size=0.1 , random_state = 0)
print(f'\nX_train : {X_train.shape}\nX_test : {X_test.shape}')

#------model testing-----------------
svc_model.fit(X_train , y_train)
y_pred = svc_model.predict(X_test)
print(f'Accuracy of SVC without HP tuning : {accuracy_score(y_test , y_pred)}')

#------Hyperparameter Tuning---------
svc_model_new = SVC()
params = {
      'C' : [0.0001 , 0.001 , 0.01 , 0.1 , 1 , 10 , 100 , 1000],
      'gamma' : [0.0001 , 0.001 , 0.01 , 0.1 , 1 , 10 , 100 , 1000]
}

search = GridSearchCV(svc_model_new , params , cv = 5)
search.fit(X_train,y_train)
print('Grid Search Done...!')

print(f'Best Parameters : {search.best_params_}')
print(f'Best Score : {search.best_score_}')

#------applying best params in svc------------
svc_model = SVC(C=1000 , gamma = 0.01)
svc_model.fit(X_train , y_train)
y_pred = svc_model.predict(X_test)
print(f'Accuracy of SVC with HP tuning : {accuracy_score(y_test , y_pred)}')

#-------saving the model---------
import pickle
filename = 'marks_predictor.pkl'
pickle.dump(svc_model , open(filename , 'wb'))
print('Model Saved')
