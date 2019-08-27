import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import sys
import json
import datetime
import pandas as pd
import io
import os


# query params
device = int(sys.argv[1])
sensor = int(sys.argv[2])
models_dir = sys.argv[3]
data_dir = sys.argv[4]
data_file_name = sys.argv[5]
preds_dir = sys.argv[6]

model_name = "model_{0}_{1}".format(device, sensor)

# get data
data = pd.read_csv(data_dir + "/" + data_file_name)
data = data[(data["Device"] == device) & (data["Sensor"] == sensor)]
tss = data["TS"]
vals = np.array(data["Value"])

# load model
print("Loading model")
with open(models_dir + "/" + model_name, "rb") as f:
    pipe = pickle.load(f)


# predict
preds = pipe.predict(vals.reshape(-1, 1))
preds = np.where(preds == 1, 0, 1)  # 1 indicates an anomaly, 0 otherwise

# csv results
res = pd.DataFrame(
    {
        "TS": tss,
        "Device": np.repeat(device, len(preds)),
        "Sensor": np.repeat(sensor, len(preds)),
        "Val": vals,
        "Prediction": preds,
    }
)
res = res[["TS", "Device", "Sensor", "Val", "Prediction"]]

res_file_name = "preds_{0}_{1}_{2}.csv".format(
    device, sensor, datetime.datetime.now().strftime("%y%m%d%H%M%S")
)


# save predictions
print("Saving predictions")
os.makedirs(preds_dir)
with open(preds_dir + "/" + res_file_name, "w") as f:
    res.to_csv(f, index=None)

