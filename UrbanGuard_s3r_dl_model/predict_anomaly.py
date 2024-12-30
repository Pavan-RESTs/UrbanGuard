import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import math
from matplotlib.animation import FuncAnimation
from I3D_Feature_Extraction_resnet.main import generate_single_video
from S3R.makepred import predict_single_video
import torch
from S3R.anomaly.models.detectors.detector import S3R
from calculate_threshold import binary_prediction





def get_video_frame_rate(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error opening video file {video_path}")
    
    
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return math.ceil(frame_rate)


def preload_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return []
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    return frames


def display_video_with_plot(video_path, anomaly_scores, frequency=15):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    
    fig, (ax_video, ax_plot) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]})
    ax_plot.set_xlim(0, total_frames // frequency * 0.5)
    ax_plot.set_ylim(min(anomaly_scores) - 0.05, max(anomaly_scores) + 0.05)
    ax_plot.set_xlabel('Time (seconds)')
    ax_plot.set_ylabel('Anomaly Score')
    ax_plot.set_title('Anomaly Score Over Time')

    line, = ax_plot.plot([], [], 'b-', marker='o', label='Anomaly Score')
    highlight, = ax_plot.plot([], [], 'ro', label='Current Frame')
    
    ret, frame = cap.read()
    im = ax_video.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ax_video.axis('off')

    def update(frame_idx):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            im.set_array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
        current_time = frame_idx / frame_rate
        line.set_data(np.arange(0, len(anomaly_scores)) * 0.5, anomaly_scores)
        highlight.set_data([current_time], [anomaly_scores[frame_idx // frequency]])
        
        return im, line, highlight

    ani = FuncAnimation(
        fig, 
        update, 
        frames=range(0, total_frames, 16),
        interval=500,  
        blit=True
    )

    plt.tight_layout()
    plt.show()
    cap.release()



def main(video_path, pretrained_path, model_path, dictionary_path, oversampledCrop):
    
    start_time = time.time()

    
    frame_rate = get_video_frame_rate(video_path)
    frequency = 16  

    
    print("Feature extraction started...")
    i3d_feature_vector = generate_single_video(video_path, pretrained_path, frequency, batch_size=20, sample_mode="oversample")
    

    
    
    
    
    
    
    print("Feature extraction finished")
    print(i3d_feature_vector.shape)

    
    model = S3R(dim=2048, batch_size=1, quantize_size=32, modality='taskaware')
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint)
    model = model.to('cuda')

    
    print("Prediction started...")
    anomaly_scores = predict_single_video(model, i3d_feature_vector, dictionary_path)
    
    
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")

    
    aggregation = [0.16252615, 0.84889114, 62.836292516672216]
    print(binary_prediction(anomaly_scores, oversampledCrop, aggregation))
    return binary_prediction(anomaly_scores, oversampledCrop, aggregation)


video_path = r"C:\Users\pavan\Downloads\Anomaly-Videos-Part-1\Arson\Arson011_x264.mp4"
pretrained_path = r"I3D_Feature_Extraction_resnet\pretrained\i3d_r50_kinetics.pth"
model_path = r"S3R\checkpoint\ucf-crime_s3r_i3d_best.pth"
dictionary_path = r"S3R\dictionary\ucf-crime\ucf-crime_dictionaries.taskaware.omp.100iters.50pct.npy"

if __name__ == "__main__":
    main(video_path, pretrained_path, model_path, dictionary_path)
