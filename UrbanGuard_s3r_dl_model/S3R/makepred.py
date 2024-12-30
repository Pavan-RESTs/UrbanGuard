import torch
import numpy as np
import matplotlib.pyplot as plt
from S3R.anomaly.models.detectors.detector import S3R


def predict_single_video(model, feature_vector, dictionary_path, device='cuda'):
    
    features = feature_vector  
    features = np.array(features, dtype=np.float32)  
    
    t, n_group, channels = features.shape
    features = np.transpose(features, (2, 0, 1))  
    features = np.transpose(features, (2, 1, 0))

    video = torch.from_numpy(features).unsqueeze(0).to(device)

    
    dictionary = np.load(dictionary_path)
    dictionary = np.array(dictionary, dtype=np.float32)
    dictionary = torch.from_numpy(dictionary).unsqueeze(0).to(device)
    
    model.eval()
    with torch.no_grad():
        pred = torch.zeros(0).to(device)
        outputs = model(video, dictionary)
        logits = outputs['video_scores']
        logits = torch.squeeze(logits, 1)
        scores = torch.mean(logits, 0)
        
        sig = logits
        pred = torch.cat((pred, sig))
        pred = pred.cpu().detach().numpy()
        pred = np.repeat(np.array(pred), 16)

        
    return scores.cpu().detach().numpy()



if __name__ == "__main__":
    model_path = "checkpoint/ucf-crime_s3r_i3d_best.pth"
    dictionary_path = "dictionary/ucf-crime/ucf-crime_dictionaries.taskaware.omp.100iters.50pct.npy"
    video_path = r"C:\Users\pavan\StudioProjects\UrbanGuardV2\I3D_Feature_Extraction_resnet\output\samplevideos\Usethis.npy"

    model = S3R(dim=2048, batch_size=1, quantize_size=32, modality='taskaware')
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint)
    model = model.to('cuda')
    
    prediction = predict_single_video(model, video_path, dictionary_path)


    print(f"Anomaly score: {prediction}")

    
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(len(prediction)), prediction, label="Anomaly Score", color='b', marker='o')
    plt.title('Anomaly Scores Over Time')
    plt.xlabel('Time Steps (or Frame Indices)')
    plt.ylabel('Anomaly Score')
    plt.grid(True)
    plt.legend()
    plt.show()
