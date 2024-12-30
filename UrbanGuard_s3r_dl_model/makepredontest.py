import os
import numpy as np
from S3R.anomaly.models.detectors.detector import S3R
import torch
from S3R.makepred import predict_single_video
from calculate_threshold import binary_prediction
from calculate_threshold import count_files
import pickle

test_path = r"C:\Users\pavan\StudioProjects\UrbanGuardV2\S3R\data\ucf-crime\i3d\test"
file_count = count_files(test_path)

path = r"C:\Users\pavan\StudioProjects\UrbanGuardV2\S3R\data\ucf-crime\i3d\test"
model_path = r"S3R\checkpoint\ucf-crime_s3r_i3d_best.pth"
dictionary_path = r"S3R\dictionary\ucf-crime\ucf-crime_dictionaries.taskaware.omp.100iters.50pct.npy"

true_pred_paths = []

true_prediction = 0
false_prediction = 0
false_positive = 0
false_negative = 0

with open('anomaly_predictions.pkl', 'rb') as file:
    anomaly_predictions = pickle.load(file)


for i, files in enumerate(os.listdir(test_path)):
    video_feature_path = os.path.join(test_path, files)
    anomaly_output = anomaly_predictions[i]


    gt = -1
    if "Normal" in files:
        gt = 0
    else:
        gt = 1
    
    pred = binary_prediction(anomaly_output)
    

    if (pred == gt):
        true_prediction += 1
        true_pred_paths.append(video_feature_path)
    else:
        if (gt==0):
             false_positive += 1
        else:
             false_negative += 1
        false_prediction +=1 

print(f"{true_prediction}/{file_count} is correctly predicted")
print(f"{false_prediction}/{file_count} is wrongly predicted")
print(f"{false_positive}/{false_prediction} is false positive")
print(f"{false_negative}/{false_prediction} is false negative")



with open('true_pred.pkl', 'wb') as f: 
        pickle.dump(true_pred_paths, f) 




    

