#!/usr/bin/env python
import sys
import subprocess
import os
import time
import torch
from pathlib import Path
from PIL import Image
import streamlit as st
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

if __name__ == "__main__" and "streamlit.runtime.scriptrunner" not in sys.modules:
    print("检测到直接运行，正在启动集成服务器...")
    print("Streamlit界面: http://localhost:8501")
    print("健康检查API: http://localhost:8502/health")
    print("请稍等，浏览器将自动打开...")
    
    script_path = __file__
    
    health_server_script = os.path.join(os.path.dirname(script_path), "simple_health_server.py")
    if os.path.exists(health_server_script):
        print("🚀 启动健康检查服务器...")
        health_process = subprocess.Popen([sys.executable, health_server_script])
        time.sleep(1)
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path, "--browser.gatherUsageStats", "false"], check=True)

    except KeyboardInterrupt:
        print("\n程序已停止")
        try:
            health_process.terminate()
        except:
            pass
    except subprocess.CalledProcessError as e:
        print(f"启动Streamlit时出错: {e}")
    sys.exit(0)

st.set_page_config(
    page_title="智慧工地检测系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    )

css=''' 
<style> 
[data-testid="stFileUploaderDropzone"] div div::before{content:"将文件拖放到此处"} 
[data-testid="stFileUploaderDropzone"] div div span{display:none;} 
[data-testid="stFileUploaderDropzone"] div div::after{
    color:rgba(49,51,63,0.6);
    font-size:.8em;
    content:"每个文件限制200MB•XLSX"} 
[data-testid="stFileUploaderDropzone"] div div small{display:none;} 
[data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"]{font-size:0px;} 
[data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"]::after{
    content:"浏览文件";
    font-size:17px;} 
</style> 
'''
st.markdown(css, unsafe_allow_html=True)

st.title("智慧工地检测系统")

st.sidebar.header("模型配置")

if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
    st.sidebar.info(f"当前使用显卡: {gpu_name} ({gpu_memory:.1f}GB)")
else:
    st.sidebar.info("当前使用CPU")

task_type = st.sidebar.selectbox(
    "选择任务",
    ["检测"]
)

model_type = None
if task_type == "检测":
    model_type = st.sidebar.selectbox(
        "选择模型",
        config.DETECTION_MODEL_LIST
    )
else:
    st.error("目前仅实现了'检测'功能")

confidence = float(st.sidebar.slider(
    "选择模型置信度", 30, 100, 50)) / 100

model_path = ""
if model_type:
    model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
else:
    st.error("请在侧边栏选择模型")

try:
    model = load_model(model_path)
    global_model = model
    MODEL_PATH = str(model_path)
except Exception as e:
    st.error(f"无法加载模型。请检查指定路径: {model_path}")

st.sidebar.header("图像/视频配置")
source_selectbox = st.sidebar.selectbox(
    "选择源",
    config.SOURCES_LIST
)

if source_selectbox == config.SOURCES_LIST[0]:
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]:
    infer_uploaded_video(confidence, model)
elif source_selectbox == config.SOURCES_LIST[2]:
    infer_uploaded_webcam(confidence, model)
else:
    st.error("目前仅实现了'图像'和'视频'源")