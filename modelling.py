import pickle
import pandas as pd
import numpy as np
import re
import json

model = pickle.load(open('svc.pkl', 'rb'))




df1 = pd.read_csv('Symptom-severity.csv')


def SVM():
    with open('data.json', 'r') as openfile:
        json_object = json.load(openfile)
    arr = list(json_object.values())

    a = np.array(df1["Symptom"])
    b = np.array(df1["weight"])
    for j in range(len(arr)):
        for k in range(len(a)):
            if arr[j] == a[k]:
                arr[j] = b[k]
    nulls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    psy = [arr + nulls]
    pred = model.predict(psy)
    val = str(pred)
    res = re.sub(r'[^\w\s]', '', val)
    return res

