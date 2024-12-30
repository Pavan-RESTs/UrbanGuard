
import logging
import os
import sys
import time
import datetime

from anomaly.apis.utils import color

def setup_logger(name, save_dir, distributed_rank, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    if distributed_rank > 0:
        return logger
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    
    
    formatter = logging.Formatter("{now} - {name} - {level} - {message}".format(
            now = '%(asctime)s',
            name = '%(name)s',
            level = '%(levelname)s',
            message = '%(message)s'
        ), "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        if filename is None:
            filename = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + ".log"
        fh = logging.FileHandler(os.path.join(save_dir, filename))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def setup_tblogger(save_dir, distributed_rank):
    if distributed_rank>0:
        return None
    from tensorboardX import SummaryWriter
    tbdir = os.path.join(save_dir,'tb')
    os.makedirs(tbdir,exist_ok=True)
    tblogger = SummaryWriter(tbdir)
    return tblogger
