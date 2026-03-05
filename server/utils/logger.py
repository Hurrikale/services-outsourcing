import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别
    
    # 控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # 文件处理器
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    fh = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    fh.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger

logger = setup_logger(__name__)
