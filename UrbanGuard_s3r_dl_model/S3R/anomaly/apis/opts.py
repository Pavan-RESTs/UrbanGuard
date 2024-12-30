
from pathlib import Path

from tap import Tap
from typing import Dict, List, Optional, Tuple, Union

try:
    from typing import Literal 
except ImportError:
    from typing_extensions import Literal

class S3RArgumentParser(Tap):
    
    
    
    backbone: Literal['i3d', 'c3d'] = 'i3d' 
    feature_size: int = 2048 
    gpus: int = 1
    lr: float = 0.001 
    batch_size: int = 32 
    workers: int = 0 
    model_name: str = 's3r' 
    dataset: Literal['shanghaitech', 'ucf-crime', 'xd-violence'] = 'ucf-crime' 
    plot_freq: int = 10 
    max_epoch: int = 15000 
    dropout: float = 0.7 
    quantize_size: int = 32 

    
    
    
    root_path: Path = 'data' 
    log_path: Path = 'logs' 
    checkpoint_path: Path = 'checkpoint' 
    dictionary_path: Path ='dictionary' 
    resume: Optional[str] = None 

    
    
    
    evaluate_freq: int = 1 
    evaluate_min_step: int = 5000 

    
    
    
    seed: Optional[int] = -1 
    version: str = 'vad-1.0' 
    debug: bool = False 
    inference: bool = False 
    report_k: int = 10 
    descr: List[str] = ['S3R', 'video', 'anomaly', 'detection'] 
