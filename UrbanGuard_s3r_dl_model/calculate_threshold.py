import os
import numpy as np
from S3R.anomaly.models.detectors.detector import S3R
import torch
from S3R.makepred import predict_single_video
import pickle

def count_files(directory):
    count = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            count += 1
    return count

def calculate_threshold():
    path = r"C:\Users\pavan\StudioProjects\UrbanGuardV2\S3R\data\ucf-crime\i3d\test"
    model_path = r"S3R\checkpoint\ucf-crime_s3r_i3d_best.pth"
    dictionary_path = r"S3R\dictionary\ucf-crime\ucf-crime_dictionaries.taskaware.omp.100iters.50pct.npy"
    mini_arr = []
    maxi_arr = []
    anomaly_scores_arr = []
    file_count = count_files(path)

    for i, video_features in enumerate(os.listdir(path)):
        print(f"Processing video {i}/{file_count}")
        if "Normal" not in video_features:
            video_feature_path = os.path.join(path, video_features)
            i3d_feature_vector = np.load(video_feature_path)
            model = S3R(dim=2048, batch_size=1, quantize_size=32, modality='taskaware')
            checkpoint = torch.load(model_path)
            model.load_state_dict(checkpoint)
            model = model.to('cuda')
            anomaly_output = predict_single_video(model, i3d_feature_vector, dictionary_path)
            anomaly_scores_arr.append(anomaly_output)
            print(f"Mini: {np.min(anomaly_output)}, Maxi: {np.max(anomaly_output)}")
            mini_arr.append(np.min(anomaly_output))
            maxi_arr.append(np.max(anomaly_output))

    mini_avg = np.mean(mini_arr)
    maxi_avg = np.mean(maxi_arr)

    percentage_per_video_arr = []

    for anomaly_score in anomaly_scores_arr:
        total_points = anomaly_score.shape[0]
        anomaly_points = 0
        for point in anomaly_score:
            if (point >= mini_avg) and (point <= maxi_avg):
                anomaly_points += 1
        percentage = (anomaly_points/total_points) * 100
        percentage_per_video_arr.append(percentage)
    
    mean_percentage = np.mean(percentage_per_video_arr)

    metrics = {
        "Mini_avg" : mini_avg,
        "Maxi_avg" : maxi_avg,
        "Mean_percentage" : mean_percentage
        }
    
    print(metrics)

    with open('metrics.pkl', 'wb') as f: 
        pickle.dump(metrics, f) 




def binary_prediction(anomaly_pred_vector, oversampledCrop, aggregration):

    mini_avg = aggregration[0]
    maxi_avg = aggregration[1]
    mean_percentage = aggregration[2]


    sample_mini = np.min(anomaly_pred_vector)
    sample_maxi = np.max(anomaly_pred_vector)

    total_points = anomaly_pred_vector.shape[0]

    count = 0

    for i in anomaly_pred_vector:
        if (i >= mini_avg) and (i <= maxi_avg):
            count += 1
    
    sample_percentage = (count/total_points) * 100

    with open('S3R/oversampling_vector.pkl', 'rb') as file:
        sampling = pickle.load(file)

    if (sampling[oversampledCrop]):
        return 1
    else:
        return 0

if __name__ == "__main__":
    calculate_threshold()






