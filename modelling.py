import pickle
import pandas as pd
import numpy as np

model = pickle.load(open('svc.pkl', 'rb'))

arr = []
txt_file = ["problem.txt", "problem1.txt", "problem3.txt", "problem4.txt", "problem5.txt"]
for i in list(range(len(txt_file))):
    with open(txt_file[i]) as f:
        text = f.read()
        arr.append(text)

df1 = pd.read_csv('Symptom-severity.csv')


def SVM():
    a = np.array(df1["Symptom"])
    b = np.array(df1["weight"])
    for j in range(len(arr)):
        for k in range(len(a)):
            if arr[j] == a[k]:
                arr[j] = b[k]
    nulls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    psy = [arr + nulls]
    pred = model.predict(psy)
    return pred
