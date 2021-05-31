import pandas as pd
import pickle
from sklearn.svm import SVC
import os

os.chdir(r'D:\ProjectsFolder\Flask Projects\CAT2.0\AdaptiveTest')
data = pd.read_csv(r'DataSets\marks_predict.csv')
print(data.head(10))

model = pickle.load(open('marks_predictor.pkl' , 'rb'))
print(model)


test_tuple = [10 , 40 , 5 ]
pred = model.predict([test_tuple])
print(pred[0])

