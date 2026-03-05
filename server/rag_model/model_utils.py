from modelscope import snapshot_download
from modelscope.hub.api import HubApi
import os

def download_model():
    """下载Qwen2.5-Math模型到本地"""
    api = HubApi()
    api.login(access_token='a6d28b7d-deeb-420c-a32b-a9fb14b64621')
    
    model_dir = "./rag_model/models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
        
    try:
        model_id = "Qwen/Qwen2.5-Math-1.5B-Instruct"
        snapshot_download(model_id=model_id, 
                        cache_dir=model_dir,
                        revision='master')
        print("模型下载完成")
    except Exception as e:
        print(f"模型下载失败: {str(e)}")
        raise e

if __name__ == "__main__":
    download_model()
